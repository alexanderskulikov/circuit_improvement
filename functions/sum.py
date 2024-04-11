from core.circuit import Circuit
from itertools import product


def add_sum2(circuit, input_labels):
    assert len(input_labels) == 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2] = input_labels
    g1 = circuit.add_gate(x1, x2, '0110')
    g2 = circuit.add_gate(x1, x2, '0001')

    return g1, g2


def add_sum3(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x1, x2, x3 = input_labels

    g1 = circuit.add_gate(x1, x2, '0110')
    g2 = circuit.add_gate(g1, x3, '0110')
    g3 = circuit.add_gate(x1, x2, '0001')
    g4 = circuit.add_gate(g1, x3, '0001')
    g5 = circuit.add_gate(g3, g4, '0110')
    return g2, g5


# given x1, x2, and (x2 oplus x3), computes the binary representation
# of (x1 + x2 + x3)
def add_stockmeyer_block(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x1, x2, x23 = input_labels

    w0 = circuit.add_gate(x1, x23, '0110')

    g2 = circuit.add_gate(x2, x23, '0010')
    g3 = circuit.add_gate(x1, x23, '0001')
    w1 = circuit.add_gate(g2, g3, '0110')
    return w0, w1


def add_sum4(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4] = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    w0, b1 = add_sum2(circuit, [a0, x4])
    w1, w2 = add_sum2(circuit, [a1, b1])

    return w0, w1, w2


def add_sum5_size11(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    g1 = circuit.add_gate(x1, x2, '0110')
    g2 = circuit.add_gate(x2, x3, '0110')
    g3 = circuit.add_gate(g1, g2, '0111')
    g4 = circuit.add_gate(g1, x3, '0110')
    g5 = circuit.add_gate(g3, g4, '0110')
    g6 = circuit.add_gate(x4, g4, '0110')
    g7 = circuit.add_gate(x4, x5, '0110')
    g8 = circuit.add_gate(g6, g7, '0010')
    g9 = circuit.add_gate(g4, g7, '0110')
    g10 = circuit.add_gate(g3, g8, '0110')
    g11 = circuit.add_gate(g5, g10, '0010')

    return g9, g10, g11


def add_sum5_size11_via_mdfa(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x1, x2, x3, x4, x5 = input_labels

    x23 = circuit.add_gate(x2, x3, '0110')
    x45 = circuit.add_gate(x4, x5, '0110')
    w0, c1, c12 = add_mdfa(circuit, [x1, x2, x23, x4, x45])
    w2 = circuit.add_gate(c1, c12, '0010')

    return w0, c12, w2


def add_sum5_size12(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    w0, b1 = add_sum3(circuit, [a0, x4, x5])
    w1, w2 = add_sum2(circuit, [a1, b1])

    return w0, w1, w2


def add_sum6_size16(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels

    a0, a1, a2 = add_sum5_size11(circuit, [x1, x2, x3, x4, x5])
    w0, c1 = add_sum2(circuit, [a0, x6])
    w1, c2 = add_sum2(circuit, [a1, c1])
    w2 = circuit.add_gate(a2, c2, '0110')

    return w0, w1, w2


def add_sum7_size19(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels

    a0, a1, a2 = add_sum5_size11(circuit, [x1, x2, x3, x4, x5])
    w0, c1 = add_sum3(circuit, [a0, x6, x7])
    w1, e1 = add_sum2(circuit, [a1, c1])
    w2 = circuit.add_gate(a2, e1, '0110')

    return w0, w1, w2


def add_sum8_size25(circuit, input_labels):
    assert len(input_labels) == 8
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x1, x2, x3, x4, x5, x6, x7, x8 = input_labels

    x12 = circuit.add_gate(x1, x2, '0110')
    x34 = circuit.add_gate(x3, x4, '0110')
    x56 = circuit.add_gate(x5, x6, '0110')
    x78 = circuit.add_gate(x7, x8, '0110')
    a0, a1, a12 = add_simplified_mdfa(circuit, [x1, x12, x3, x34])
    w0, b1, b12 = add_mdfa(circuit, [a0, x5, x56, x7, x78])
    w1, c2, c23 = add_simplified_mdfa(circuit, [a1, a12, b1, b12])
    w3 = circuit.add_gate(c2, c23, '0010')

    return w0, w1, c23, w3


def add_sum9_size27(circuit, input_labels):
    assert len(input_labels) == 9
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9] = input_labels

    a0, a1, a2 = add_sum5_size11(circuit, [x1, x2, x3, x4, x5])
    w0, b1, b2 = add_sum5_size11(circuit, [a0, x6, x7, x8, x9])

    w1 = circuit.add_gate(a1, b1, '0110')
    d1 = circuit.add_gate(a1, b1, '0001')
    d2 = circuit.add_gate(a2, b2, '0110')
    d3 = circuit.add_gate(d1, d2, '0110')
    d4 = circuit.add_gate(a2, b2, '0001')

    return w0, w1, d3, d4


def add_sum10_size31(circuit, input_labels):
    assert len(input_labels) == 10
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = input_labels

    x34 = circuit.add_gate(x3, x4, '0110')
    x56 = circuit.add_gate(x5, x6, '0110')
    x78 = circuit.add_gate(x7, x8, '0110')
    x910 = circuit.add_gate(x9, x10, '0110')

    a0, a1 = add_sum2(circuit, [x1, x2])
    b0, b1, b12 = add_mdfa(circuit, [a0, x3, x34, x5, x56])
    c0, c1, c12 = add_mdfa(circuit, [b0, x7, x78, x9, x910])
    d1, d2, d23 = add_mdfa(circuit, [a1, b1, b12, c1, c12])
    w3 = circuit.add_gate(d2, d23, '0010')

    return c0, d1, d23, w3


def add_sum11_size34(circuit, input_labels):
    assert len(input_labels) == 11
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11 = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])

    x45 = circuit.add_gate(x4, x5, '0110')
    x67 = circuit.add_gate(x6, x7, '0110')
    c0, c1, c12 = add_mdfa(circuit, [a0, x4, x45, x6, x67])

    x89 = circuit.add_gate(x8, x9, '0110')
    x1011 = circuit.add_gate(x10, x11, '0110')
    w0, d1, d12 = add_mdfa(circuit, [c0, x8, x89, x10, x1011])

    w1, e2, e23 = add_mdfa(circuit, [a1, c1, c12, d1, d12])
    w3 = circuit.add_gate(e2, e23, '0010')

    return w0, w1, e23, w3


def add_sum12_size41(circuit, input_labels):
    assert len(input_labels) == 12
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12 = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])

    x45 = circuit.add_gate(x4, x5, '0110')
    x67 = circuit.add_gate(x6, x7, '0110')
    c0, c1, c12 = add_mdfa(circuit, [a0, x4, x45, x6, x67])

    x89 = circuit.add_gate(x8, x9, '0110')
    x1011 = circuit.add_gate(x10, x11, '0110')
    d0, d1, d12 = add_mdfa(circuit, [c0, x8, x89, x10, x1011])

    w0, e1 = add_sum2(circuit, [d0, x12])

    f1, f2, f23 = add_mdfa(circuit, [a1, c1, c12, d1, d12])
    w1, h2 = add_sum2(circuit, [e1, f1])

    w2, w3 = add_stockmeyer_block(circuit, [h2, f2, f23])

    return w0, w1, w2, w3


def add_sum13_size43(circuit, input_labels):
    assert len(input_labels) == 13
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13 = input_labels

    x67 = circuit.add_gate(x6, x7, '0110')
    x89 = circuit.add_gate(x8, x9, '0110')
    x1011 = circuit.add_gate(x10, x11, '0110')
    x1213 = circuit.add_gate(x12, x13, '0110')

    a0, a1, a2 = add_sum5_size11(circuit, [x1, x2, x3, x4, x5])
    b0, b1, b12 = add_mdfa(circuit, [a0, x6, x67, x8, x89])
    w0, c1, c12 = add_mdfa(circuit, [b0, x10, x1011, x12, x1213])
    w1, d2, d23 = add_mdfa(circuit, [a1, b1, b12, c1, c12])
    w2, w3 = add_stockmeyer_block(circuit, [a2, d2, d23])

    return w0, w1, w2, w3


def add_mdfa(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    z, x1, xy1, x2, xy2 = input_labels

    g1 = circuit.add_gate(x1, z, '0110')
    g2 = circuit.add_gate(xy1, g1, '0111')
    g3 = circuit.add_gate(xy1, z, '0110')
    g4 = circuit.add_gate(g2, g3, '0110')
    g5 = circuit.add_gate(x2, g3, '0110')
    g6 = circuit.add_gate(g3, xy2, '0110')
    g7 = circuit.add_gate(g5, xy2, '0010')
    g8 = circuit.add_gate(g2, g7, '0110')

    return g6, g4, g8


# an MDFA block with z=0
def add_simplified_mdfa(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x1, xy1, x2, xy2 = input_labels

    g2 = circuit.add_gate(xy1, x1, '0111')
    g4 = circuit.add_gate(g2, xy1, '0110')
    g5 = circuit.add_gate(x2, xy1, '0110')
    g6 = circuit.add_gate(xy1, xy2, '0110')
    g7 = circuit.add_gate(g5, xy2, '0010')
    g8 = circuit.add_gate(g2, g7, '0110')

    return g6, g4, g8


def add_sum14_size48(circuit, input_labels):
    assert len(input_labels) == 14
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15 = input_labels

    x45 = circuit.add_gate(x4, x5, '0110')
    x67 = circuit.add_gate(x6, x7, '0110')
    x89 = circuit.add_gate(x8, x9, '0110')
    x1011 = circuit.add_gate(x10, x11, '0110')
    x1213 = circuit.add_gate(x12, x13, '0110')
    x1415 = circuit.add_gate(x14, x15, '0110')

    a0, a1 = add_sum2(circuit, [x2, x3])
    b0, b1, b12 = add_mdfa(circuit, [a0, x4, x45, x6, x67])
    c0, c1, c12 = add_mdfa(circuit, [b0, x8, x89, x10, x1011])
    w0, d1, d12 = add_mdfa(circuit, [c0, x12, x1213, x14, x1415])
    e1, e2, e23 = add_mdfa(circuit, [a1, b1, b12, c1, c12])
    w1, f2 = add_stockmeyer_block(circuit, [e1, d1, d12])
    w2, w3 = add_stockmeyer_block(circuit, [f2, e2, e23])

    return w0, w1, w2, w3


def add_sum15_size51(circuit, input_labels):
    assert len(input_labels) == 15
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15 = input_labels

    x45 = circuit.add_gate(x4, x5, '0110')
    x67 = circuit.add_gate(x6, x7, '0110')
    x89 = circuit.add_gate(x8, x9, '0110')
    x1011 = circuit.add_gate(x10, x11, '0110')
    x1213 = circuit.add_gate(x12, x13, '0110')
    x1415 = circuit.add_gate(x14, x15, '0110')

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    b0, b1, b12 = add_mdfa(circuit, [a0, x4, x45, x6, x67])
    c0, c1, c12 = add_mdfa(circuit, [b0, x8, x89, x10, x1011])
    w0, d1, d12 = add_mdfa(circuit, [c0, x12, x1213, x14, x1415])
    e1, e2, e23 = add_mdfa(circuit, [a1, b1, b12, c1, c12])
    w1, f2 = add_stockmeyer_block(circuit, [e1, d1, d12])
    w2, w3 = add_stockmeyer_block(circuit, [f2, e2, e23])

    return w0, w1, w2, w3


def add_sum16_size59(circuit, input_labels):
    assert len(input_labels) == 16
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16 = input_labels

    q0, q1, q2, q3 = add_sum15_size51(circuit, input_labels[:-1])
    w0, a1 = add_sum2(circuit, [q0, x16])
    w1, b2 = add_sum2(circuit, [q1, a1])
    w2, c3 = add_sum2(circuit, [q2, b2])
    w3, w4 = add_sum2(circuit, [q3, c3])

    return w0, w1, w2, w3, w4


def add_sum31(circuit, input_labels):
    assert len(input_labels) == 31
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16,
     x17, x18, x19, x20, x21, x22, x23, x24, x25, x26, x27, x28, x29, x30, x31] = input_labels

    a0, a1, a2 = add_sum7_size19(circuit, [x1, x2, x3, x4, x5, x6, x7])
    b0, b1, b2 = add_sum7_size19(circuit, [a0, x8, x9, x10, x11, x12, x13])
    c0, c1, c2 = add_sum7_size19(circuit, [b0, x14, x15, x16, x17, x18, x19])
    d0, d1, d2 = add_sum7_size19(circuit, [c0, x20, x21, x22, x23, x24, x25])
    w0, e1, e2 = add_sum7_size19(circuit, [d0, x26, x27, x28, x29, x30, x31])
    w1, f2, f3 = add_sum5_size11(circuit, [a1, b1, c1, d1, e1])
    g2, g3, g4 = add_sum5_size11(circuit, [a2, b2, c2, d2, e2])
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
        assert s == sum(x), f'Input: {x}, sum: {sum(x)}, s: {s}, output: {[truth_tables[circuit.outputs[d]][i] for d in range(len(circuit.outputs))]}'


def add_sum(circuit, input_labels):
    n = len(input_labels)
    if n == 2:
        return add_sum2(circuit, input_labels)
    if n == 3:
        return add_sum3(circuit, input_labels)
    if n == 4:
        return add_sum4(circuit, input_labels)
    if n == 5:
        return add_sum5_size11(circuit, input_labels)
    if n == 6:
        return add_sum6_size16(circuit, input_labels)
    if n == 7:
        return add_sum7_size19(circuit, input_labels)
    if n == 8:
        return add_sum8_size25(circuit, input_labels)
    if n == 9:
        return add_sum9_size27(circuit, input_labels)
    if n == 10:
        return add_sum10_size31(circuit, input_labels)
    if n == 11:
        return add_sum11_size34(circuit, input_labels)
    if n == 12:
        return add_sum12_size41(circuit, input_labels)
    if n == 13:
        return add_sum13_size43(circuit, input_labels)
    if n == 14:
        return add_sum14_size48(circuit, input_labels)
    if n == 15:
        return add_sum15_size51(circuit, input_labels)
    if n == 16:
        return add_sum16_size59(circuit, input_labels)

    assert False, 'not yet implemented'


# if __name__ == '__main__':
#     ckt = Circuit(input_labels=[f'x{i}' for i in range(1, 17)])
#     ckt.outputs = add_sum16_size59(ckt, ckt.input_labels)
#     check_sum_circuit(ckt)
#     ckt.save_to_file('sum16_size59', extension='ckt')

