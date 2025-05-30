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
    assert basis in ('xaig', 'aig')

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

    print('Looking for a final block...', end='')
    final_block, final_block_size = False, n - 1
    while not final_block:
        final_block_size += 1
        print(f'{final_block_size}...', end='')
        finder = CircuitFinder(dimension=len(sum_outputs), input_labels=sum_outputs,
                               function=final_block_function, number_of_gates=final_block_size,
                               basis=basis)
        final_block = finder.solve_cnf_formula(time_limit=60, verbose=0)

    print('Done!')

    final_block.rename_internal_gates(prefix='sort')
    final_block.rename_output_gates([f'sout{i}' for i in range(1, n + 1)])

    for gate in final_block.gates:
        first, second, oper = final_block.gates[gate]
        circuit.add_gate(first, second, oper, gate)

    circuit.outputs = [f'sout{i}' for i in range(1, n + 1)]
    circuit.outputs_negations = [False] * n

    print(f'Synthesized a circuit of size {circuit.get_nof_true_binary_gates()}!')

    print('Verifying a circuit...', end='')
    verify_sorting_circuit(circuit)
    print('OK!')

    print(f'Now, try to improve it locally...')
    better_circuit = improve_circuit_iteratively(
        circuit, speed=15,
        file_name=f'tmp_{basis}_sort{n}', save_circuits=False, basis=basis)

    verify_sorting_circuit(better_circuit)
    print(f'Final circuit:')
    better_circuit.save_to_file(f'{basis}_sort{"0" if n < 10 else ""}{n}_size{better_circuit.get_nof_true_binary_gates()}', extension='bench')

def experiments():
    n, basis = 9, 'aig'
    circuit = Circuit(input_labels=[f'x{i}' for i in range(1, n + 1)])
    a0, a1 = add_sum3(circuit, ['x1', 'x2', 'x3'], basis=basis)
    b0, b1 = add_sum3(circuit, [a0, 'x4', 'x5'], basis=basis)
    c0, c1 = add_sum3(circuit, [b0, 'x6', 'x7'], basis=basis)
    d0, d1 = add_sum3(circuit, [c0, 'x8', 'x9'], basis=basis)
    e1, e2 = add_sum3(circuit, [a1, b1, c1], basis=basis)

    def final_block_function(y):
        (d0, d1, e1, e2) = y
        s = d0 + 2 * d1 + 2 * e1 + 4 * e2
        assert 0 <= s <= n
        return [1 if s >= t else 0 for t in range(n, 0, -1)]

    print('Looking for a final block...', end='')
    final_block, final_block_size = False, n - 1
    while not final_block:
        final_block_size += 1
        print(f'{final_block_size}...', end='')
        finder = CircuitFinder(dimension=4, input_labels=[d0, d1, e1, e2],
                               function=final_block_function, number_of_gates=final_block_size,
                               basis=basis)
        final_block = finder.solve_cnf_formula(time_limit=200, verbose=0)

    print('Done!')

    final_block.rename_internal_gates(prefix='sort')
    final_block.rename_output_gates([f'sout{i}' for i in range(1, n + 1)])

    for gate in final_block.gates:
        first, second, oper = final_block.gates[gate]
        circuit.add_gate(first, second, oper, gate)

    circuit.outputs = [f'sout{i}' for i in range(1, n + 1)]
    circuit.outputs_negations = [False] * n

    print(f'Synthesized a circuit of size {circuit.get_nof_true_binary_gates()}!')

    print('Verifying a circuit...', end='')
    verify_sorting_circuit(circuit)
    print('OK!')

    print(f'Now, try to improve it locally...')
    better_circuit = improve_circuit_iteratively(
        circuit, speed=12,
        file_name=f'tmp_{basis}_sort{n}', save_circuits=False, basis=basis)

    verify_sorting_circuit(better_circuit)
    print(f'Final circuit:')
    better_circuit.save_to_file(f'{basis}_sort{"0" if n < 10 else ""}{n}_size{better_circuit.get_nof_true_binary_gates()}', extension='bench')


def synthesize_sort15_aig():
    circuit = Circuit(input_labels=[f'x{i}' for i in range(1, 16)])
    b = add_sum(circuit, circuit.input_labels, 'aig')  # size: 77

    l0 = circuit.add_gate(b[0], b[1], '1000')
    l1 = circuit.add_gate(b[0], b[1], '0100')
    l2 = circuit.add_gate(b[0], b[1], '0010')
    l3 = circuit.add_gate(b[0], b[1], '0001')

    r0 = circuit.add_gate(b[2], b[3], '1000')
    r1 = circuit.add_gate(b[2], b[3], '0100')
    r2 = circuit.add_gate(b[2], b[3], '0010')
    r3 = circuit.add_gate(b[2], b[3], '0001')

    e1 = circuit.add_gate(l1, r0, '0001')
    e2 = circuit.add_gate(l2, r0, '0001')
    e3 = circuit.add_gate(l3, r0, '0001')
    e4 = circuit.add_gate(l0, r1, '0001')
    e5 = circuit.add_gate(l1, r1, '0001')
    e6 = circuit.add_gate(l2, r1, '0001')
    e7 = circuit.add_gate(l3, r1, '0001')
    e8 = circuit.add_gate(l0, r2, '0001')
    e9 = circuit.add_gate(l1, r2, '0001')
    e10 = circuit.add_gate(l2, r2, '0001')
    e11 = circuit.add_gate(l3, r2, '0001')
    e12 = circuit.add_gate(l0, r3, '0001')
    e13 = circuit.add_gate(l1, r3, '0001')
    e14 = circuit.add_gate(l2, r3, '0001')
    e15 = circuit.add_gate(l3, r3, '0001')

    ge15 = e15
    ge14 = circuit.add_gate(ge15, e14, '0111')
    ge13 = circuit.add_gate(ge14, e13, '0111')
    ge12 = circuit.add_gate(ge13, e12, '0111')
    ge11 = circuit.add_gate(ge12, e11, '0111')
    ge10 = circuit.add_gate(ge11, e10, '0111')
    ge9 = circuit.add_gate(ge10, e9, '0111')
    ge8 = circuit.add_gate(ge9, e8, '0111')
    ge7 = circuit.add_gate(ge8, e7, '0111')
    ge6 = circuit.add_gate(ge7, e6, '0111')
    ge5 = circuit.add_gate(ge6, e5, '0111')
    ge4 = circuit.add_gate(ge5, e4, '0111')
    ge3 = circuit.add_gate(ge4, e3, '0111')
    ge2 = circuit.add_gate(ge3, e2, '0111')
    ge1 = circuit.add_gate(ge2, e1, '0111')

    circuit.outputs = [ge15, ge14, ge13, ge12, ge11, ge10, ge9, ge8, ge7, ge6, ge5, ge4, ge3, ge2, ge1]
    return circuit




if __name__ == '__main__':
    # for basis, n in product(('aig', 'xaig'), range(5, 17)):
    #     synthesize_sorting_circuit(n, basis)

    # experiments()
    ckt = synthesize_sort15_aig()
    # verify_sorting_circuit(ckt)
    print(ckt.get_nof_true_binary_gates())
    improve_circuit_iteratively(ckt, speed=8, file_name=f'sort15', save_circuits=False, basis='aig')





