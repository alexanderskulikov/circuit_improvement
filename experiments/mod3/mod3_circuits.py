# from functions import BooleanFunction
# from itertools import product
from core.circuit_search import CircuitFinder

# n, r, size = 4, 0, 7
# n, r, size = 4, 1, 7
# n, r, size = 4, 2, 6
# n, r, size = 5, 1, 9  # no
# n, r, size = 5, 0, 10  # yes 408 seconds
n, r, size = 5, 2, 10  # yes quick


def mod3(x):
    return [1, ] if sum(x) % 3 == r else [0, ]


finder = CircuitFinder(dimension=n, number_of_gates=size, function=mod3, input_labels=[f'x{i}' for i in range(1, n + 1)])
finder.fix_gate(n, 0, 1, '0001')
finder.fix_gate(n + 1, 2, n, '0110')
for to_gate in range(n + 2, n + size):
    finder.forbid_wire(n, to_gate)


circuit = finder.solve_cnf_formula(verbose=True)
print(circuit)
circuit.draw(detailed_labels=False, file_name=f'mod3_{n}_{r}_{size}_top3and')
