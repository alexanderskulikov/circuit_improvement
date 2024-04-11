from core.circuit_improvement import *
from functions.mult import *
from core.circuit_search import *

ckt = Circuit(input_labels=[f'x{i}' for i in range(8)])
r = add_mul_4_4(ckt, ckt.input_labels)
ckt.outputs = [r[1], r[3]]
ckt.normalize()
print(ckt.get_nof_true_binary_gates())
ckt = improve_circuit_iteratively(ckt, max_subcircuit_size=5)
print(ckt.get_nof_true_binary_gates())
