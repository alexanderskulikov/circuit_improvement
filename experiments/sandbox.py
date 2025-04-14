from core.circuit_improvement import *
from functions.mult import *
from functions.th import *
from functions.sum import *
from core.circuit_search import *
from datetime import datetime
from core.circuit_improvement import *

ckt = Circuit(input_labels=[f'x{i}' for i in range(1, 6)])
a0, a1 = add_sum3(ckt, ['x1', 'x2', 'x3'])
b0, b1 = add_sum3(ckt, [a0, 'x4', 'x5'])
c1, c2 = add_sum2(ckt, [a1, b1])
ckt.outputs = [b0, c1, c2]

improve_circuit_iteratively(ckt, file_name='sum5', basis='xaig', save_circuits=True, speed=15)

