from core.circuit_improvement import *
from functions.sum import *
from core.circuit_search import *
from math import ceil, log2


def verify_majority_circuit(circuit):
    n = len(circuit.input_labels)
    table = circuit.get_truth_tables()[circuit.outputs[0]]
    for value, x in enumerate(product(range(2), repeat=n)):
        assert (table[value] == 1) == (sum(x) > n / 2)


def synthesize_maj_circuit_via_sum_old(n):
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


def synthesize_majority_circuit(n, basis):
    assert n % 2 and basis in ('xaig', 'aig')
    print(f'--> Synthesizing a majority circuit for n={n} over the basis {basis}')

    circuit = Circuit(input_labels=[f'x{i}' for i in range(1, n + 1)])
    sum_outputs = add_sum(circuit, circuit.input_labels, basis)

    if n in (7, 15):
        circuit.outputs = [sum_outputs[-1], ]
        circuit.outputs_negations = [False]
    else:
        assert len(sum_outputs) == ceil(log2(n + 1))

        def final_block_function(sum_bits):
            s = sum(sum_bits[i] * (2 ** i) for i in range(len(sum_bits)))
            if s > n:
                return '*'
            else:
                return '1' if s > n / 2 else '0'

        final_block, final_block_size = False, len(sum_outputs) - 2
        while not final_block:
            final_block_size += 1
            finder = CircuitFinder(dimension=len(sum_outputs), input_labels=sum_outputs,
                                   function=final_block_function, number_of_gates=final_block_size,
                                   basis=basis)
            final_block = finder.solve_cnf_formula(time_limit=200)

        print(f'Found a final block of size {final_block_size}')
        final_block.rename_internal_gates(prefix='maj')
        final_block.rename_output_gates(['out'])

        for gate in final_block.gates:
            first, second, oper = final_block.gates[gate]
            circuit.add_gate(first, second, oper, gate)

        circuit.outputs = ['out',]
        circuit.outputs_negations = [False,]

    print(f'Synthesized a circuit of size {circuit.get_nof_true_binary_gates()}!')

    print('Verifying a circuit...', end='')
    verify_majority_circuit(circuit)
    print('OK!')

    if basis == 'xaig':
        circuit.normalize()
        print(f'Size after normalization: {circuit.get_nof_true_binary_gates()}')

    print(f'Now, try to improve it locally...')
    better_circuit = improve_circuit_iteratively(
        circuit, time_limit=2, min_subcircuit_size=4, max_subcircuit_size=9,
        file_name=f'tmp_{basis}_maj{n}', save_circuits=False, basis=basis)
    verify_majority_circuit(better_circuit)
    print(f'Final circuit:')
    better_circuit.save_to_file(f'{basis}_maj{"0" if n < 10 else ""}{n}_size{better_circuit.get_nof_true_binary_gates()}', extension='bench')


if __name__ == '__main__':
    for basis, n in product(('aig',), (5, 7, 9, 11, 13, 15)):
        synthesize_majority_circuit(n, basis)
