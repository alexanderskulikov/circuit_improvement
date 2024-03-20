from core.circuit_search import *
from core.circuit_improvement import *
from functions.sum import *


def verify_sorting_circuit(circuit):
    n = len(circuit.input_labels)
    assert n == len(circuit.outputs)

    tables = circuit.get_truth_tables()
    for value, x in enumerate(product(range(2), repeat=n)):
        for i in range(n):
            assert (tables[circuit.outputs[i]][value] == 1) == (sum(x) >= n - i)


def find_block_for_sum_circuit(x):
    s = x[0] + 2 * x[1] + 4 * x[2] + 8 * x[3]
    threshold = 10
    if s > threshold:
        return ['*' for _ in range(threshold)]
    else:
        return [1 if s >= t else 0 for t in range(threshold, 0, -1)]


# for size in range(16, 3, -1):
#     finder = CircuitFinder(dimension=4, function=find_block_for_sum_circuit, number_of_gates=size,
#                            input_labels=['z19', 'z27', 'z29', 'z30'])
#     block = finder.solve_cnf_formula(verbose=True, solver='cadical195')
#     block.save_to_file(f'block10_size{size}', extension='ckt')

ckt = Circuit()
ckt.load_from_file('improved44', extension='ckt')
print(len(ckt.gates))
verify_sorting_circuit(ckt)
# improve_circuit_iteratively(ckt, max_subcircuit_size=5)
ckt.save_to_file('sort10_size44', extension='ckt')
ckt.save_to_file('sort10_size44', extension='bench')


# ckt = Circuit(input_labels=[f'x{i}' for i in range(1, 15)])
# ckt.outputs = add_sum14_size48(ckt, ckt.input_labels)
# # improve_circuit_iteratively(ckt, max_subcircuit_size=4)
# print(len(ckt.gates))
# ckt.save_to_file('sum14_size48', extension='ckt')
# ckt.save_to_file('sum14_size48', extension='bench')



