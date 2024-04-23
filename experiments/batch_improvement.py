from core.circuit_improvement import *
from datetime import datetime
from os import listdir

print('Start batch improvement. Time:', datetime.now())

for file_name in sorted(listdir('./circuits/')):
    if file_name == '.images':
        continue

    ckt = Circuit()
    ckt.load_from_file(file_name[:-6], extension='bench')
    ckt.normalize()
    print(f'Processing {file_name[:-6]} of size {ckt.get_nof_true_binary_gates()}')
    improve_circuit_iteratively(ckt, file_name[:-6], max_subcircuit_size=7)

print('Done! Time:', datetime.now())
