from core.circuit_search import *
from core.circuit_improvement import *
from functions.sum import *

for i in range(85, 86):
    file_name = 'ex' + ('0' if i < 10 else '') + str(i)
    ckt = Circuit()
    ckt.load_from_file(file_name, extension='bench')
    ckt.contract_not_gates()
    print(ckt.get_nof_true_binary_gates())
    improve_circuit_iteratively(ckt, max_subcircuit_size=7)


