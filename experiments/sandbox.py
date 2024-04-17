from core.circuit_improvement import *
from functions.mult import *
from functions.th import *
from core.circuit_search import *
from datetime import datetime

for size in (10, 9, 8):
    f = CircuitFinder(dimension=6, output_truth_tables=['1010111110101111101000001010000010101111101000111111010101110001', ], number_of_gates=size)
    f.fix_gate(6, 3, 5, '0111')
    ckt = f.solve_cnf_formula()
    if ckt:
        ckt.save_to_file(f'z_ex80_size{size}', extension='bench')
