from circuit_search import CircuitFinder
from itertools import product


def majority(x):
    return [1, ] if sum(x) >= len(x) / 2 else [0, ]


# optimal values: (3, 4), (4, 7), (5, 10)[16 sec], (6, 15)[??? sec]
n, gates = 7, 20
binary_operations = [''.join(op) for op in product('01', repeat=4)]
basis = ('0001', '0111')
forbidden_operations = [op for op in binary_operations if op not in basis]

finder = CircuitFinder(
    dimension=n,
    number_of_gates=gates,
    function=majority,
    input_labels=[f'x{i}' for i in range(1, n + 1)],
    forbidden_operations=forbidden_operations
)

circuit = finder.solve_cnf_formula(verbose=True)
if circuit:
    print(circuit)
    circuit.draw(detailed_labels=False, file_name=f'majority_{n}_{gates}_monotone')
else:
    print('There is no such circuit!')

