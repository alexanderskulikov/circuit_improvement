from core.circuit_improvement import improve_circuit_iteratively
from core.circuit import *
import os
import re

processed_benches_file_name = 'processed-bench-names.txt'
input_folder, output_folder, max_size = 'circuits', 'circuits/improved', 4000


if not os.path.exists(processed_benches_file_name):
    with open(processed_benches_file_name, 'w'):
        pass

with open(processed_benches_file_name, 'r') as processed_benches_file:
    processed_bench_names = [line.rstrip() for line in processed_benches_file]

for file_name in sorted(os.listdir(input_folder)):
    if not file_name.endswith('.bench'):
        continue

    print('Processing', file_name)

    if file_name in processed_bench_names:
        print('  skip: has been processed already')
        continue

    fields = re.split(r'[_, .]+', file_name)
    bench_name, depth, size = fields[0], int(fields[1]), int(fields[2])

    if size > max_size:
        print('  skip: the size is too large')
        continue

    try:
        circuit = Circuit()
        circuit.load_from_file(path=input_folder + '/' + file_name)
        circuit.normalize(basis='aig')

        improve_circuit_iteratively(
            circuit,
            file_name=fields[0],
            basis='aig',
            save_circuits=True,
            speed='easy',
            global_time_limit=60 * 60 * 40,
            keep_depth=False,
            output_folder=output_folder
        )

        with open(processed_benches_file_name, 'a') as processed_benches_file:
            processed_benches_file.write(file_name + '\n')

    except Exception as err:
        print(f'    \033[91mUnexpected {err=}, {type(err)=}\033[0m')
