from core.circuit_improvement import improve_circuit
from functions.sum import *


def verify_majority_circuit(circuit):
    table = circuit.get_truth_tables()[circuit.outputs[0]]
    for value, x in enumerate(product(range(2), repeat=len(circuit.input_labels))):
        assert (table[value] == 1) == (sum(x) > n / 2)


n = 9
circuit = Circuit(input_labels=[f'x{i}' for i in range(1, n + 1)])
w0, w1, w2, w3 = add_sum9(circuit, circuit.input_labels)
y1 = circuit.add_gate(w0, w1, '0111')
y2 = circuit.add_gate(y1, w2, '0001')
y2 = circuit.add_gate(y2, w3, '0111')
circuit.outputs = [y2, ]
verify_majority_circuit(circuit)
circuit.save_to_file('maj09', extension='bench')

# n = 11
# circuit = Circuit(input_labels=[f'x{i}' for i in range(1, n + 1)])
# w0, w1, w2, w3 = add_sum11_size36(circuit, circuit.input_labels)
# y1 = circuit.add_gate(w1, w2, '0001')
# y2 = circuit.add_gate(w3, y1, '0111')
# circuit.outputs = [y2, ]
# verify_majority_circuit(circuit)
#
# n = 15
# circuit = Circuit(input_labels=[f'x{i}' for i in range(1, n + 1)])
# w0, w1, w2, w3 = add_sum15_size53(circuit, circuit.input_labels)
# circuit.outputs = [w3]
# verify_majority_circuit(circuit)