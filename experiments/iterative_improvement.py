from core.circuit_improvement import improve_circuit_iteratively
from core.circuit import *
from datetime import datetime, timedelta

import os
import re

processed_benches_file_name = 'processed-bench-names.txt'
input_folder, output_folder = '/Users/Alexander.Kulikov/Desktop/pareto', '/Users/Alexander.Kulikov/Desktop/pareto-improved'
max_size = 1000

# total_time = 60 * 60 * 24 * 3  # 3 days
total_time = 60 * 45  # nine hours


if not os.path.exists(processed_benches_file_name):
    with open(processed_benches_file_name, 'w'):
        pass

with open(processed_benches_file_name, 'r') as processed_benches_file:
    processed_bench_names = [line.rstrip() for line in processed_benches_file]

files_to_be_processed = []
nof_too_big, nof_processed_already = 0, 0

for file_name in sorted(os.listdir(input_folder)):
    if not file_name.endswith('.bench'):
        continue

    if file_name in processed_bench_names:
        nof_processed_already += 1
        continue

    fields = re.split(r'[_, .]+', file_name)
    size = int(fields[2])

    if size > max_size:
        nof_too_big += 1
        continue

    files_to_be_processed.append(file_name)

single_benchmark_timelimit = total_time // max(1, len(files_to_be_processed))

print(f'''
Start improving Pareto front
Processing {len(files_to_be_processed)} benches, giving each one {single_benchmark_timelimit} sec (or {single_benchmark_timelimit / 3600:.1f} hours), and skipping {nof_too_big} large benches and {nof_processed_already} already processed benches
ETA: {(datetime.now() + timedelta(seconds=total_time)).strftime("%Y-%m-%d %H:%M:%S")}
''')

for file_name in files_to_be_processed:
    print('\nProcessing', file_name)

    fields = re.split(r'[_, .]+', file_name)
    bench_name = fields[0]

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
            global_time_limit=single_benchmark_timelimit,
            keep_depth=False,
            output_folder=output_folder
        )

        with open(processed_benches_file_name, 'a') as processed_benches_file:
            processed_benches_file.write(file_name + '\n')

    except Exception as err:
        print(f'    \033[91mUnexpected {err=}, {type(err)=}\033[0m')
