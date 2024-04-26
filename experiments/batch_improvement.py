from core.circuit_improvement import *
from datetime import datetime
from os import listdir

basis = 'xaig'

print(f'Start batch improvement ({datetime.now()})')
files = sorted(listdir('./circuits/'))

for file_number, file_name in enumerate(files):
    if file_name == '.images':
        continue

    ckt = Circuit()
    ckt.load_from_file(file_name[:-6], extension='bench')
    ckt.normalize(basis)

    if len(ckt.gates) < ckt.get_nof_true_binary_gates():
        print(f'Skipping {file_name[:-6]} as it still contains unary gates')
    else:
        print(f'[{file_number}/{len(files)}] Processing {file_name[:-6]} of size {ckt.get_nof_true_binary_gates()} ({datetime.now()})')
        improve_circuit_iteratively(ckt, file_name[:-6], basis=basis, speed='fast')

print(f'Done! ({datetime.now()})')
