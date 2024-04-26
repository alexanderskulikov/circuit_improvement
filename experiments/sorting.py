from core.circuit_search import *
from core.circuit_improvement import *
from functions.sum import *
from math import ceil, log2


def verify_sorting_circuit(circuit):
    n = len(circuit.input_labels)
    assert n == len(circuit.outputs)

    tables = circuit.get_truth_tables()
    for value, x in enumerate(product(range(2), repeat=n)):
        for i in range(n):
            assert (tables[circuit.outputs[i]][value] == 1) == (sum(x) >= n - i)


def synthesize_sorting_circuit(n, basis):
    basis in ('xaig', 'aig')

    print(f'--> Synthesizing a sorting circuit for n={n} over the basis {basis}')

    circuit = Circuit(input_labels=[f'x{i}' for i in range(1, n + 1)])
    sum_outputs = add_sum(circuit, circuit.input_labels, basis)
    assert len(sum_outputs) == ceil(log2(n + 1))

    def final_block_function(sum_bits):
        s = sum(sum_bits[i] * (2 ** i) for i in range(len(sum_bits)))
        if s > n:
            return ['*'] * n
        else:
            return [1 if s >= t else 0 for t in range(n, 0, -1)]

    final_block, final_block_size = False, n - 1
    while not final_block:
        final_block_size += 1
        finder = CircuitFinder(dimension=len(sum_outputs), input_labels=sum_outputs,
                               function=final_block_function, number_of_gates=final_block_size,
                               basis=basis)
        final_block = finder.solve_cnf_formula(time_limit=20, verbose=0)

    print(f'Found a final block of size {final_block_size}')
    final_block.rename_internal_gates(prefix='sort')
    final_block.rename_output_gates([f'out{i}' for i in range(1, n + 1)])

    for gate in final_block.gates:
        first, second, oper = final_block.gates[gate]
        circuit.add_gate(first, second, oper, gate)

    circuit.outputs = [f'out{i}' for i in range(1, n + 1)]
    circuit.outputs_negations = [False] * n

    print(f'Synthesized a circuit of size {circuit.get_nof_true_binary_gates()}!')

    print('Verifying a circuit...', end='')
    verify_sorting_circuit(circuit)
    print('OK!')

    print(f'Now, try to improve it locally...')
    better_circuit = improve_circuit_iteratively(
        circuit, speed='fast',
        file_name=f'tmp_{basis}_sort{n}', save_circuits=False, basis=basis)

    verify_sorting_circuit(better_circuit)
    print(f'Final circuit:')
    better_circuit.save_to_file(f'{basis}_sort{"0" if n < 10 else ""}{n}_size{better_circuit.get_nof_true_binary_gates()}', extension='bench')


if __name__ == '__main__':
    for basis, n in product(('xaig', 'aig',), range(5, 17)):
        synthesize_sorting_circuit(n, basis)
