from core.circuit_improvement import *
from functions.sum import *

circuit = Circuit(input_labels=[f'x{i}' for i in range(13)])
circuit.outputs = add_sum13_size43(circuit, circuit.input_labels)

print(improve_circuit(circuit))
