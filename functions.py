from circuit import Circuit
from itertools import product
from circuit_improvement import improve_circuit


def add_binary_sum(circuit, input_labels, binary_operation):
    n = len(input_labels)
    last_gate = input_labels[0]
    for i in range(n - 1):
        new_gate = circuit.add_gate(last_gate, input_labels[i + 1], binary_operation)
        last_gate = new_gate
    return last_gate


def add_or(circuit, input_labels):
    return add_binary_sum(circuit, input_labels, '0111')


# of size 3n-5
def add_naive_thr2_circuit(circuit, input_labels):
    n = len(input_labels)
    c = circuit

    and_gates = [None] * (n + 1)
    thr1_gates = [None] * (n + 1)
    thr2_gates = [None] * (n + 1)

    thr1_gates[2] = c.add_gate(first_predecessor=input_labels[0], second_predecessor=input_labels[1], operation='0111')
    thr2_gates[2] = c.add_gate(first_predecessor=input_labels[0], second_predecessor=input_labels[1], operation='0001')

    for i in range(3, n + 1):
        if i < n:
            thr1_gates[i] = c.add_gate(
                first_predecessor=input_labels[i - 1],
                second_predecessor=thr1_gates[i - 1],
                operation='0111',
            )

        and_gates[i] = c.add_gate(
            first_predecessor=input_labels[i - 1],
            second_predecessor=thr1_gates[i - 1],
            operation='0001',
        )

        thr2_gates[i] = c.add_gate(
            first_predecessor=thr2_gates[i - 1],
            second_predecessor=and_gates[i],
            operation='0111',
        )

    #c_eff.outputs = [f'thr2-{n}']
    return [thr2_gates[n],]


# of size 2n+o(n)
def add_efficient_thr2_circuit(circuit, input_labels, rows, columns):
    n = len(input_labels)
    assert n == rows * columns

    row_gates, column_gates = [], []
    for i in range(rows):
        row_gates.append(add_or(circuit, [input_labels[i * columns + j] for j in range(columns)]))
    for j in range(columns):
        column_gates.append(add_or(circuit, [input_labels[i * columns + j] for i in range(rows)]))

    or1 = add_naive_thr2_circuit(circuit, row_gates)[0]
    or2 = add_naive_thr2_circuit(circuit, column_gates)[0]
    last_gate = circuit.add_gate(or1, or2, '0111')
    return [last_gate,]


def add_sum2(circuit, input_labels):
    assert len(input_labels) == 2
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2] = input_labels
    g1 = circuit.add_gate(x1, x2, '0110')
    g2 = circuit.add_gate(x1, x2, '0001')

    return g1, g2


def add_stockmeyers_block(circuit, input_labels):
    assert len(input_labels) == 3
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1_xor_x2, x2, x3] = input_labels
    g2 = circuit.add_gate(x2, x3, '0110')
    g3 = circuit.add_gate(x1_xor_x2, g2, '0111')
    g4 = circuit.add_gate(x1_xor_x2, x3, '0110')
    g5 = circuit.add_gate(g3, g4, '0110')

    return g4, g5


def add_sum3(circuit, input_labels):
    assert len(input_labels) == 3
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3] = input_labels

    x1_xor_x2 = circuit.add_gate(x1, x2, '0110')
    w0, w1 = add_stockmeyers_block(circuit, [x1_xor_x2, x2, x3])

    return w0, w1


def add_mdfa(circuit, input_labels):
    assert len(input_labels) == 5
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1_xor_x2, x2, x3, x4, x4_xor_x5] = input_labels

    #g1 = circuit.add_gate(x1, x2, '0110')
    g2 = circuit.add_gate(x2, x3, '0110')
    g3 = circuit.add_gate(x1_xor_x2, g2, '0111')
    g4 = circuit.add_gate(x1_xor_x2, x3, '0110')
    g5 = circuit.add_gate(g3, g4, '0110')
    g6 = circuit.add_gate(x4, g4, '0110')
    #g7 = circuit.add_gate(x4, x5, '0110')
    g8 = circuit.add_gate(g6, x4_xor_x5, '0010')
    g9 = circuit.add_gate(g4, x4_xor_x5, '0110')
    g10 = circuit.add_gate(g3, g8, '0110')
    #g11 = circuit.add_gate(g5, g10, '0010')

    return g9, g5, g10


def add_sum4(circuit, input_labels):
    assert len(input_labels) == 4
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x0, x1, x2, x3] = input_labels
    x4 = circuit.add_gate(x2, x3, '0110')
    x5 = circuit.add_gate(x0, x4, '0110')
    x6 = circuit.add_gate(x1, x5, '0110')
    x7 = circuit.add_gate(x3, x4, '0010')
    x8 = circuit.add_gate(x0, x6, '0100')
    x9 = circuit.add_gate(x7, x8, '0110')
    x10 = circuit.add_gate(x1, x4, '0111')
    x11 = circuit.add_gate(x9, x10, '0110')
    x12 = circuit.add_gate(x7, x11, '0010')

    return x6, x11, x12


def add_sum5(circuit, input_labels):
    assert len(input_labels) == 5
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    x1_xor_x2 = circuit.add_gate(x1, x2, '0110') #g1
    # g2 = circuit.add_gate(x2, x3, '0110')
    # g3 = circuit.add_gate(g1, g2, '0111')
    # g4 = circuit.add_gate(g1, x3, '0110')
    # g5 = circuit.add_gate(g3, g4, '0110')
    # g6 = circuit.add_gate(x4, g4, '0110')
    x4_xor_x5 = circuit.add_gate(x4, x5, '0110') # g7
    # g8 = circuit.add_gate(g6, g7, '0010')
    # g9 = circuit.add_gate(g4, g7, '0110')
    # g10 = circuit.add_gate(g3, g8, '0110')
    # g11 = circuit.add_gate(g5, g10, '0010')

    b0, a1, a1_xor_b1 = add_mdfa(circuit, [x1_xor_x2, x2, x3, x4, x4_xor_x5])
    g11 = circuit.add_gate(a1, a1_xor_b1, '0010')

    return b0, a1_xor_b1, g11


def add_sum5_suboptimal(circuit, input_labels):
    assert len(input_labels) == 5
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    w0, b1 = add_sum3(circuit, [a0, x4, x5])
    w1, w2 = add_sum2(circuit, [a1, b1])

    return w0, w1, w2


def add_sum6(circuit, input_labels):
    assert len(input_labels) == 6
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels

    a0, a1, a2 = add_sum5(circuit, [x1, x2, x3, x4, x5])
    w0, c1 = add_sum2(circuit, [a0, x6])
    w1, c2 = add_sum2(circuit, [a1, c1])
    w2 = circuit.add_gate(a2, c2, '0110')

    return w0, w1, w2


def add_sum7(circuit, input_labels):
    assert len(input_labels) == 7
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels

    a0, a1, a2 = add_sum5(circuit, [x1, x2, x3, x4, x5])
    w0, c1 = add_sum3(circuit, [a0, x6, x7])
    w1, e1 = add_sum2(circuit, [a1, c1])
    w2 = circuit.add_gate(a2, e1, '0110')

    return w0, w1, w2


def add_sum7_suboptimal(circuit, input_labels):
    assert len(input_labels) == 7
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    b0, b1 = add_sum3(circuit, [a0, x4, x5])
    c0, c1 = add_sum3(circuit, [b0, x6, x7])
    d1, d2 = add_sum3(circuit, [a1, b1, c1])

    return c0, d1, d2


def add_sum9(circuit, input_labels):
    assert len(input_labels) == 9
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9] = input_labels

    a0, a1, a2 = add_sum5(circuit, [x1, x2, x3, x4, x5])
    w0, b1, b2 = add_sum5(circuit, [a0, x6, x7, x8, x9])

    w1 = circuit.add_gate(a1, b1, '0110')
    d1 = circuit.add_gate(a1, b1, '0001')
    d2 = circuit.add_gate(a2, b2, '0110')
    d3 = circuit.add_gate(d1, d2, '0110')
    d4 = circuit.add_gate(a2, b2, '0001')

    return w0, w1, d3, d4


def add_sum9_using_mdfa(circuit, input_labels):
    assert len(input_labels) == 9
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9] = input_labels
    x1_xor_x2 = circuit.add_gate(x1, x2, '0110')
    x4_xor_x5 = circuit.add_gate(x4, x5, '0110')
    b0, a1, a1_xor_b1 = add_mdfa(circuit, [x1_xor_x2, x2, x3, x4, x4_xor_x5])
    x6_xor_x7 = circuit.add_gate(x6, x7, '0110')
    x8_xor_x9 = circuit.add_gate(x8, x9, '0110')
    f0, c1, c1_xor_d1 = add_mdfa(circuit, [x6_xor_x7, x7, b0, x8, x8_xor_x9])

    g3 = circuit.add_gate(a1_xor_b1, a1, '0111')
    g5 = circuit.add_gate(a1_xor_b1, g3, '0110')
    g6 = circuit.add_gate(a1_xor_b1, c1, '0110')
    g8 = circuit.add_gate(g6, c1_xor_d1, '0010')
    g9 = circuit.add_gate(a1_xor_b1, c1_xor_d1, '0110')
    g10 = circuit.add_gate(g3, g8, '0110')
    g11 = circuit.add_gate(g5, g10, '0010')

    return f0, g9, g10, g11


def add_sum15(circuit, input_labels):
    assert len(input_labels) == 15
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15] = input_labels

    a0, a1, a2 = add_sum7(circuit, [x1, x2, x3, x4, x5, x6, x7])
    b0, b1, b2 = add_sum7(circuit, [a0, x8, x9, x10, x11, x12, x13])
    w0, c1 = add_sum3(circuit, [b0, x14, x15])
    w1, d2 = add_sum3(circuit, [a1, b1, c1])
    w2, w3 = add_sum3(circuit, [a2, b2, d2])

    return w0, w1, w2, w3


def add_sum15_using_mdfa(circuit, input_labels):
    assert len(input_labels) == 15
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15] = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    x4_xor_x5 = circuit.add_gate(x4, x5, '0110')
    x6_xor_x7 = circuit.add_gate(x6, x7, '0110')
    b0, e1, e1_xor_f1 = add_mdfa(circuit, [x4_xor_x5, x4, a0, x6, x6_xor_x7])
    x8_xor_x9 = circuit.add_gate(x8, x9, '0110')
    x10_xor_x11 = circuit.add_gate(x10, x11, '0110')
    c0, g1, g1_xor_h1 = add_mdfa(circuit, [x8_xor_x9, x8, b0, x10, x10_xor_x11])
    x12_xor_x13 = circuit.add_gate(x12, x13, '0110')
    x14_xor_x15 = circuit.add_gate(x14, x15, '0110')
    w0, i1, i1_xor_j1 = add_mdfa(circuit, [x12_xor_x13, x12, c0, x14, x14_xor_x15])
    n1, k2, k2_xor_l2 = add_mdfa(circuit, [e1_xor_f1, e1, a1, g1, g1_xor_h1])
    w1, m2 = add_stockmeyers_block(circuit, [i1_xor_j1, i1, n1])
    w2, w3 = add_stockmeyers_block(circuit, [k2_xor_l2, k2, m2])

    return w0, w1, w2, w3


def add_sum31(circuit, input_labels):
    assert len(input_labels) == 31
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16,
     x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31] = input_labels

    a0, a1, a2 = add_sum7(circuit, [x1, x2, x3, x4, x5, x6, x7])
    b0, b1, b2 = add_sum7(circuit, [a0, x8, x9, x10, x11, x12, x13])
    c0, c1, c2 = add_sum7(circuit, [b0, x14, x15, x16, x17, x18, x19])
    d0, d1, d2 = add_sum7(circuit, [c0, x20, x21, x22, x23, x24, x25])
    w0, e1, e2 = add_sum7(circuit, [d0, x26, x27, x28, x29, x30, x31])
    w1, f2, f3 = add_sum5(circuit, [a1, b1, c1, d1, e1])
    g2, g3, g4 = add_sum5(circuit, [a2, b2, c2, d2, e2])
    w2, h3 = add_sum2(circuit, [f2, g2])
    w3, i4 = add_sum3(circuit, [f3, g3, h3])
    w4 = f'z{len(circuit.gates)}'
    circuit.gates[w4] = (g4, i4, '0110')

    return w0, w1, w2, w3, w4


def check_sum_circuit(circuit):
    truth_tables = circuit.get_truth_tables()
    n = len(circuit.input_labels)

    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = sum(truth_tables[circuit.outputs[d]][i] * (2 ** d) for d in range(len(circuit.outputs)))
        assert s == sum(x)


def check_various_sum_circuits():
    c = Circuit(input_labels=[f'x{i}' for i in range(2)], gates={})
    c.outputs = add_sum2(c, c.input_labels)
    check_sum_circuit(c)

    c = Circuit(input_labels=[f'x{i}' for i in range(3)], gates={})
    c.outputs = add_sum3(c, c.input_labels)
    check_sum_circuit(c)

    c = Circuit(input_labels=[f'x{i}' for i in range(4)], gates={})
    c.outputs = add_sum4(c, c.input_labels)
    check_sum_circuit(c)

    c = Circuit(input_labels=[f'x{i}' for i in range(5)], gates={})
    c.outputs = add_sum5(c, c.input_labels)
    check_sum_circuit(c)

    c = Circuit(input_labels=[f'x{i}' for i in range(5)], gates={})
    c.outputs = add_sum5_suboptimal(c, c.input_labels)
    check_sum_circuit(c)

    c = Circuit(input_labels=[f'x{i}' for i in range(6)], gates={})
    c.outputs = add_sum6(c, c.input_labels)
    check_sum_circuit(c)

    c = Circuit(input_labels=[f'x{i}' for i in range(7)], gates={})
    c.outputs = add_sum7(c, c.input_labels)
    check_sum_circuit(c)

    c = Circuit(input_labels=[f'x{i}' for i in range(7)], gates={})
    c.outputs = add_sum7_suboptimal(c, c.input_labels)
    check_sum_circuit(c)

    c = Circuit(input_labels=[f'x{i}' for i in range(9)], gates={})
    c.outputs = add_sum9(c, c.input_labels)
    check_sum_circuit(c)

    c = Circuit(input_labels=[f'x{i}' for i in range(15)], gates={})
    c.outputs = add_sum15(c, c.input_labels)
    check_sum_circuit(c)

    c = Circuit(input_labels=[f'x{i}' for i in range(15)], gates={})
    c.outputs = add_sum15_using_mdfa(c, c.input_labels)
    check_sum_circuit(c)


    # c_eff = Circuit(input_labels=[f'x{i}' for i in range(1, 32)], gates={})
    # c_eff.outputs = add_sum31(c_eff, c_eff.input_labels)
    # check_sum_circuit(c_eff)


def add_matrix_multiplication2(circuit, input_labels):
    assert len(input_labels) == 8
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [a11, a12, a21, a22, b11, b12, b21, b22] = input_labels

    e1111 = circuit.add_gate(a11, b11, '0001')
    e1221 = circuit.add_gate(a12, b21, '0001')
    c11 = circuit.add_gate(e1111, e1221, '0110')

    e1112 = circuit.add_gate(a11, b12, '0001')
    e1222 = circuit.add_gate(a12, b22, '0001')
    c12 = circuit.add_gate(e1112, e1222, '0110')

    e2111 = circuit.add_gate(a21, b11, '0001')
    e2221 = circuit.add_gate(a22, b21, '0001')
    c21 = circuit.add_gate(e2111, e2221, '0110')

    e2112 = circuit.add_gate(a21, b12, '0001')
    e2222 = circuit.add_gate(a22, b22, '0001')
    c22 = circuit.add_gate(e2112, e2222, '0110')

    return [c11, c12, c21, c22]


def add_matrix_multiplication(circuit, input_labels, n):
    assert len(input_labels) == 2 * n * n
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    a = [list(input_labels[i * n: (i + 1) * n]) for i in range(n)]
    b = [list(input_labels[n * n + i * n: n * n + (i + 1) * n]) for i in range(n)]

    outputs = []
    for i, j in product(range(n), repeat=2):
        products = [circuit.add_gate(a[i][k], b[k][j], '0001') for k in range(n)]
        outputs.append(add_binary_sum(circuit, products, '0110'))

    return outputs


def add_integer_multiplication3(circuit, input_labels):
    assert len(input_labels) == 6
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [a0, a1, a2, b0, b1, b2] = input_labels

    p00 = circuit.add_gate(a0, b0, '0001')
    p01 = circuit.add_gate(a0, b1, '0001')
    p02 = circuit.add_gate(a0, b2, '0001')
    p10 = circuit.add_gate(a1, b0, '0001')
    p11 = circuit.add_gate(a1, b1, '0001')
    p12 = circuit.add_gate(a1, b2, '0001')
    p20 = circuit.add_gate(a2, b0, '0001')
    p21 = circuit.add_gate(a2, b1, '0001')
    p22 = circuit.add_gate(a2, b2, '0001')

    c1, c2 = add_sum2(circuit, [p01, p10])
    d2, d3, d4 = add_sum4(circuit, [p02, p11, p20, c2])
    e3, e4 = add_sum3(circuit, [p12, p21, d3])
    f4, f5 = add_sum3(circuit, [p22, d4, e4])
    # q1 = circuit.add_gate(p22, d4, '0110')
    # q2 = circuit.add_gate(e4, q1, '0110')
    # q3 = circuit.add_gate(e4, q2, '0010')
    # q4 = circuit.add_gate(d4, q3, '0110')

    # circuit.outputs = [p00, c1, d2, e3, q2, q4]
    return p00, c1, d2, e3, f4, f5


if __name__ == '__main__':
    n = 3
    inputs = [f'a-{i}-{j}' for i, j in product(range(n), repeat=2)] + [f'b-{i}-{j}' for i, j in product(range(n), repeat=2)]

    circuit = Circuit(input_labels=inputs, gates={})
    circuit.outputs = add_matrix_multiplication(circuit, inputs, 3)
    # print(circuit)
    improve_circuit(circuit)



