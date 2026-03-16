from core.circuit_improvement import improve_circuit_iteratively
from core.circuit import *
import os
import re


folder = 'circuits'
for file_name in sorted(os.listdir(folder)):
    if not file_name.endswith('.bench'):
        continue

    print('Processing', file_name)

    fields = re.split(r'[_, .]+', file_name)
    depth, size = int(fields[1]), int(fields[2])

    if size > 2000:
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
            global_time_limit= 60 * 60 * 17,
            # global_time_limit=60 * 60 * 24 * 2,
            keep_depth=False
        )
    except Exception as err:
        print(f'    \033[91mUnexpected {err=}, {type(err)=}\033[0m')

