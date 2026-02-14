from core.circuit import Circuit
from core.circuit_improvement import improve_circuit_iteratively
from functions.sum import add_sum2, add_sum3, add_sum16_size59


circuit = Circuit(input_labels=[f'x{i}' for i in range(16)])
circuit.outputs = add_sum16_size59(circuit, circuit.input_labels)
ckt = improve_circuit_iteratively(circuit, speed='hard', global_time_limit=10 ** 5)
