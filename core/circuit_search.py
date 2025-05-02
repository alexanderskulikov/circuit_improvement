from core.circuit import Circuit
from itertools import combinations, product, permutations, chain
from core.functions2 import BooleanFunction
from datetime import datetime
import os
import pycosat
import sys
from timeit import default_timer as timer
from pysat.formula import CNF
from pysat.solvers import Solver
from threading import Timer

precalc_inv_clauses = dict()

class CircuitFinder:
    def __init__(self, dimension, number_of_gates, input_labels=None,
                 input_truth_tables=None, output_truth_tables=None,
                 function=None, basis='xaig'):
        self.dimension = dimension

        if function is not None:
            assert input_truth_tables is None
            assert output_truth_tables is None

            output_num = len(function([0] * self.dimension))
            self.output_truth_tables = [[] for _ in range(output_num)]
            for x in product(range(2), repeat=self.dimension):
                x_output = function(x)
                assert len(x_output) == output_num
                for i in range(output_num):
                    self.output_truth_tables[i].append(x_output[i])

            self.output_truth_tables = [''.join(map(str, t)) for t in self.output_truth_tables]
        else:
            assert output_truth_tables is not None
            self.output_truth_tables = output_truth_tables

        if input_truth_tables is not None:
            assert input_labels is not None
            assert len(input_labels) == len(input_truth_tables)
            assert all(len(table) == 1 << dimension for table in input_truth_tables)
            assert all(all(symbol in '01' for symbol in table) for table in input_truth_tables)
        else:
            if input_labels is None:
                input_labels = list(range(dimension))
            input_truth_tables = [[] for _ in range(dimension)]
            for t in range(1 << dimension):
                for i in range(dimension):
                    input_truth_tables[i].append((t >> (dimension - 1 - i)) & 1)
            input_truth_tables = [''.join(map(str, t)) for t in input_truth_tables]

        self.input_labels = input_labels
        self.input_truth_tables = input_truth_tables
        self.number_of_gates = number_of_gates
        # self.is_normal = all(table[0] != '1' for table in self.output_truth_tables)
        # self.is_normal = False

        assert all(len(table) == 1 << dimension for table in self.output_truth_tables)
        assert all(all(symbol in "01*" for symbol in table) for table in self.output_truth_tables)

        number_of_input_gates = len(self.input_truth_tables)
        number_of_outputs = len(self.output_truth_tables)

        self.input_gates = list(range(number_of_input_gates))
        self.internal_gates = list(range(number_of_input_gates, number_of_input_gates + number_of_gates))
        self.gates = list(range(number_of_input_gates + number_of_gates))
        self.outputs = list(range(number_of_outputs))

        assert all(str(gate) not in self.input_labels for gate in self.internal_gates)

        assert basis in ('xaig', 'aig')
        self.forbidden_operations = [] if basis == 'xaig' else ['0110', '1001']

        self.clauses = []
        self.cnt_variables = 1
        # self.cnt_variables_by_type = precalc_cnt_variables_by_type[(self.dimension, len(self.outputs), number_of_input_gates + number_of_gates)]
        self.cnt_variables_by_type = []

        # output of gate on inputs (p, q)
        self.cnt_variables_by_type.append(0)
        for p in range(2):
            for q in range(2):
                for gate in range(number_of_input_gates + number_of_gates):
                    self.cnt_variables_by_type[0] += 1
                    self.cnt_variables += 1

        # gate operates on gates first_pred and second_pred
        self.cnt_variables_by_type.append(0)
        for gate in range(number_of_input_gates + number_of_gates):
            for first_pred in range(number_of_input_gates + number_of_gates):
                for second_pred in range(number_of_input_gates + number_of_gates):
                    self.cnt_variables_by_type[1] += 1
                    self.cnt_variables += 1

        # h-th output is computed at gate
        self.cnt_variables_by_type.append(0)
        for h in range(len(self.outputs)):
            for gate in range(number_of_input_gates + number_of_gates):
                self.cnt_variables_by_type[2] += 1
                self.cnt_variables += 1

        # t-th bit of the truth table of gate
        self.cnt_variables_by_type.append(0)
        for gate in range(number_of_input_gates + number_of_gates):
            for t in range(1 << self.dimension):
                self.cnt_variables_by_type[3] += 1
                self.cnt_variables += 1

        self.init_default_cnf_formula()

    # output of gate on inputs (p, q)
    def gate_type_variable(self, gate, p, q):
        assert 0 <= p <= 1 and 0 <= q <= 1
        assert gate in self.gates
        # return self.variable_number(f'f_{gate}_{p}_{q}')
        # return self.variable_number((0,gate, p, q))
        return 1 + p * (2 * len(self.gates)) + q * len(self.gates) + gate
        # return 1 + (p + 1) * (q + 1) * (gate + 1)

    # gate operates on gates first_pred and second_pred
    def predecessors_variable(self, gate, first_pred, second_pred):
        assert gate in self.internal_gates
        assert first_pred in self.gates and second_pred in self.gates
        assert first_pred < second_pred < gate
        # return self.variable_number(f's_{gate}_{first_pred}_{second_pred}')
        return 1 + self.cnt_variables_by_type[0] + gate * (len(self.gates) ** 2) + first_pred * len(self.gates) + second_pred
        # return self.variable_number((1,gate,first_pred,second_pred))
        # return 1 + 2 * 2 * self.internal_gates + (gate + 1) * (first_pred + 1) * ()

    # h-th output is computed at gate
    def output_gate_variable(self, h, gate):
        assert h in self.outputs
        assert gate in self.gates
        # return self.variable_number(f'g_{h}_{gate}')
        return 1 + self.cnt_variables_by_type[0] + self.cnt_variables_by_type[1] + h * len(self.gates) + gate
        # return self.variable_number((2,h,gate,-1))

    # t-th bit of the truth table of gate
    def gate_value_variable(self, gate, t):
        assert gate in self.gates
        assert 0 <= t < 1 << self.dimension
        # return self.variable_number(f'x_{gate}_{t}')
        return 1 + self.cnt_variables_by_type[0] + self.cnt_variables_by_type[1] + self.cnt_variables_by_type[2] + gate * (1 << self.dimension) + t
        # return self.variable_number((3,gate,t,-1))

    def at_most_one_of(self, literals):
        k = len(literals)
        if k == 0:
            return []
        if k == 1:
            return [[literals[0]]]

        clauses = []

        clauses.append([-literals[0], self.cnt_variables + 1])
        for i in range(2, k):
            clauses.append([-literals[i - 1], self.cnt_variables + i])
            clauses.append([-(self.cnt_variables + i - 1), self.cnt_variables + i])

        for i in range(2, k + 1):
            clauses.append([-literals[i - 1], -(self.cnt_variables + i - 1)])
        self.cnt_variables += (k - 1)
        return clauses

    def exactly_one_of(self, literals):
        k = len(literals)
        if k == 0:
            return []
        if k == 1:
            return [[literals[0]]]
        return [list(literals)] + self.at_most_one_of(literals)

        # out = [list(literals)] + [[-literals[i], self.cnt_variables + i] for i in range(1, len(literals))] + \
        #     [[-(literals[0] if i == 1 else self.cnt_variables + i - 1), self.cnt_variables + i] for i in range(1, len(literals))] + \
        #     [[-(literals[0] if i == 1 else self.cnt_variables + i - 1), -literals[i]] for i in range(1, len(literals))]
        # self.cnt_variables += len(literals)
        # return out
        return [list(literals)] + [[-a, -b] for (a, b) in combinations(literals, 2)]

    def init_default_cnf_formula(self):

        inv_on_sizes_clauses = []
        inv_on_func_clauses = []
        params = (self.dimension, len(self.outputs), self.dimension + len(self.internal_gates))

        if params not in precalc_inv_clauses:
            precalc_inv_clauses[params] = []
            # gate operates on two gates predecessors
            for gate in self.internal_gates:
                precalc_inv_clauses[params].extend(self.exactly_one_of([self.predecessors_variable(gate, a, b) for (a, b) in combinations(range(gate), 2)]))

            # each output is computed somewhere
            for h in range(len(self.outputs)):
                precalc_inv_clauses[params].extend(self.exactly_one_of([self.output_gate_variable(h, gate) for gate in self.internal_gates]))
            precalc_inv_clauses[params].extend(self.exactly_one_of([self.output_gate_variable(h, self.internal_gates[-1]) for h in range(len(self.outputs))]))

            # each gate computes a non-degenerate function (0, 1, x, -x, y, -y)
            for gate in self.internal_gates:
                precalc_inv_clauses[params].append([self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1), self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1)])
                precalc_inv_clauses[params].append([-self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1), -self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1)])

                precalc_inv_clauses[params].append([self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1), -self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1)])
                precalc_inv_clauses[params].append([-self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1), self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1)])

                precalc_inv_clauses[params].append([self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1), self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1)])
                precalc_inv_clauses[params].append([-self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1), -self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1)])

            # each gate computes an allowed operation
            for gate in self.internal_gates:
                for op in self.forbidden_operations:
                    # assert len(op) == 4 and all(int(b) in (0, 1) for b in op)
                    clause = []
                    for i in range(4):
                        clause.append((-1 if int(op[i]) == 1 else 1) * self.gate_type_variable(gate, i // 2, i % 2))
                    precalc_inv_clauses[params].append(clause)

            for gate in range(self.internal_gates[-1] + 1):
                lit = []
                if gate >= self.internal_gates[0]:
                    for h in range(len(self.outputs)):
                       lit.append(self.output_gate_variable(h, gate))
                for j in range(gate + 1, self.internal_gates[-1] + 1):
                    for k in range(max(j + 1, self.internal_gates[0]), self.internal_gates[-1] + 1):
                        lit.append(self.predecessors_variable(k, gate, j))
                for j in range(gate):
                    for k in range(max(gate + 1, self.internal_gates[0]), self.internal_gates[-1] + 1):
                        lit.append(self.predecessors_variable(k, j, gate))
                precalc_inv_clauses[params].append(lit)
            #
            for gate, gate_ in combinations(self.internal_gates, 2):
                for j, k in combinations(range(gate), 2):
                    precalc_inv_clauses[params].append([-self.predecessors_variable(gate, j, k), -self.predecessors_variable(gate_, j, gate)])
                    precalc_inv_clauses[params].append([-self.predecessors_variable(gate, j, k), -self.predecessors_variable(gate_, k, gate)])

            for gate in self.internal_gates:
                if gate == self.internal_gates[-1]:
                    continue
                for j, k in combinations(range(gate), 2):
                    for j_ in range(j):
                        precalc_inv_clauses[params].append([-self.predecessors_variable(gate, j, k), -self.predecessors_variable(gate + 1, j_, k)])
                    for j_, k_ in combinations(range(k), 2):
                        precalc_inv_clauses[params].append([-self.predecessors_variable(gate, j, k), -self.predecessors_variable(gate + 1, j_, k_)])

                # for j_, j, k in combinations(range(gate), 3):
                #     precalc_inv_clauses[params].append([-self.predecessors_variable(gate, j, k), -self.predecessors_variable(gate + 1, j_, k)])
                # for j_, k_, k in combinations(range(gate), 3):
                #     for j in range(k):
                #         precalc_inv_clauses[params].append([-self.predecessors_variable(gate, j, k), -self.predecessors_variable(gate + 1, j_, k_)])

            # gate computes the right value
            for t in range(1 << self.dimension):
                # ch = True
                # for g in range(len(self.output_truth_tables)):
                #     if self.output_truth_tables[g][t] != '*':
                #         ch = False
                #         break
                # if ch:
                #     continue

                for a, b, c in product(range(2), repeat=3):
                    mul_a, mul_b, mul_c = (-1 if a else 1), (-1 if b else 1), (-1 if c else 1)
                    for gate in self.internal_gates:
                        for first_pred, second_pred in combinations(range(gate), 2):
                            precalc_inv_clauses[params].append([
                                -self.predecessors_variable(gate, first_pred, second_pred),
                                mul_a * self.gate_value_variable(gate, t),
                                mul_b * self.gate_value_variable(first_pred, t),
                                mul_c * self.gate_value_variable(second_pred, t),
                                -mul_a * self.gate_type_variable(gate, b, c)
                            ])

            # for i in range(len(self.internal_gates) - 1):
            #     g, g2 = self.internal_gates[i], self.internal_gates[i + 1]
            #     # t0 — первый индекс (можно взять t=0)
            #     precalc_inv_clauses[params].append([
            #         -self.gate_value_variable(g, 0),
            #         self.gate_value_variable(g2, 0)
            #     ])

        # for p, q in combinations(self.input_gates, 2):
        #     ch = True
        #     for t in range(1 << self.dimension):
        #         if t & (1 << p) and not t & (1 << q):
        #             tn = t - (1 << p) + (1 << q)
        #             for g in range(len(self.output_truth_tables)):
        #                 if self.output_truth_tables[g][t] != '*' and self.output_truth_tables[g][tn] != '*' and self.output_truth_tables[g][t] != self.output_truth_tables[g][tn]:
        #                     ch = False
        #                     break
        #             if not ch:
        #                 break
        #     if ch:
        #         for j in range(q):
        #             if j == p:
        #                 continue
        #             for i in self.internal_gates:
        #                 claus = [-self.predecessors_variable(i, j, q)]
        #                 for i_ in range(self.internal_gates[0], i):
        #                     for j_, k_ in combinations(range(i_), 2):
        #                         if j_ == p or k_ == p:
        #                             claus.append(self.predecessors_variable(i_, j_, k_))
        #                 self.clauses.append(claus)


        # truth values for inputs
        for t in range(1 << self.dimension):
            ch = True
            for g in range(len(self.output_truth_tables)):
                if self.output_truth_tables[g][t] != '*':
                    ch = False
                    break
            if ch:
                continue

            for input_gate in self.input_gates:
                if self.input_truth_tables[input_gate][t] == '1':
                    inv_on_func_clauses.append([self.gate_value_variable(input_gate, t)])
                else:
                    assert self.input_truth_tables[input_gate][t] == '0'
                    inv_on_func_clauses.append([-self.gate_value_variable(input_gate, t)])

        for h in self.outputs:
            for t in range(1 << self.dimension):
                if self.output_truth_tables[h][t] == '*':
                    continue
                mul = (1 if self.output_truth_tables[h][t] == '1' else -1)
                for gate in self.internal_gates:
                    inv_on_func_clauses.append([
                        -self.output_gate_variable(h, gate),
                        mul * self.gate_value_variable(gate, t)
                    ])
        self.clauses = chain(precalc_inv_clauses[params], inv_on_func_clauses)
        # return chain(precalc_inv_clauses[params], inv_on_func_clauses)
        # return self.clauses

    # returns: a circuit if found; False if there is no circuit; None if a SAT solver is interrupted by the time limit
    def solve_cnf_formula(self, solver_name='glucose421', verbose=1, time_limit=None):
        global interrupt
        if verbose:
            print(f'Solving a CNF formula, '
                  f'number of gates: {self.number_of_gates}, '
                  f'solver: {solver_name}, '
                  f'time_limit: {time_limit}, '
                  f'current time: {datetime.now()}'
            )

        # corner case: looking for a circuit of size 0
        if self.number_of_gates == 0:
            for tt in self.output_truth_tables:
                f = BooleanFunction(tt)
                if not f.is_constant() and not f.is_any_literal():
                    return False

            return Circuit()

        # self.finalize_cnf_formula()

        if verbose:
            print(f'Running {solver_name}')

        solver = Solver(name=solver_name, bootstrap_with=self.clauses)

        if time_limit:
            def interrupt(s):
                s.interrupt()

            solver_timer = Timer(time_limit, interrupt, [solver])
            solver_timer.start()
            solver.solve_limited(expect_interrupt=True)
        else:
            solver.solve()

        if verbose:
            print(f'Done solving, current time: {datetime.now()}')

        model = solver.get_model()
        interrupted = solver.get_status() is None
        solver.delete()

        if interrupted:
            for gate in self.internal_gates[1:]:
                k = gate - 1
                lit = []
                for j in range(gate - 1):
                    lit.append(self.predecessors_variable(gate, j, k))
                self.exactly_one_of(lit)

            solver = Solver(name=solver_name, bootstrap_with=self.clauses)
            solver_timer = Timer(time_limit, interrupt, [solver])
            solver_timer.start()
            solver.solve_limited(expect_interrupt=True)

            model2 = solver.get_model()
            interrupted2 = solver.get_status() is None
            solver.delete()
            if interrupted2:
                return None
            if not model2:
                return False
        if not model:
            return False

        gate_descriptions = {}
        for gate in self.internal_gates:
            first_predecessor, second_predecessor = None, None
            for f, s in combinations(range(gate), 2):
                if self.predecessors_variable(gate, f, s) in model:
                    first_predecessor, second_predecessor = f, s
                else:
                    assert -self.predecessors_variable(gate, f, s) in model

            gate_type = []
            for p, q in product(range(2), repeat=2):
                if self.gate_type_variable(gate, p, q) in model:
                    gate_type.append(1)
                else:
                    assert -self.gate_type_variable(gate, p, q) in model
                    gate_type.append(0)

            first_predecessor = self.input_labels[first_predecessor] if first_predecessor in self.input_gates else 's' + str(first_predecessor)
            second_predecessor = self.input_labels[second_predecessor] if second_predecessor in self.input_gates else 's' + str(second_predecessor)
            gate_descriptions['s' + str(gate)] = (first_predecessor, second_predecessor, ''.join(map(str, gate_type)))

        output_gates = []
        for h in self.outputs:
            for gate in self.gates:
                if self.output_gate_variable(h, gate) in model:
                    output_gates.append('s' + str(gate))

        return Circuit(self.input_labels, gate_descriptions, output_gates)

    def finalize_cnf_formula(self):
        # if self.is_normal:
        #     for gate in self.internal_gates:
        #         self.clauses += [[-self.gate_type_variable(gate, 0, 0)]]
        pass

    # The following method allows to further restrict the internal structure of a circuit.
    # Only use it if you know what you are doing.
    # The parameters gate, first_predecessor, second_predecessor are gate indices
    # (rather than labels).
    def fix_gate(self, gate, first_predecessor=None, second_predecessor=None, gate_type=None):
        assert gate in self.internal_gates

        if first_predecessor is not None and second_predecessor is not None:
            assert first_predecessor in self.gates
            assert second_predecessor in self.gates
            self.clauses += [[self.predecessors_variable(gate, first_predecessor, second_predecessor)]]
        else:
            if first_predecessor is not None:
                assert first_predecessor in self.gates
                assert not second_predecessor
                for a, b in combinations(range(gate), 2):
                    if a != first_predecessor and b != first_predecessor:
                        self.clauses += [[-self.predecessors_variable(gate, a, b)]]

        if gate_type:
            assert isinstance(gate_type, str) and len(gate_type) == 4

            # if gate_type[0] != '0':
            #     self.is_normal = False

            for a, b in product(range(2), repeat=2):
                bit = int(gate_type[2 * a + b])
                assert bit in range(2)
                self.clauses += [[(1 if bit else -1) * self.gate_type_variable(gate, a, b)]]

    def forbid_wire(self, from_gate, to_gate):
        assert from_gate in self.gates
        assert to_gate in self.internal_gates
        assert from_gate < to_gate

        for other in self.gates:
            if other < to_gate and other != from_gate:
                self.clauses += [[-self.predecessors_variable(to_gate, min(other, from_gate), max(other, from_gate))]]


# hist = [[[[dict() for ____ in range((1 << 9))] for ___ in range((1 << 9))] for __ in range(9)] for _ in range(9)]
hist = dict()
def find_circuit(dimension, number_of_gates, input_labels, input_truth_tables, output_truth_tables, basis='xaig', verbose=0, time_limit=None):
    # print("find circuit", dimension, number_of_gates, input_truth_tables, output_truth_tables)
    # cnt_0, cnt_1 = 0, 0
    # for g in range(len(output_truth_tables)):
    #     cnt_0 += output_truth_tables[g].count('0')
    #     cnt_1 += output_truth_tables[g].count('1')
    # if tuple(output_truth_tables) in hist[dimension][number_of_gates][cnt_0][cnt_1]:
    #     return hist[dimension][number_of_gates][cnt_0][cnt_1][tuple(output_truth_tables)]

    if (number_of_gates, tuple(output_truth_tables)) in hist:
        # print("HARD MEMOIZATION +1")
        return hist[(number_of_gates, tuple(output_truth_tables))]
    circuit_finder = CircuitFinder(dimension=dimension,
                                   number_of_gates=number_of_gates,
                                   input_labels=input_labels,
                                   input_truth_tables=input_truth_tables,
                                   output_truth_tables=output_truth_tables,
                                   basis=basis)
    out = circuit_finder.solve_cnf_formula(verbose=verbose, time_limit=time_limit)
    if out is None or out == False:
        # hist[dimension][number_of_gates][cnt_0][cnt_1][tuple(output_truth_tables)] = out
        hist[(number_of_gates, tuple(output_truth_tables))] = out
    return out








if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print('Usage:', sys.argv[0], 'n r truthtable1 ... truthtablem')
        print('(n is the number of inputs, r is the number of gates, m is the number of outputs)')
        sys.exit(0)

    number_of_inputs = int(sys.argv[1])
    number_of_gates = int(sys.argv[2])
    output_truth_tables = sys.argv[3:]

    start = timer()
    circuit = find_circuit(dimension=number_of_inputs,
                           number_of_gates=number_of_gates,
                           output_truth_tables=output_truth_tables,
                           input_labels=None,
                           input_truth_tables=None,
                           basis='xaig')
    end = timer()

    if not circuit:
        print('There is no such circuit, sorry')
    else:
        print('Circuit found!\n')
        print(circuit)
    print(f'Time: {end-start:.2f} seconds')
