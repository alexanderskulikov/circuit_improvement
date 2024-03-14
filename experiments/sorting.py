from core.circuit_search import *


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


finder = CircuitFinder(dimension=4, function=find_block_for_sum_circuit, number_of_gates=13, input_labels=['z21', 'z24', 'z30', 'z31'])
block = finder.solve_cnf_formula(verbose=True)
block.save_to_file('block10', extension='ckt')


# ckt = Circuit()
# ckt.load_from_file('sort10_size45', extension='ckt')
# verify_sorting_circuit(ckt)
# ckt.save_to_file('sort10_size45', extension='bench')
