from core.circuit import *
from core.circuit_search import *
from functions.sum import *
from itertools import product
from mip import *
from tqdm import tqdm
from os import listdir


# checks whether a given gate computes [w0x0+w1x1+...+w(n-1)x(n-1) >= t] for some
# integers w0, w1, ..., w(n-1), t
def check_gate_for_weighted_threshold(circuit, gate):
    assert gate in circuit.gates

    n = len(circuit.input_labels)

    model = Model(sense=MINIMIZE)
    model.emphasis = 1
    model.verbose = False

    t = model.add_var(var_type=INTEGER, name='t', lb=-10)
    w = [model.add_var(var_type=INTEGER, name=f'w{i}', lb=-10) for i in range(n)]

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

    model.verbose = 0
    # model += t >= 0
    # model.objective = t
    status = model.optimize(max_seconds=5)

    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        return [int(w[i].x) for i in range(n)] + [int(t.x), ]
    else:
        return None


def weighted_threshold(x):
    weights, t = [1, 1, -10, 3, 1], 3
    assert len(x) == len(weights)
    return [1 if sum(weights[i] * x[i] for i in range(len(x))) >= t else 0, ]


# finder = CircuitFinder(dimension=5, number_of_gates=8, function=weighted_threshold)
# ckt = finder.solve_cnf_formula()
# # print(ckt)

for file_name in sorted(listdir('./circuits/')):
    if file_name == '.images':
        continue

    print(f'Processing {file_name}')
    ckt = Circuit()
    ckt.load_from_file(file_name[:-6], extension='bench')
    ckt.normalize(basis='xaig')

    gates = list(reversed(list(nx.topological_sort(ckt.construct_graph()))))
    for gate in tqdm(gates):
        if gate in ckt.input_labels:
            continue
        wt = check_gate_for_weighted_threshold(ckt, gate)
        if wt and len([a for a in wt if a != 0]) >= 5:
            description = '+'.join([f'{wt[i]}*x{i}' for i in range(len(wt) - 1) if wt[i] != 0])
            print(f'Gate {gate} computes a weighted sum: [{description}>={wt[-1]}]')
