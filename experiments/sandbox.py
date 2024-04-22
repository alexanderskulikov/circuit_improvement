from core.circuit_improvement import *
from functions.mult import *
from functions.th import *
from core.circuit_search import *
from datetime import datetime

finder = CircuitFinder(
    dimension=4,
    number_of_gates=11,
    output_truth_tables=['0000000000000001', '0001011101111111', '0110100110010110'],
    forbidden_operations=['0110', '1001']
)
ckt = finder.solve_cnf_formula()
print(ckt)