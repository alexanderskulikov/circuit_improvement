# looking for optimal circuits where every variable feeds xors only

from core.circuit import Circuit
from itertools import combinations, product, permutations
from core.functions2 import BooleanFunction
from datetime import datetime
import os
import pycosat
import sys
from timeit import default_timer as timer
from pysat.formula import CNF
from pysat.solvers import Solver
from threading import Timer


class MOD3XorsCircuitFinder:
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
        self.variables = {'dummy': 0}

        self.init_default_cnf_formula()

    def variable_number(self, name):
        if name in self.variables:
            return self.variables[name]

        self.variables[name] = len(self.variables) + 1
        return self.variables[name]

    # output of gate on inputs (p, q)
    def gate_type_variable(self, gate, p, q):
        assert 0 <= p <= 1 and 0 <= q <= 1
        assert gate in self.gates
        return self.variable_number(f'f_{gate}_{p}_{q}')

    # gate operates on gates first_pred and second_pred
    def predecessors_variable(self, gate, first_pred, second_pred):
        assert gate in self.internal_gates
        assert first_pred in self.gates and second_pred in self.gates
        assert first_pred < second_pred < gate
        return self.variable_number(f's_{gate}_{first_pred}_{second_pred}')

    # whether gate has a xor-type
    def is_xor_variable(self, gate):
        return self.variable_number(f'isxor_{gate}')

    # h-th output is computed at gate
    def output_gate_variable(self, h, gate):
        assert h in self.outputs
        assert gate in self.gates
        return self.variable_number(f'g_{h}_{gate}')

    # t-th bit of the truth table of gate
    def gate_value_variable(self, gate, t):
        assert gate in self.gates
        assert 0 <= t < 1 << self.dimension
        return self.variable_number(f'x_{gate}_{t}')

    def init_default_cnf_formula(self):
        def exactly_one_of(literals):
            return [list(literals)] + [[-a, -b] for (a, b) in combinations(literals, 2)]

        # gate operates on two gates predecessors
        for gate in self.internal_gates:
            self.clauses += exactly_one_of([self.predecessors_variable(gate, a, b) for (a, b) in combinations(range(gate), 2)])

        # each output is computed somewhere
        for h in range(len(self.outputs)):
            self.clauses += exactly_one_of([self.output_gate_variable(h, gate) for gate in self.internal_gates])

        # truth values for inputs
        for input_gate in self.input_gates:
            for t in range(1 << self.dimension):
                col = [''.join(map(str, [self.output_truth_tables[g][t] for g in range(len(self.output_truth_tables))]))][0]
                if col.count('*') == len(col):
                    continue

                if self.input_truth_tables[input_gate][t] == '1':
                    self.clauses += [[self.gate_value_variable(input_gate, t)]]
                else:
                    assert self.input_truth_tables[input_gate][t] == '0'
                    self.clauses += [[-self.gate_value_variable(input_gate, t)]]

        # gate computes the right value
        for gate in self.internal_gates:
            for first_pred, second_pred in combinations(range(gate), 2):
                for a, b, c in product(range(2), repeat=3):
                    for t in range(1 << self.dimension):
                        col = [''.join(map(str, [self.output_truth_tables[g][t] for g in range(len(self.output_truth_tables))]))][0]
                        if col.count('*') == len(col):
                            continue

                        self.clauses += [[
                            -self.predecessors_variable(gate, first_pred, second_pred),
                            (-1 if a else 1) * self.gate_value_variable(gate, t),
                            (-1 if b else 1) * self.gate_value_variable(first_pred, t),
                            (-1 if c else 1) * self.gate_value_variable(second_pred, t),
                            (1 if a else -1) * self.gate_type_variable(gate, b, c)
                        ]]

        for h in self.outputs:
            for t in range(1 << self.dimension):
                if self.output_truth_tables[h][t] == '*':
                    continue

                for gate in self.internal_gates:
                    self.clauses += [[
                        -self.output_gate_variable(h, gate),
                        (1 if self.output_truth_tables[h][t] == '1' else -1) * self.gate_value_variable(gate, t)
                    ]]

        # each gate computes a non-degenerate function (0, 1, x, -x, y, -y)
        for gate in self.internal_gates:
            self.clauses += [[self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1), self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1)]]
            self.clauses += [[-self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1), -self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1)]]

            self.clauses += [[self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1), -self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1)]]
            self.clauses += [[-self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1), self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1)]]

            self.clauses += [[self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1), self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1)]]
            self.clauses += [[-self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1), -self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1)]]

        # each gate computes an allowed operation
        for gate in self.internal_gates:
            for op in self.forbidden_operations:
                assert len(op) == 4 and all(int(b) in (0, 1) for b in op)
                clause = []
                for i in range(4):
                    clause.append((-1 if int(op[i]) == 1 else 1) * self.gate_type_variable(gate, i // 2, i % 2))
                self.clauses.append(clause)

        # experimental!
        for gate in self.internal_gates:
            # self.clauses += [[self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1),
            #                   -self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1),
            #                   self.is_xor_variable(gate)]]
            # self.clauses += [[-self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1),
            #                   self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1),
            #                   self.is_xor_variable(gate)]]

            # ++++
            self.clauses += [[self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1),
                              self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # +++-
            self.clauses += [[self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1),
                              self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # ++-+
            self.clauses += [[self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1),
                              -self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # ++--
            self.clauses += [[self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1),
                              -self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # +-++
            self.clauses += [[self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1),
                              self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # +-+-
            self.clauses += [[self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1),
                              self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # +--+ xor!
            self.clauses += [[self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1),
                              -self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1),
                              self.is_xor_variable(gate)]]
            # +---
            self.clauses += [[self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1),
                              -self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # -+++
            self.clauses += [[-self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1),
                              self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # -++- xor!
            self.clauses += [[-self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1),
                              self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1),
                              self.is_xor_variable(gate)]]
            # -+-+
            self.clauses += [[-self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1),
                              -self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # -+--
            self.clauses += [[-self.gate_type_variable(gate, 0, 0), self.gate_type_variable(gate, 0, 1),
                              -self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # --++
            self.clauses += [[-self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1),
                              self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # --+-
            self.clauses += [[-self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1),
                              self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # ---+
            self.clauses += [[-self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1),
                              -self.gate_type_variable(gate, 1, 0), self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]
            # ----
            self.clauses += [[-self.gate_type_variable(gate, 0, 0), -self.gate_type_variable(gate, 0, 1),
                              -self.gate_type_variable(gate, 1, 0), -self.gate_type_variable(gate, 1, 1),
                              -self.is_xor_variable(gate)]]




        for gate, other_predecessor, input_gate in product(self.internal_gates, self.gates, self.input_gates):
            if other_predecessor != input_gate and other_predecessor < gate:
                # print(gate, other_predecessor, input_gate)
                self.clauses += [[
                    -self.predecessors_variable(gate, min(input_gate, other_predecessor), max(input_gate, other_predecessor)),
                    self.is_xor_variable(gate)
                ]]

        return self.clauses

    def save_cnf_formula_to_file(self, file_name):
        self.finalize_cnf_formula()

        with open(file_name, 'w') as file:
            file.write(f'p cnf {len(self.variables)} {len(self.clauses)}\n')
            for clause in self.clauses:
                file.write(f'{" ".join(map(str, clause))} 0\n')
            for v in self.variables:
                file.write(f'c {v} {self.variables[v]}\n')

    # returns: a circuit if found; False if there is no circuit; None if a SAT solver is interrupted by the time limit
    def solve_cnf_formula(self, solver_name='glucose421', verbose=1, time_limit=None):
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

        self.finalize_cnf_formula()

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
            return None
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


if __name__ == '__main__':
    # for n, r in product(range(3, 6), range(3)):
    for n, r in ((4, 0), ):
        print(f'n={n}, r={r}')

        def mod3(x):
            return [1, ] if sum(x) % 3 == r else [0, ]

        finder = MOD3XorsCircuitFinder(
            dimension=n,
            number_of_gates=3 * n - 5 - (1 if (n + r) % 3 == 0 else 0),
            function=mod3,
            input_labels=[f'x{i}' for i in range(1, n + 1)]
        )
        circuit = finder.solve_cnf_formula(verbose=False)
        if circuit:
            # circuit.draw(f'mod3_n{n}_r{r}_xor_vars.png')
            circuit.save_to_file(f'mod3_n{n}_r{r}_xor_vars.ckt')
        else:
            print('there is no such circuit')

