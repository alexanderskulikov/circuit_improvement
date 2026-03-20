from core.circuit_improvement import improve_circuit_iteratively
from core.circuit import *
import os
import re

processed_benches_file_name = 'processed-bench-names.txt'
input_folder, output_folder, max_size = '/Users/Alexander.Kulikov/Desktop/pareto', '/Users/Alexander.Kulikov/Desktop/pareto-improved', 2000
# total_time = 60 * 60 * 24 * 3  # 3 days
total_time = 60 * 60 * 9  # nine hours


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

single_benchmark_timelimit = total_time / max(1, len(files_to_be_processed))

print('Start improving Pareto front')
print(f'  Skipping {nof_too_big} benches as they are too large and skipping {nof_processed_already} benches as they have been processed already')
print(f'  Processing {len(files_to_be_processed)} benches')
print(f'  The total time given is {total_time} sec (or {total_time / 3600:.1f} hours, or {total_time / 3600 / 24:.1f} days),'
      f' so each benchmark will be given {single_benchmark_timelimit:.1f} sec (or {single_benchmark_timelimit / 3600:.1f} hours)\n')


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
