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
    s = x[0] + 2 * x[1] + 4 * x[2] + 8 * x[3] + 16 * x[4]
    threshold = 16
    if s > threshold:
        return ['*' for _ in range(threshold)]
    else:
        return [1 if s >= t else 0 for t in range(threshold, 0, -1)]
