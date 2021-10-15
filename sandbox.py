from circuit_search import CircuitFinder

# finding a circuit for the parity function over U_2

def parity(x):
    return [sum(x) % 2, ]

finder = CircuitFinder(dimension=4, number_of_gates=9, function=parity, forbidden_operations=['0110', '1001'])
circuit = finder.solve_cnf_formula()
print(circuit)
circuit.draw('parity_u2')