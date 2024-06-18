from core.circuit_improvement import *
from functions.mult import *
from functions.th import *
from functions.sum import *
from core.circuit_search import *
from datetime import datetime
from core.circuit_improvement import *

ckt = Circuit(input_labels=[f'x{i}' for i in range(7)])
ckt.outputs = add_sum(ckt, ckt.input_labels, basis='aig')
print(ckt.get_nof_true_binary_gates())
improve_circuit_iteratively(ckt, file_name='sum7_aig', basis='aig', speed=10)
