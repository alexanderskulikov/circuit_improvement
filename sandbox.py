from circuit_search import CircuitFinder
from math import ceil, log2

def sum_n(x):
    return [(sum(x) >> i) & 1 for i in range(ceil(log2(len(x) + 1)))]


circuit_finder = CircuitFinder(dimension=3, number_of_gates=7,
                               function=sum_n, forbidden_operations=['0110', '1001'])
circuit = circuit_finder.solve_cnf_formula()
circuit.draw('sum3')