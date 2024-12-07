# finding circuits for SUM with a special structure (see Figure 5 of the paper)

from math import ceil, log2
from core.circuit_search import CircuitFinder


def sum_n(x):
    return [(sum(x) >> i) & 1 for i in range(ceil(log2(len(x) + 1)))]


for n, size in ((3, 5), (4, 9), (5, 11), (6, 16)):
    circuit_finder = CircuitFinder(dimension=n, number_of_gates=size,
                                   function=sum_n)
    circuit_finder.fix_gate(n, 0, 1, '0110')
    for k in range(n - 2):
        circuit_finder.fix_gate(n + k + 1, k + 2, n + k, '0110')
    for i in range(1, n):
        for j in range(n, n + size):
            if i + n - 1 != j:
                circuit_finder.forbid_wire(i, j)

    circuit_finder.fix_gate(2 * n - 1, 0, n + 1, '0110')
    circuit_finder.fix_gate(2 * n, n, 2 * n - 1, '0111')
    circuit_finder.fix_gate(2 * n + 1, n + 1, 2 * n, '0110')

    circuit = circuit_finder.solve_cnf_formula(verbose=1)
    circuit.draw(f'sum{n}', detailed_labels=True)