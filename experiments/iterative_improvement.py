from core.circuit_improvement import improve_circuit_iteratively
from core.circuit import *

folder = 'circuits'
for file_name in sorted(os.listdir(folder)):
    if file_name.startswith('.'):
        continue
    circuit = Circuit()
    circuit.load_from_file(path=folder + '/' + file_name)
    circuit.normalize(basis='aig')
    improve_circuit_iteratively(circuit, file_name=file_name, basis='aig', save_circuits=True, speed=11, global_time_limit=60 * 60 * 24 * 2)

