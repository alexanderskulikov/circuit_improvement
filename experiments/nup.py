from core.circuit_improvement import *
from functions.sum import *

circuit = Circuit(input_labels=['x1', 'x2', 'x3', 'x4', 'x5'])
a0, a1 = add_sum3(circuit, ['x1', 'x2', 'x3'])
b0, b1 = add_sum3(circuit, ['x4', 'x5', a0])
c1, c2 = add_sum2(circuit, [a1, b1])
circuit.outputs = [b0, c1, c2]

circuit.draw('sum5')

improve_circuit_iteratively(circuit)