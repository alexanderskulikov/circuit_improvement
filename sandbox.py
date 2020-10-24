from circuit import Circuit
from circuit_search import find_circuit, CircuitFinder
from itertools import product


if __name__ == '__main__':
    n = 5
    tt = [
        ''.join(str(sum(x) & 1) for x in product(range(2), repeat=n)),
        ''.join(str((sum(x) >> 1) & 1) for x in product(range(2), repeat=n)),
        ''.join(str((sum(x) >> 2) & 1) for x in product(range(2), repeat=n))
    ]

    circuit_finder = CircuitFinder(5, None, None, 11, tt)
    circuit_finder.fix_gate(5, 0, 1, '0110')
    circuit_finder.fix_gate(6, 2, 5, '0110')
    circuit_finder.fix_gate(7, 3, 6, '0110')
    circuit_finder.fix_gate(8, 4, 7, '0110')
    c = circuit_finder.solve_cnf_formula()

    if c:
        print(c)
        c.draw('circuit.png')
    else:
        print('There is no such circuit')