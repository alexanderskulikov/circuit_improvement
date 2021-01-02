from circuit import Circuit
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

    [x1, x2, x3] = input_labels

    g1 = circuit.add_gate(x1, x2, '0110')
    g2 = circuit.add_gate(x2, x3, '0110')
    g3 = circuit.add_gate(g1, g2, '0111')
    g4 = circuit.add_gate(g1, x3, '0110')
    g5 = circuit.add_gate(g3, g4, '0110')

    return g4, g5


def add_sum4(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4] = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    w0, b1 = add_sum2(circuit, [a0, x4])
    w1, w2 = add_sum2(circuit, [a1, b1])

    return w0, w1, w2


def add_sum5(circuit, input_labels):
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


def add_sum5_suboptimal(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    w0, b1 = add_sum3(circuit, [a0, x4, x5])
    w1, w2 = add_sum2(circuit, [a1, b1])

    return w0, w1, w2


def add_sum6(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels

    a0, a1, a2 = add_sum5(circuit, [x1, x2, x3, x4, x5])
    w0, c1 = add_sum2(circuit, [a0, x6])
    w1, c2 = add_sum2(circuit, [a1, c1])
    w2 = circuit.add_gate(a2, c2, '0110')

    return w0, w1, w2


def add_sum7(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels

    a0, a1, a2 = add_sum5(circuit, [x1, x2, x3, x4, x5])
    w0, c1 = add_sum3(circuit, [a0, x6, x7])
    w1, e1 = add_sum2(circuit, [a1, c1])
    w2 = circuit.add_gate(a2, e1, '0110')

    return w0, w1, w2


def add_sum7_suboptimal(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    b0, b1 = add_sum3(circuit, [a0, x4, x5])
    c0, c1 = add_sum3(circuit, [b0, x6, x7])
    d1, d2 = add_sum3(circuit, [a1, b1, c1])

    return c0, d1, d2


def add_sum8_1(circuit, input_labels):
    assert len(input_labels) == 8
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8] = input_labels

    a0, a1, a2 = add_sum7(circuit, [x1, x2, x3, x4, x5, x6, x7])
    b0, b1 = add_sum2(circuit, [a0, x8])
    c0, c1 = add_sum2(circuit, [b1, a1])
    d0, d1 = add_sum2(circuit, [c1, a2])

    return b0, c0, d0, d1


def add_sum8_2(circuit, input_labels):
    assert len(input_labels) == 8
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8] = input_labels

    a0, a1, a2 = add_sum6(circuit, [x1, x2, x3, x4, x5, x6])
    b0, b1 = add_sum3(circuit, [a0, x7, x8])
    c0, c1 = add_sum2(circuit, [b1, a1])
    d0, d1 = add_sum2(circuit, [c1, a2])

    return b0, c0, d0, d1


def add_sum9(circuit, input_labels):
    assert len(input_labels) == 9
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9] = input_labels

    a0, a1, a2 = add_sum5(circuit, [x1, x2, x3, x4, x5])
    w0, b1, b2 = add_sum5(circuit, [a0, x6, x7, x8, x9])

    w1 = circuit.add_gate(a1, b1, '0110')
    d1 = circuit.add_gate(a1, b1, '0001')
    d2 = circuit.add_gate(a2, b2, '0110')
    d3 = circuit.add_gate(d1, d2, '0110')
    d4 = circuit.add_gate(a2, b2, '0001')

    return w0, w1, d3, d4


def add_sum10(circuit, input_labels):
    assert len(input_labels) == 10
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10] = input_labels
    z1 = circuit.add_gate(x2, x3, '0110')
    z36 = circuit.add_gate(x1, x2, '0110')
    z37 = circuit.add_gate(x3, z36, '0110')
    z5 = circuit.add_gate(x4, z37, '0110')
    z6 = circuit.add_gate(x4, x5, '0110')
    z7 = circuit.add_gate(z5, z6, '0010')
    z8 = circuit.add_gate(z6, z37, '0110')
    z34 = circuit.add_gate(z1, z36, '0111')
    z9 = circuit.add_gate(z7, z34, '0110')
    z11 = circuit.add_gate(z8, x6, '0110')
    z12 = circuit.add_gate(z8, x6, '0001')
    z13 = circuit.add_gate(z9, z12, '0110')
    z14 = circuit.add_gate(z9, z12, '0001')
    z16 = circuit.add_gate(z11, x7, '0110')
    z17 = circuit.add_gate(x7, x8, '0110')
    z18 = circuit.add_gate(z16, z17, '0111')
    z19 = circuit.add_gate(z16, x8, '0110')
    z20 = circuit.add_gate(z18, z19, '0110')
    z21 = circuit.add_gate(x9, z19, '0110')
    z22 = circuit.add_gate(x9, x10, '0110')
    z23 = circuit.add_gate(z21, z22, '0010')
    z24 = circuit.add_gate(z19, z22, '0110')
    z25 = circuit.add_gate(z18, z23, '0110')
    z26 = circuit.add_gate(z20, z25, '0010')
    z27 = circuit.add_gate(z25, z13, '0110')
    z28 = circuit.add_gate(z25, z13, '0001')
    z30 = circuit.add_gate(z26, z28, '0110')
    z35 = circuit.add_gate(z30, z14, '0110')
    z38 = circuit.add_gate(z34, z37, '0110')
    z39 = circuit.add_gate(z9, z38, '1011')
    z40 = circuit.add_gate(z35, z39, '1001')
    z41 = circuit.add_gate(z30, z40, '0010')

    return z24, z27, z40, z41


def add_sum10_suboptimal(circuit, input_labels):
    assert len(input_labels) == 10
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10] = input_labels

    a0, a1, a2 = add_sum6(circuit, [x1, x2, x3, x4, x5, x6])
    w0, b1, b2 = add_sum5(circuit, [a0, x7, x8, x9, x10])
    w1, c1 = add_sum2(circuit, [b1, a1])
    w2, w3 = add_sum3(circuit, [a2, b2, c1])

    return w0, w1, w2, w3


def add_sum15(circuit, input_labels):
    assert len(input_labels) == 15
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15] = input_labels

    a0, a1, a2 = add_sum7(circuit, [x1, x2, x3, x4, x5, x6, x7])
    b0, b1, b2 = add_sum7(circuit, [a0, x8, x9, x10, x11, x12, x13])
    w0, c1 = add_sum3(circuit, [b0, x14, x15])
    w1, d2 = add_sum3(circuit, [a1, b1, c1])
    w2, w3 = add_sum3(circuit, [a2, b2, d2])

    return w0, w1, w2, w3


def add_mid_sum15(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [b0, x14, x15, a1, b1, a2, b2] = input_labels

    w0, c1 = add_sum3(circuit, [b0, x14, x15])
    w1, d2 = add_sum3(circuit, [a1, b1, c1])
    w2, w3 = add_sum3(circuit, [a2, b2, d2])

    return w0, w1, w2, w3

def add_norm_mdfa(circuit, input_labels):
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


def add_sum15_51(circuit, input_labels):
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


def add_sum15_using_mdfa2(circuit, input_labels):
    assert len(input_labels) == 15
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15] = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    x4_xor_x5 = circuit.add_gate(x4, x5, '0110')
    x6_xor_x7 = circuit.add_gate(x6, x7, '0110')
    x8_xor_x9 = circuit.add_gate(x8, x9, '0110')
    x10_xor_x11 = circuit.add_gate(x10, x11, '0110')

    #c0, n1, k2, k2_xor_l2 = add_3mdfa_new(circuit, [])

    b0, e1, e1_xor_f1 = add_mdfa(circuit, [x4_xor_x5, x4, a0, x6, x6_xor_x7])
    c0, g1, g1_xor_h1 = add_mdfa(circuit, [x8_xor_x9, x8, b0, x10, x10_xor_x11])
    n1, k2, k2_xor_l2 = add_mdfa(circuit, [e1_xor_f1, e1, a1, g1, g1_xor_h1])

    x12_xor_x13 = circuit.add_gate(x12, x13, '0110')
    x14_xor_x15 = circuit.add_gate(x14, x15, '0110')
    w0, i1, i1_xor_j1 = add_mdfa(circuit, [x12_xor_x13, x12, c0, x14, x14_xor_x15])
    w1, m2 = add_stockmeyers_block(circuit, [i1_xor_j1, i1, n1])
    w2, w3 = add_stockmeyers_block(circuit, [k2_xor_l2, k2, m2])

    return w0, w1, w2, w3


def add_3mdfa_new(circuit, input_labels):
    assert len(input_labels) == 10
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10] = input_labels
    a5 = circuit.add_gate(x3, x1, '0110')
    a10 = circuit.add_gate(x4, a5, '0110')
    z5 = circuit.add_gate(a10, x5, '0010')
    a6 = circuit.add_gate(z5, a5, '0110')
    a7 = circuit.add_gate(x2, x3, '1001')
    a8 = circuit.add_gate(x1, a7, '0100')
    a9 = circuit.add_gate(z5, a8, '1001')
    z6 = circuit.add_gate(a5, x5, '0110')
    z8 = circuit.add_gate(x6, x7, '0110')
    z9 = circuit.add_gate(z6, z8, '0111')
    z10 = circuit.add_gate(z6, x7, '0110')
    z11 = circuit.add_gate(z9, z10, '0110')
    z12 = circuit.add_gate(x8, z10, '0110')
    z13 = circuit.add_gate(z12, x9, '0010')
    z14 = circuit.add_gate(z10, x9, '0110')
    z15 = circuit.add_gate(z9, z13, '0110')
    z17 = circuit.add_gate(x10, a6, '0111')
    z18 = circuit.add_gate(x10, a9, '0110')
    z19 = circuit.add_gate(z17, z18, '0110')
    z20 = circuit.add_gate(z11, z18, '0110')
    z21 = circuit.add_gate(z20, z15, '0010')
    z22 = circuit.add_gate(z18, z15, '0110')
    z23 = circuit.add_gate(z17, z21, '0110')


    return z14, z22, z19, z23


def add_3mdfa(circuit, input_labels):
    assert len(input_labels) == 10
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [i0, i1, x1ry1, y1, x2ry2, y2, x3ry3, y3, x4ry4, y4] = input_labels
    a0, b1, b2rb1 = add_mdfa(circuit, [x1ry1, y1, i0, x2ry2, y2])
    w0, c1, c2rc1 = add_mdfa(circuit, [x3ry3, y3, a0, x4ry4, y4])
    w1, d1, d2rd1 = add_mdfa(circuit, [b2rb1, b1, i1, c2rc1, c1])

    return w0, w1, d1, d2rd1

def add_mdfasbsb(circuit, input_labels):
    assert len(input_labels) == 7
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [e1_xor_f1, e1, a1, g1, g1_xor_h1, i1_xor_j1, i1] = input_labels
    n1, k2, k2_xor_l2 = add_mdfa(circuit, [e1_xor_f1, e1, a1, g1, g1_xor_h1])
    w1, m2 = add_stockmeyers_block(circuit, [i1_xor_j1, i1, n1])
    w2, w3 = add_stockmeyers_block(circuit, [k2_xor_l2, k2, m2])

    return w1, w2, w3


def add_mdfasb(circuit, input_labels):
    assert len(input_labels) == 7
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x0, x1, x2, x3, x4, x5, x6] = input_labels
    a0, b1, b2 = add_mdfa(circuit, [x0, x1, x2, x3, x4])
    w0, c1 = add_stockmeyers_block(circuit, [x5, x6, a0])

    return b1, b2, w0, c1


def add_sb_mdfa(circuit, input_labels):
    assert len(input_labels) == 10
    for input in input_labels:
        assert input in circuit.input_labels or input in circuit.gates

    [x0, x1, x2, x3, x4, x5, x6, x7, x8, in1] = input_labels
    a0, b1, b2 = add_mdfa(circuit, [x0, x1, x2, x3, x4])
    w0, c1, c2 = add_mdfa(circuit, [a0, x5, x6, x7, x8])
    w1, out1, out2 = add_mdfa(circuit, [b2, b1, in1, c2, c1])

    return w0, w1, out1, out2

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

def add_sum31(circuit, input_labels):
    assert len(input_labels) == 31
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

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


def add_532_for31(circuit, input_labels):
    assert len(input_labels) == 10
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [a1, b1, c1, d1, e1, a2, b2, c2, d2, e2] = input_labels

    g2, g3, g4 = add_sum5(circuit, [a2, b2, c2, d2, e2])
    w1, f2, f3 = add_sum5(circuit, [a1, b1, c1, d1, e1])
    w2, h3 = add_sum2(circuit, [f2, g2])
    w3, i4 = add_sum3(circuit, [f3, g3, h3])
    w4 = f'z{len(circuit.gates)}'
    circuit.gates[w4] = (g4, i4, '0110')

    return w1, w2, w3, w4


def add_532_for31_imp(circuit, input_labels):
    assert len(input_labels) == 10
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10] = input_labels
    z0 = circuit.add_gate(x1, x2, '0110')
    z1 = circuit.add_gate(x2, x3, '0110')
    z2 = circuit.add_gate(z0, z1, '0111')
    z3 = circuit.add_gate(z0, x3, '0110')
    z5 = circuit.add_gate(x4, z3, '0110')
    z6 = circuit.add_gate(x4, x5, '0110')
    z7 = circuit.add_gate(z5, z6, '0010')
    z8 = circuit.add_gate(z3, z6, '0110')
    z11 = circuit.add_gate(x6, x7, '0110')
    z12 = circuit.add_gate(x7, x8, '0110')
    z13 = circuit.add_gate(z11, z12, '0111')
    z14 = circuit.add_gate(z11, x8, '0110')
    z15 = circuit.add_gate(z13, z14, '0110')
    z16 = circuit.add_gate(x9, z14, '0110')
    z17 = circuit.add_gate(x9, x10, '0110')
    z18 = circuit.add_gate(z16, z17, '0010')
    z19 = circuit.add_gate(z14, z17, '0110')
    z20 = circuit.add_gate(z13, z18, '0110')
    z21 = circuit.add_gate(z15, z20, '0010')
    b5 = circuit.add_gate(z7, z2, '0110')
    a6 = circuit.add_gate(z3, z2, '1001')
    b6 = circuit.add_gate(a6, b5, '0111')
    z23 = circuit.add_gate(b5, z19, '0001')
    z25 = circuit.add_gate(z20, z23, '0110')
    b7 = circuit.add_gate(z25, b6, '1001')
    z22 = circuit.add_gate(b5, z19, '0110')
    b8 = circuit.add_gate(z20, b7, '0010')
    z29 = circuit.add_gate(z21, b8, '0110')

    return z8, z22, b7, z29


def add_75(circuit, input_labels):
    assert len(input_labels) == 11
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11] = input_labels

    a0, a1, a2 = add_sum7(circuit, [x1, x2, x3, x4, x5, x6, x7])
    w1, f2, f3 = add_sum5(circuit, [a0, x8, x9, x10, x11])

    return a1, a2, w1, f2, f3


def add_77(circuit, input_labels):
    assert len(input_labels) == 13
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13] = input_labels

    a0, a1, a2 = add_sum7(circuit, [x1, x2, x3, x4, x5, x6, x7])
    b0, b1, b2 = add_sum7(circuit, [x8, x9, x10, x11, x12, x13, a0])

    return a1, a2, b0, b1, b2


def add_775(circuit, input_labels):
    assert len(input_labels) == 16
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, c1, d1, e1] = input_labels

    a0, a1, a2 = add_sum7(circuit, [x1, x2, x3, x4, x5, x6, x7])
    b0, b1, b2 = add_sum7(circuit, [a0, x8, x9, x10, x11, x12, x13])
    w1, f2, f3 = add_sum5(circuit, [a1, b1, c1, d1, e1])

    return a2, b0, b2, w1, f2, f3


def add_773(circuit, input_labels):
    assert len(input_labels) == 14
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, c1] = input_labels

    a0, a1, a2 = add_sum7(circuit, [x1, x2, x3, x4, x5, x6, x7])
    b0, b1, b2 = add_sum7(circuit, [a0, x8, x9, x10, x11, x12, x13])
    w1, d2 = add_sum3(circuit, [a1, b1, c1])

    return a2, b0, b2, w1, d2


def add_summ22(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4] = input_labels

    z0 = circuit.add_gate(x2, x4, '0110')
    b4 = circuit.add_gate(x2, x4, '0001')
    b5 = circuit.add_gate(x3, b4, '0110')
    b6 = circuit.add_gate(x1, b4, '1001')
    b8 = circuit.add_gate(b5, b6, '1110')
    a9 = circuit.add_gate(x3, b8, '1001')
    b7 = circuit.add_gate(x3, b6, '1001')

    return z0, b7, a9


def add_sum6new(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    b0, b1 = add_sum3(circuit, [x4, x5, x6])
    c0, c1, c2 = add_summ22(circuit,[a1, a0, b1, b0])

    return c0, c1, c2

def add_sum7new(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x0, x1, x2, x3, x4, x5, x6] = input_labels

    b1 = circuit.add_gate(x0, x1, '0110')
    b2 = circuit.add_gate(b1, x2, '0110')
    b3 = circuit.add_gate(b2, x3, '0110')
    b4 = circuit.add_gate(b3, x4, '0110')
    b5 = circuit.add_gate(b4, x5, '0110')
    b6 = circuit.add_gate(b5, x6, '0110')

    a7 = circuit.add_gate(x0, b2, '0110')
    a8 = circuit.add_gate(b2, b4, '0110')
    a9 = circuit.add_gate(b4, b6, '0110')
    a10 = circuit.add_gate(b1, a7, '1000')
    a11 = circuit.add_gate(b3, a8, '1000')
    a12 = circuit.add_gate(b5, a9, '1101')
    a13 = circuit.add_gate(a8, a10, '0110')
    a14 = circuit.add_gate(b2, a10, '1001')
    a15 = circuit.add_gate(a11, a12, '0110')
    a16 = circuit.add_gate(a11, a13, '0110')
    a17 = circuit.add_gate(a14, a15, '0110')
    a18 = circuit.add_gate(a15, a16, '0111')
    a19 = circuit.add_gate(a17, a18, '0110')

    return b6, a17, a19


def add_sum7ad(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x0, x1, x2, x3, x4, x5, x6] = input_labels

    a7 = circuit.add_gate(x0, x2, '0110')
    a8 = circuit.add_gate(x2, x4, '0110')
    a9 = circuit.add_gate(x4, x6, '0110')
    a10 = circuit.add_gate(x1, a7, '1000')
    a11 = circuit.add_gate(x3, a8, '1000')
    a12 = circuit.add_gate(x5, a9, '1101')
    a13 = circuit.add_gate(a8, a10, '0110')
    a14 = circuit.add_gate(x2, a10, '1001')
    a15 = circuit.add_gate(a11, a12, '0110')
    a16 = circuit.add_gate(a11, a13, '0110')
    a17 = circuit.add_gate(a14, a15, '0110')
    a18 = circuit.add_gate(a15, a16, '0111')
    a19 = circuit.add_gate(a17, a18, '0110')

    return a17, a19

def add_sum7ad2(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x0, x1, x2, x3, x4, x5, x6] = input_labels

    a7 = circuit.add_gate(x0, x2, '0110')
    a8 = circuit.add_gate(x2, x4, '0110')
    a9 = circuit.add_gate(x4, x6, '0110')
    a10 = circuit.add_gate(x1, a7, '0111')
    a11 = circuit.add_gate(x3, a8, '0111')
    a12 = circuit.add_gate(x5, a9, '0010')
    a13 = circuit.add_gate(x2, a10, '0110')
    a14 = circuit.add_gate(x4, a11, '0110')
    a15 = circuit.add_gate(a13, a14, '0110')
    a16 = circuit.add_gate(a11, a12, '0110')
    a17 = circuit.add_gate(a15, a16, '0111')
    a18 = circuit.add_gate(a13, a16, '0110')
    a19 = circuit.add_gate(a17, a18, '0110')

    return a18, a19


def add_sum6ad2(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x0, x1, x2, x3, x4, x5] = input_labels

    a6 = circuit.add_gate(x0, x2, '0110')
    a7 = circuit.add_gate(x2, x4, '0110')
    a8 = circuit.add_gate(x1, a6, '0111')
    a9 = circuit.add_gate(x3, a7, '0111')
    a10 = circuit.add_gate(x2, a8, '0110')
    a11 = circuit.add_gate(x4, x5, '0001')
    a12 = circuit.add_gate(a8, a9, '0111')
    a13 = circuit.add_gate(a9, a10, '0110')
    a14 = circuit.add_gate(a11, a13, '0111')
    a15 = circuit.add_gate(a12, a14, '0110')
    a16 = circuit.add_gate(a11, a13, '0110')

    return a15, a16

def add_aox4(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x0, x1, x2, x3, x4] = input_labels

    a0 = circuit.add_gate(x0, x1, '0110')
    a1 = circuit.add_gate(x2, a0, '0110')
    a2 = circuit.add_gate(x3, a1, '0110')
    a3 = circuit.add_gate(x4, a2, '0110')

    b0 = circuit.add_gate(x0, x1, '0001')
    b1 = circuit.add_gate(x2, b0, '0001')
    b2 = circuit.add_gate(x3, b1, '0001')
    b3 = circuit.add_gate(x4, b2, '0001')

    c0 = circuit.add_gate(x0, x1, '0111')
    c1 = circuit.add_gate(x2, c0, '0111')
    c2 = circuit.add_gate(x3, c1, '0111')
    c3 = circuit.add_gate(x4, c2, '0111')

    return a3, b3, c3


def check_sum_circuit(circuit):
    truth_tables = circuit.get_truth_tables()
    n = len(circuit.input_labels)

    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = sum(truth_tables[circuit.outputs[d]][i] * (2 ** d) for d in range(len(circuit.outputs)))
        assert s == sum(x)


def run(fun, size):
    c = Circuit(input_labels=[f'x{i}' for i in range(1, size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    check_sum_circuit(c)
    # c.save_to_file(f'sum/sum{len(c.input_labels)}_size{len(c.gates)}')


def check_various_sum_circuits():
    a=5
    #run(add_sum2, 2)
    #run(add_sum3, 3)
    #run(add_sum4, 4)
    #run(add_sum5, 5)
    #run(add_sum5_suboptimal, 5)
    #run(add_sum6, 6)
    # run(add_sum7, 7)
    #run(add_sum7_suboptimal, 7)
    #run(add_sum8_1, 8)
    #run(add_sum8_2, 8)
    #run(add_sum9, 9)
    #run(add_sum10, 10)
    #run(add_sum10_suboptimal, 10)
    #run(add_sum15, 15)
#    run(add_sum6ad2, 6)
    #run(add_sum15_using_mdfa2, 15)
    #run(add_sum6new, 6)

    # run(add_sum31, 31)


    #c = Circuit(input_labels=[f'x{i}' for i in range(1, 7 + 1)], gates={})
    #c.outputs = add_sum7new(c, c.input_labels)
    #c.draw('newsum7')
    #check_sum_circuit(c)
    #c.save_to_file(f'sum/sum7_sub')

    c = Circuit()
    c.load_from_file('lolkshn')
    check_sum_circuit(c)


check_various_sum_circuits()
