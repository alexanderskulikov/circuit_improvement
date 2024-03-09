from core.circuit_improvement import improve_circuit
from functions.sum import *

circuit = Circuit(input_labels=[f'x{i}' for i in range(1, 8)])
w0, w1, w2 = add_sum7(circuit, circuit.input_labels)
circuit.outputs = [w2, ]
better_circuit = improve_circuit(circuit)

print(better_circuit.get_truth_tables())