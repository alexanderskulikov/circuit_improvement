from core.circuit_improvement import improve_circuit_iteratively
from core.circuit import *
import os
import re


input_folder, output_folder, max_size = 'pareto', 'pareto-improved', 100
pareto_frontier = dict()

for file_name in sorted(os.listdir(input_folder)):
    if file_name.startswith('.'):
        continue

    fields = re.split(r'[_, .]+', file_name)
    bench_name, depth, size = fields[0], int(fields[1]), int(fields[2])
    if bench_name not in pareto_frontier:
        pareto_frontier[bench_name] = []
    pareto_frontier[bench_name].append((depth, size))


for file_name in sorted(os.listdir(input_folder)):
    if file_name.startswith('.'):
        continue

    fields = re.split(r'[_, .]+', file_name)
    bench_name, depth, size = fields[0], int(fields[1]), int(fields[2])

    if size > max_size:
        continue

    try:
        circuit = Circuit()
        circuit.load_from_file(path=folder + '/' + file_name)
        circuit.normalize(basis='aig')

        improve_circuit_iteratively(
            circuit,
            file_name=fields[0],
            basis='aig',
            save_circuits=True,
            speed='easy',
            global_time_limit= 60 * 2,
            # global_time_limit=60 * 60 * 24 * 2,
            keep_depth=False
        )
    except Exception as err:
        print(f'    \033[91mUnexpected {err=}, {type(err)=}\033[0m')

