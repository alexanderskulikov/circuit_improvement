# checking what happens if instead of computing x1+x2+...+xn we compute smth like
# x1+2x2-2x1x2+x3+...+xn

from math import ceil, log2
from core.circuit_search import CircuitFinder


def sum_n(x):
    assert len(x) in (3, 4, 5)
    s = x[0] + 2 * x[1] - 2 * x[0] * x[1] + sum(x[2:])
    assert 0 <= s <= len(x)
    return [(s >> i) & 1 for i in range(ceil(log2(len(x) + 1)))]


n, upper = 3, 5
for size in range(upper, -1, -1):
    finder = CircuitFinder(dimension=n, number_of_gates=size, function=sum_n)
    circuit = finder.solve_cnf_formula(verbose=0)
    print(f'size={size}: ', end='')
    if circuit:
        print('circuit found')
        circuit.draw(f'sum{n}_deg2_size{size}.png')
    else:
        print('there is no circuit')
        break