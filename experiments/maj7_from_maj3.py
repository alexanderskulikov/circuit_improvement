from itertools import combinations, product
from pysat.card import *
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver
from tqdm import tqdm

n, nof_gates = 3, 1

input_assignments = list(product((0, 1), repeat=n))
inputs_gates = list(range(n))
internal_gates = list(range(n, n + nof_gates))
all_gates = list(range(n + nof_gates))
output_gate = n + nof_gates - 1

id_pool = IDPool()


def var_gate_value(gate, input_assignment):
    assert gate in all_gates and input_assignment in input_assignments
    return id_pool.id(('value', gate, input_assignment))


def var_wire(internal_gate, from_gate, wire_id):
    assert internal_gate in internal_gates and from_gate in all_gates and wire_id in range(3)
    assert from_gate < internal_gate
    return id_pool.id(('wire', internal_gate, from_gate, wire_id))


def var_wire_sign(internal_gate, wire_id):
    assert internal_gate in internal_gates and wire_id in range(3)
    return id_pool.id(('wire_sign', internal_gate, wire_id))


# if (x1=c1 and x2=c2 and ... and xk=ck) then (x=c)
def if_then_clause(varvalues, varvalue):
    return [(1 - 2 * value) * var for var, value in varvalues] + [(2 * varvalue[1] - 1) * varvalue[0], ]


cnf_formula = CNF()


# the circuit computes MAJ_n
for assignment in input_assignments:
    cnf_formula.append([(1 if sum(assignment) > n / 2 else -1) * var_gate_value(output_gate, assignment)])

# for every internal gate, there are three incoming wires
for internal_gate, wire_id in product(internal_gates, range(3)):
    possible_predecessors = list(range(internal_gate))
    lits = [var_wire(internal_gate, from_gate, wire_id) for from_gate in possible_predecessors]
    cnf_formula.append(lits)
    for l1, l2 in combinations(lits, 2):
        cnf_formula.append([-l1, -l2])

# each gate computes the right value
print('Crafting a formula:')
for gate, assignment in tqdm(list(product(all_gates, input_assignments))):
    if gate in inputs_gates:
        cnf_formula.append([(1 if assignment[gate] else -1) * var_gate_value(gate, assignment)])
    else:
        assert gate in internal_gates
        possible_predecessors = list(range(gate))
        for p0, p1, p2 in product(possible_predecessors, repeat=3):
            for s0, s1, s2 in product(range(2), repeat=3):
                for v0, v1, v2 in product(range(2), repeat=3):
                    gate_value = 1 if ((1 if v0 == s0 else 0) + (1 if v1 == s1 else 0) + (1 if v2 == s2 else 0)) >= 2 else 0

                    cnf_formula.append(if_then_clause([
                        (var_wire(gate, from_gate=p0, wire_id=0), 1),
                        (var_wire(gate, from_gate=p1, wire_id=1), 1),
                        (var_wire(gate, from_gate=p2, wire_id=2), 1),
                        (var_wire_sign(gate, wire_id=0), s0),
                        (var_wire_sign(gate, wire_id=1), s1),
                        (var_wire_sign(gate, wire_id=2), s2),
                        (var_gate_value(gate=p0, input_assignment=assignment), v0),
                        (var_gate_value(gate=p1, input_assignment=assignment), v1),
                        (var_gate_value(gate=p2, input_assignment=assignment), v2),
                    ], (gate, gate_value)))


solver = Solver(bootstrap_with=cnf_formula)
# if solver.solve():
#     print(solver.get_model())
# else:
#     print('Unsatisfiable')
a = {}

