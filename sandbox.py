from circuit import Circuit
from circuit_search import find_circuit, CircuitFinder
from itertools import product
from circuit_search_tests import verify_sum_circuit
from functions import *
from circuit_improvement import improve_circuit
from math import log2


if __name__ == '__main__':

    def sum_n(x):
        assert all(a in (0, 1) for a in x)
        s, l = sum(x), int(log2(len(x) + 1))
        return [(s >> i) & 1 for i in range(l)]

    circuit_finder = CircuitFinder(dimension=3, number_of_gates=5, function=sum_n)
    circuit = circuit_finder.solve_cnf_formula()
    print(circuit)