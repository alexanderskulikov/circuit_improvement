from core.circuit_improvement import *
from functions.mult import *
from core.circuit_search import *

def f(x):
    assert len(x) == 3
    # return (x[0] + x[1]) % 2, (1 + x[0] * x[1]) % 2, (x[0] + x[1] + x[0] * x[1] + 1 + x[2]) % 2
    return [(x[0] + x[1] + x[0] * x[1] + 1 + x[2]) % 2,]

finder = CircuitFinder(dimension=3, function=f, number_of_gates=2)
ckt = finder.solve_cnf_formula()
print(ckt)
