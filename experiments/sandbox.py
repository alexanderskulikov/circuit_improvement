from core.circuit_improvement import *
from functions.mult import *
from functions.th import *
from functions.sum import *
from core.circuit_search import *
from datetime import datetime
from core.circuit_improvement import *

finder = CircuitFinder(dimension=2, output_truth_tables=['0110', ], basis='aig', number_of_gates=3)
ckt = finder.solve_cnf_formula()
print(ckt)

