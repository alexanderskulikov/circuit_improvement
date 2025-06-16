from core.circuit_improvement import *
from functions.mult import *
from core.circuit_search import *

from functions.sum import add_sum

for k in range(3, 8):
    n = 2 ** k - 1
    ckt = Circuit(input_labels=[f'x{i}' for i in range(n)])
    outs = add_sum(ckt, ckt.input_labels, basis='aig')
    ckt.outputs = outs
    ckt.save_to_file(f'sum{n}_size{ckt.get_nof_true_binary_gates()}_aig.bench')