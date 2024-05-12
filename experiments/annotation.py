from core.circuit import *
from core.circuit_search import *
from functions.sum import *
from itertools import product
from mip import *


# checks whether a given gate computes [w0x0+w1x1+...+w(n-1)x(n-1) >= t] for some
# integers w0, w1, ..., w(n-1), t
def check_gate_for_weighted_threshold(circuit, gate):
    assert gate in circuit.gates

    n = len(circuit.input_labels)

    model = Model()
    model.emphasis = 1
    model.verbose = False

    t = model.add_var(var_type=INTEGER, name='t', lb=-1000, ub=1000)
    w = [model.add_var(var_type=INTEGER, name=f'w{i}', lb=-1000, ub=1000) for i in range(n)]

    all_truth_tables = circuit.get_truth_tables()
    gate_truth_table = all_truth_tables[gate]

    for i, x in enumerate(product((0, 1), repeat=n)):
        value = gate_truth_table[i]

        if value == 1:
            model += xsum(w[i] * x[i] for i in range(n)) >= t
            pass
        else:
            assert value == 0
            model += xsum(w[i] * x[i] for i in range(n)) <= t - 1

    # print('Start optimizing...')
    model.verbose = False
    status = model.optimize()
    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        return [w[i].x for i in range(n)] + [t.x, ]
    else:
        return None


def weighted_threshold(x):
    weights, t = [1, 1, -10, 3, 1], 3
    assert len(x) == len(weights)
    return [1 if sum(weights[i] * x[i] for i in range(len(x))) >= t else 0, ]


# finder = CircuitFinder(dimension=5, number_of_gates=8, function=weighted_threshold)
# ckt = finder.solve_cnf_formula()
# # print(ckt)

ckt = Circuit()
ckt.load_from_file('ex01', extension='bench')

for gate in reversed(list(nx.topological_sort(ckt.construct_graph()))):
    if gate in ckt.input_labels:
        continue
    print(f'Processing gate {gate}...')
    wt = check_gate_for_weighted_threshold(ckt, gate)
    if wt:
        print(f'Gate {gate} computes a weighted sum: {wt}')
