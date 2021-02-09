# This tutorial shows the main features of the program.
# To run it in the cloud, press the Google Colab badge above
# and the notebook.

from circuit import Circuit
from functions import *
from math import ceil, log2


# Building a circuit for SUM5 out of SUM2 and SUM3 blocks
circuit = Circuit(input_labels=['x1', 'x2', 'x3', 'x4', 'x5'])
x1, x2, x3, x4, x5 = circuit.input_labels
a0, a1 = add_sum3(circuit, [x1, x2, x3])
b0, b1 = add_sum3(circuit, [a0, x4, x5])
w1, w2 = add_sum2(circuit, [a1, b1])
circuit.outputs = [b0, w1, w2]
check_sum_circuit(circuit)
circuit.draw('sum5')


# Finding an optimum circuit for SUM3 using SAT-solvers
def sum_n(x):
    return [(sum(x) >> i) & 1 for i in range(ceil(log2(len(x) + 1)))]


circuit = find_circuit(dimension=3, number_of_gates=5, function=sum_n)
circuit.draw('sum3')


