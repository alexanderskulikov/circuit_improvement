from core.circuit_improvement import improve_circuit_iteratively
from core.circuit import *
import os
import re

# with open('processed-bench-names.txt', 'r+') as processed_benches_file:
#     processed_bench_names = [line.rstrip() for line in processed_benches_file]




exit()


input_folder, output_folder, max_size = 'pareto', 'pareto-improved', 100

for file_name in sorted(os.listdir(input_folder)):
    if not file_name.endswith('.bench'):
        continue

    fields = re.split(r'[_, .]+', file_name)
    bench_name, depth, size = fields[0], int(fields[1]), int(fields[2])

    print('Processing', file_name)

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
            global_time_limit= 60 * 2,
            keep_depth=False,
            output_folder=output_folder
        )
    except Exception as err:
        print(f'    \033[91mUnexpected {err=}, {type(err)=}\033[0m')

