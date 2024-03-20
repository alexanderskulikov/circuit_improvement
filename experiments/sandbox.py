from core.circuit_search import *
from functions.sum import *


# finder = CircuitFinder(
#     dimension=7,
#     output_truth_tables=['11010000111110100000000000001010000000000000000000000000000000000100011011000110000001000000110000000000000000000000000000000000',
#     ],
#     number_of_gates=16,
# )
# ckt = finder.solve_cnf_formula(verbose=True, solver='cadical195')
# if ckt:
#     ckt.save_to_file('2024_ex30_real_size16', extension='bench')

def sum8block(x):
    a2, a1, a0, x6, x7, x8 = x
    s = 4 * a2 + 2 * a1 + a0 + x6 + x7 + x8
    if s > 8:
        return ['*', '*', '*', '*']
    else:
        return [s >> i & 1 for i in range(4)]


# for size in range(14, 3, -1):
#     finder = CircuitFinder(dimension=6, function=sum8block, number_of_gates=size)
#     block = finder.solve_cnf_formula(verbose=True, solver='cadical195')
#     block.save_to_file(f'sum08_block_size{size}', extension='ckt')

# for s in range(9):
#     print(s, [s >> i & 1 for i in range(4)])

ckt = Circuit(input_labels=[f'x{i}' for i in range(8)])
ckt.outputs = add_sum8_size25(ckt, ckt.input_labels)
check_sum_circuit(ckt)
ckt.save_to_file('sum08_size25', extension='ckt')
ckt.save_to_file('sum08_size25', extension='bench')

