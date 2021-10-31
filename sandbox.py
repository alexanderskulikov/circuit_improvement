from functions import BooleanFunction
from itertools import product
from circuit_search import CircuitFinder

n = 6


def majority(x):
    return 1 if sum(x) > len(x) // 2 else 0


f = BooleanFunction([majority(x) for x in product(range(2), repeat=n)])


minimum_subfunction_circuit_size, best_substitution = 5, None
for subs in product(range(2), repeat=(2 ** (n - 1))):
    g = f.get_subfunction(variable=0, substitution=BooleanFunction(subs))
    print('\n', *subs, g.truth_table, minimum_subfunction_circuit_size, best_substitution, end=' ')

    circuit_exists = True
    while circuit_exists:
        circuit_finder = CircuitFinder(dimension=n - 1, output_truth_tables=[g.truth_table, ], number_of_gates=minimum_subfunction_circuit_size)
        if circuit_finder.solve_cnf_formula():
            circuit_exists = True
            print('->', minimum_subfunction_circuit_size, end=' ')
            minimum_subfunction_circuit_size -= 1
            best_substitution = subs
        else:
            circuit_exists = False

