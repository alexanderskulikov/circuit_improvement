from core.circuit_improvement import improve_circuit
from functions.sum import *
from core.circuit_search import *


def verify_majority_circuit(circuit):
    n = len(circuit.input_labels)
    table = circuit.get_truth_tables()[circuit.outputs[0]]
    for value, x in enumerate(product(range(2), repeat=n)):
        assert (table[value] == 1) == (sum(x) > n / 2)


def synthesize_maj_circuit_via_sum(n):
    circuit = Circuit(input_labels=[f'x{i}' for i in range(1, n + 1)])

    if n == 9:
        w0, w1, w2, w3 = add_sum9_size27(circuit, circuit.input_labels)
        y1 = circuit.add_gate(w0, w1, '0111')
        y2 = circuit.add_gate(y1, w2, '0001')
        y3 = circuit.add_gate(y2, w3, '0111')
        circuit.outputs = [y3, ]
    elif n == 11:
        w0, w1, w2, w3 = add_sum11_size34(circuit, circuit.input_labels)
        y1 = circuit.add_gate(w1, w2, '0001')
        y2 = circuit.add_gate(w3, y1, '0111')
        circuit.outputs = [y2, ]
    elif n == 13:
        x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13 = circuit.input_labels
        a0, a1, a2 = add_sum7_size19(circuit, [x1, x2, x3, x4, x5, x6, x7])
        w0, b1, b2 = add_sum7_size19(circuit, [a0, x8, x9, x10, x11, x12, x13])
        w1, c2 = add_sum2(circuit, [a1, b1])
        w2, w3 = add_sum3(circuit, [a2, b2, c2])
        y1 = circuit.add_gate(w0, w1, '0001')
        y2 = circuit.add_gate(y1, w2, '0001')
        y3 = circuit.add_gate(y2, w3, '0111')
        circuit.outputs = [y3, ]
    elif n == 15:
        w0, w1, w2, w3 = add_sum15_size51(circuit, circuit.input_labels)
        circuit.outputs = [w3]

    verify_majority_circuit(circuit)
    return circuit
