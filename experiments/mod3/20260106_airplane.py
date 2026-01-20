from core.circuit_search import CircuitFinder


def mod3(x):
    assert(len(x) == 4)
    return [1, ] if 2 * x[0] + x[1] - 2 * x[0] * x[1] + x[2] + x[3] % 3 == 2 else [0, ]  # (r=0: size=3), (r=1, size=6), (r=2, size=5)
    # return [1, ] if sum(x) % 3 == 1 else [0, ]  # size: 7


finder = CircuitFinder(dimension=4, number_of_gates=4, function=mod3)
circuit = finder.solve_cnf_formula(verbose=True)
print(circuit)
