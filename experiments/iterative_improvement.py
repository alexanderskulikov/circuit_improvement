from core.circuit_improvement import improve_circuit_iteratively
from core.circuit import *


# put your circuit (say, ex01.bench) to the eperiments/curcuits folder, then load it as follows
circuit = Circuit()
circuit.load_from_file('ex01', extension='bench')
circuit.normalize(basis='aig')

# you can adjust the speed in the call below (1--18)
improve_circuit_iteratively(circuit, file_name='tmp', basis='aig', save_circuits=True, speed=10)

