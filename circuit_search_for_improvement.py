from circuit import Circuit
from itertools import combinations, product
import pycosat


def find_circuit(input_labels, gates_count, in_tt, out_tt, shift=0):
    number_of_input_gates = len(next(iter(in_tt.values())))
    number_of_outputs = len(next(iter(out_tt.values())))
    variables = {'dummy': 0}
    input_gates = list(range(number_of_input_gates))
    internal_gates = list(range(number_of_input_gates, number_of_input_gates + gates_count))
    gates = list(range(number_of_input_gates + gates_count))
    outputs = list(range(number_of_outputs))

    assert all(str(gate) not in input_labels for gate in internal_gates)

    def variable_number(name):
        if name in variables:
            return variables[name]

        variables[name] = len(variables) + 1
        return variables[name]

    # output of gate on inputs (a, b)
    def gate_type_variable(gate, a, b):
        assert 0 <= a <= 1 and 0 <= b <= 1
        assert gate in gates
        return variable_number(f'f_{gate}_{a}_{b}')

    # gate operates on gates pred_first and pred_second
    def predecessors_variable(gate, pred_first, pred_second):
        assert gate in internal_gates
        assert pred_first in gates and pred_second in gates
        assert pred_first < pred_second < gate
        return variable_number(f's_{gate}_{pred_first}_{pred_second}')

    # k-th output is computed at gate
    def output_gate_variable(k, gate):
        assert k in outputs
        assert gate in gates
        return variable_number(f'g_{k}_{gate}')

    # k-th bit of the truth table of gate
    def gate_value_variable(gate, k):
        assert gate in gates
        return variable_number(f'x_{gate}_{k}')

    clauses = []

    def exactly_one_of(literals):
        return [list(literals)] + [[-a, -b] for (a, b) in combinations(literals, 2)]

    # gate operates on two gates predecessors
    for gate in internal_gates:
        clauses += exactly_one_of([predecessors_variable(gate, a, b) for (a, b) in combinations(range(gate), 2)])

    # each output is computed somewhere
    for h in range(number_of_outputs):
        clauses += exactly_one_of([output_gate_variable(h, gate) for gate in internal_gates])

    # truth values for inputs
    for input_gate in input_gates:
        for t in in_tt:
            if in_tt[t][input_gate] == '1':
                clauses += [[gate_value_variable(input_gate, t)]]
            else:
                assert in_tt[t][input_gate] == '0'
                clauses += [[-gate_value_variable(input_gate, t)]]

    # gate computes the right value
    for gate in internal_gates:
        for first_pred, second_pred in combinations(range(gate), 2):
            for a, b, c in product(range(2), repeat=3):
                for t in in_tt:
                    clauses += [[
                        -predecessors_variable(gate, first_pred, second_pred),
                        (-1 if a else 1) * gate_value_variable(gate, t),
                        (-1 if b else 1) * gate_value_variable(first_pred, t),
                        (-1 if c else 1) * gate_value_variable(second_pred, t),
                        (1 if a else -1) * gate_type_variable(gate, b, c)
                    ]]

    # each output h computes the right value
    for h in outputs:
        for t in out_tt:
            if out_tt[t][h] == '*':
                continue
            for gate in internal_gates:
                clauses += [[
                    -output_gate_variable(h, gate),
                    (1 if out_tt[t][h] == '1' else -1) * gate_value_variable(gate, t)
                ]]

    with open('tmp.cnf', 'w') as file:
        file.write(f'p cnf {len(variables)} {len(clauses)}\n')
        for clause in clauses:
            file.write(f'{" ".join(map(str, clause))} 0\n')
        for v in variables:
            file.write(f'c {v} {variables[v]}\n')

    result = pycosat.solve(clauses, verbose=0)

    # os.system('./minisat_static tmp.cnf tmp.sat > /dev/null 2>&1')
    # with open("tmp.sat") as satfile:
    #     for line in satfile:
    #         if line.split()[0] == 'UNSAT':
    #             result = 'UNSAT'
    #         elif line.split()[0] == "SAT":
    #             pass
    #         else:
    #             result = [int(x) for x in line.split()]

    if result == 'UNSAT':
        return False

    gate_descriptions = {}
    for gate in internal_gates:
        first_pred, second_pred = None, None
        for f, s in combinations(range(gate), 2):
            if predecessors_variable(gate, f, s) in result:
                first_pred, second_pred = f, s
            else:
                assert -predecessors_variable(gate, f, s) in result

        gate_type = []
        for p, q in product(range(2), repeat=2):
            if gate_type_variable(gate, p, q) in result:
                gate_type.append(1)
            else:
                assert -gate_type_variable(gate, p, q) in result
                gate_type.append(0)

        first_pred = input_labels[first_pred] if first_pred in input_gates else first_pred
        second_pred = input_labels[second_pred] if second_pred in input_gates else second_pred
        if isinstance(first_pred, int):
            first_pred = str(shift + first_pred)
        if isinstance(second_pred, int):
            second_pred = str(shift + second_pred)
        gate_descriptions[str(shift + gate)] = (first_pred, second_pred, ''.join(map(str, gate_type)))

    output_gates = []
    for h in outputs:
        for gate in gates:
            if output_gate_variable(h, gate) in result:
                output_gates.append(str(shift + gate))

    return Circuit(input_labels, gate_descriptions, output_gates)
