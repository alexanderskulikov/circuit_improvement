from core.circuit_improvement import improve_circuit_iteratively
from core.circuit import *

for file_name in sorted(os.listdir('circuits')):
    if file_name.startswith('.'):
        continue
    file_name = file_name[:-6]
    circuit = Circuit()
    circuit.load_from_file(file_name=file_name, extension='bench')
    circuit.normalize(basis='aig')
    improve_circuit_iteratively(circuit, file_name=file_name, basis='aig', save_circuits=True, speed=11)

