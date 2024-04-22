from core.circuit_improvement import *
from functions.sum import *
from os import listdir

for file_name in sorted(listdir('./circuits/')):
    if file_name == '.images':
        continue

    ckt = Circuit()
    ckt.load_from_file(file_name[:-6], extension='bench')
    ckt.normalize()
    original_size = ckt.get_nof_true_binary_gates()
    print(f'Processing {file_name[:-6]} of size {original_size}')
    improve_circuit_iteratively(ckt, file_name[:-6])
