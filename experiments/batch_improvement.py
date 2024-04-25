from core.circuit_improvement import *
from datetime import datetime
from os import listdir

print(f'Start batch improvement ({datetime.now()})')

for file_name in sorted(listdir('./circuits/')):
    if file_name == '.images':
        continue

    ckt = Circuit()
    ckt.load_from_file(file_name[:-6], extension='bench')
    ckt.normalize()

    if len(ckt.gates) < ckt.get_nof_true_binary_gates():
        print(f'Skipping {file_name[:-6]} as it still contains unary gates')
    else:
        print(f'Processing {file_name[:-6]} of size {ckt.get_nof_true_binary_gates()} ({datetime.now()})')
        improve_circuit_iteratively(ckt, file_name[:-6],
                                    min_subcircuit_size=9, max_subcircuit_size=9, max_inputs=7, time_limit=10,
                                    forbidden_operations=['0110', '1001'])

print(f'Done! ({datetime.now()})')
