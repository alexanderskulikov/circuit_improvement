from functions.sum import *
from core.circuit_improvement import *

ckt = Circuit(input_labels=['x0', 'x1', 'x2', 'x3', 'y0', 'y1', 'y2', 'y3'])
a0, a1 = add_sum2(ckt, ['x0', 'y0'])
b1, b2 = add_sum3(ckt, [a1, 'x1', 'y1'])
c2, c3 = add_sum3(ckt, [b2, 'x2', 'y2'])
d4, d5 = add_sum3(ckt, [c3, 'x3', 'y3'])
ckt.outputs = [a1, d4]

print(len(ckt.gates))

ckt = improve_circuit_iteratively(ckt, speed=15)
print()
print(len(ckt.gates))
print(ckt)
ckt.save_to_file('improved_circuit', extension='bench')
