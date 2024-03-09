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

    [x1, x2, x3] = input_labels

    # g1 = circuit.add_gate(x1, x2, '0110')
    # g2 = circuit.add_gate(x2, x3, '0110')
    # g3 = circuit.add_gate(g1, g2, '0111')
    # g4 = circuit.add_gate(g1, x3, '0110')
    # g5 = circuit.add_gate(g3, g4, '0110')
    # return g4, g5

    g1 = circuit.add_gate(x1, x2, '0110')
    g2 = circuit.add_gate(g1, x3, '0110')

    g3 = circuit.add_gate(x1, x2, '0001')
    g4 = circuit.add_gate(g1, x3, '0001')
    g5 = circuit.add_gate(g3, g4, '0110')
    return g2, g5

def add_sum3n(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels

    g1 = circuit.add_gate(x1, x2, '0110')
    g2 = circuit.add_gate(x1, x3, '1001')
    g3 = circuit.add_gate(g1, g2, '0100')
    g4 = circuit.add_gate(x2, g2, '0110')

    return g3, g4


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

def add_sum7_exp(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels


    r1 = circuit.add_gate(x1, x2, '0110')
    r2 = circuit.add_gate(r1, x3, '0110')
    r3 = circuit.add_gate(r2, x4, '0110')
    r4 = circuit.add_gate(r3, x5, '0110')
    r5 = circuit.add_gate(r4, x6, '0110')
    r6 = circuit.add_gate(r5, x7, '0110')
    r7 = circuit.add_gate(x1, r2, '0110')
    r8 = circuit.add_gate(r2, r4, '0110')
    r9 = circuit.add_gate(r4, r6, '0110')

    g1 = circuit.add_gate(r1, r7, '0111')
    g2 = circuit.add_gate(g1, r2, '0110')
    g3 = circuit.add_gate(r3, r8, '0010')
    g4 = circuit.add_gate(g1, g3, '0110')
    g5 = circuit.add_gate(g2, g4, '0010')
    g6 = circuit.add_gate(r5, r9, '0111')

    g7 = circuit.add_gate(g6, r6, '0110')
    g8 = circuit.add_gate(g4, g7, '0110')
    g9 = circuit.add_gate(g4, g7, '0001')
    g10 = circuit.add_gate(g5, g9, '0110')

    return r6, g8, g10

def add_sum7_exp_mix(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels

    ad1 = circuit.add_gate(x2, x3, '0110')
    ad2 = circuit.add_gate(x4, x5, '0110')
    ad3 = circuit.add_gate(x6, x7, '0110')

    r1 = circuit.add_gate(x1, x2, '0110')
    r2 = circuit.add_gate(r1, ad1, '0110')
    r3 = circuit.add_gate(r2, x4, '0110')
    r4 = circuit.add_gate(r3, ad2, '0110')
    r5 = circuit.add_gate(r4, x6, '0110')
    r6 = circuit.add_gate(r5, ad3, '0110')
    r7 = circuit.add_gate(x1, r2, '0110')
    r8 = circuit.add_gate(r2, r4, '0110')
    r9 = circuit.add_gate(r4, r6, '0110')

    g1 = circuit.add_gate(r1, r7, '0111')
    g2 = circuit.add_gate(g1, r2, '0110')
    g3 = circuit.add_gate(r3, r8, '0010')
    g4 = circuit.add_gate(g1, g3, '0110')
    g5 = circuit.add_gate(g2, g4, '0010')
    g6 = circuit.add_gate(r5, r9, '0111')

    g7 = circuit.add_gate(g6, r6, '0110')
    g8 = circuit.add_gate(g4, g7, '0110')
    g9 = circuit.add_gate(g4, g7, '0001')
    g10 = circuit.add_gate(g5, g9, '0110')

    return r6, g8, g10


def add_new_mdfa(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    z5 = circuit.add_gate(x1, x3, '0110')
    z6 = circuit.add_gate(x2, x4, '0010')
    z8 = circuit.add_gate(x2, x4, '1110')
    z9 = circuit.add_gate(x3, z5, '0111')
    z10 = circuit.add_gate(x4, z6, '1001')
    z11 = circuit.add_gate(x5, z5, '1011')
    z12 = circuit.add_gate(z9, z11, '1001')
    z13 = circuit.add_gate(z8, z12, '1001')
    z14 = circuit.add_gate(z10, z13, '0100')
    z15 = circuit.add_gate(z8, z14, '1101')
    z16 = circuit.add_gate(z10, z12, '1101')
    z17 = circuit.add_gate(x3, x5, '1001')
    z18 = circuit.add_gate(x1, z17, '1001')



    return z15, z14, z16, z18


def add_sum7_exp2(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels


    r1 = circuit.add_gate(x1, x2, '0110')
    r2 = circuit.add_gate(r1, x3, '0110')
    r3 = circuit.add_gate(x4, r2, '0110')
    r4 = circuit.add_gate(r3, x5, '0110')
    r5 = circuit.add_gate(r4, x6, '0110')
    r6 = circuit.add_gate(r5, x7, '0110')
    r7 = circuit.add_gate(x1, r2, '0110')
    r8 = circuit.add_gate(r2, r4, '0110')
    r9 = circuit.add_gate(r4, r6, '0110')

    g1 = circuit.add_gate(r1, r7, '0111')
    g2 = circuit.add_gate(g1, r2, '0110')
    g3 = circuit.add_gate(r3, r8, '0010')
    g4 = circuit.add_gate(g1, g3, '0110') # 2,3 from [x1..x5]
    g5 = circuit.add_gate(g2, g4, '0010')
    g6 = circuit.add_gate(r5, r9, '0111')
    g7 = circuit.add_gate(g6, r6, '0110')
    g8 = circuit.add_gate(g4, g7, '0110')
    g9 = circuit.add_gate(g4, g7, '0001')
    g10 = circuit.add_gate(g5, g9, '0110')

    return r6, g8, g10



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

def add_sum7_suboptimal_n(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels

    a0, a1 = add_sum3n(circuit, [x1, x2, x3])
    b0, b1 = add_sum3n(circuit, [a0, x4, x5])
    c0, c1 = add_sum3n(circuit, [b0, x6, x7])
    d1, d2 = add_sum3n(circuit, [a1, b1, c1])

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


def add_sum11_size36(circuit, input_labels):
    assert len(input_labels) == 11
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11] = input_labels

    a0, a1, a2 = add_sum7(circuit, [x1, x2, x3, x4, x5, x6, x7])
    b0, b1 = add_sum3(circuit, [a0, x8, x9])
    w0, c1 = add_sum3(circuit, [b0, x10, x11])
    w1, d2 = add_sum3(circuit, [a1, b1, c1])
    w2, w3 = add_sum2(circuit, [a2, d2])

    return w0, w1, w2, w3


def add_sum15_size53(circuit, input_labels):
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


def add_mdfa(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x2, x1_xor_x2, x3, x4, x4_xor_x5] = input_labels

    g2 = circuit.add_gate(x2, x3, '0110')
    g3 = circuit.add_gate(x1_xor_x2, g2, '0111')
    g4 = circuit.add_gate(x1_xor_x2, x3, '0110')
    g5 = circuit.add_gate(g3, g4, '0110')
    g6 = circuit.add_gate(x4, g4, '0110')
    g8 = circuit.add_gate(g6, x4_xor_x5, '0010')
    g9 = circuit.add_gate(g4, x4_xor_x5, '0110')
    g10 = circuit.add_gate(g3, g8, '0110')

    return g9, g5, g10


def add_mdfa_change(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x3, x2, x1_xor_x2, x4, x4_xor_x5] = input_labels

    g2 = circuit.add_gate(x2, x3, '0110')
    g3 = circuit.add_gate(x1_xor_x2, g2, '0111')
    g4 = circuit.add_gate(x1_xor_x2, x3, '0110')
    g5 = circuit.add_gate(g3, g4, '0110')
    g6 = circuit.add_gate(x4, g4, '0110')
    g8 = circuit.add_gate(g6, x4_xor_x5, '0010')
    g9 = circuit.add_gate(g4, x4_xor_x5, '0110')
    g10 = circuit.add_gate(g3, g8, '0110')

    return g9, g5, g10

def add_mdfa_with_xors(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x2, x1, x3, x4, x5] = input_labels

    x4_xor_x5 = circuit.add_gate(x4, x5, '0110')
    x1_xor_x2 = circuit.add_gate(x1, x2, '0110')
    g2 = circuit.add_gate(x2, x3, '0110')
    g3 = circuit.add_gate(x1_xor_x2, g2, '0111')
    g4 = circuit.add_gate(x1_xor_x2, x3, '0110')
    g5 = circuit.add_gate(g3, g4, '0110')
    g6 = circuit.add_gate(x4, g4, '0110')
    g8 = circuit.add_gate(g6, x4_xor_x5, '0010')
    g9 = circuit.add_gate(g4, x4_xor_x5, '0110')
    g10 = circuit.add_gate(g3, g8, '0110')

    return g9, g5, g10


def add_mdfa_cut(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x2, x1_xor_x2, x4, x4_xor_x5] = input_labels

    g3 = circuit.add_gate(x1_xor_x2, x2, '0111')
    g5 = circuit.add_gate(g3, x1_xor_x2, '0110')
    g6 = circuit.add_gate(x4, x1_xor_x2, '0110')
    g8 = circuit.add_gate(g6, x4_xor_x5, '0010')
    g9 = circuit.add_gate(x1_xor_x2, x4_xor_x5, '0110')
    g10 = circuit.add_gate(g3, g8, '0110')

    return g9, g5, g10


def add_sum8_mdfa(circuit, input_labels):
    assert len(input_labels) == 8
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8] = input_labels

    zero = circuit.add_gate(x1, x1, '0110')

    x1_xor_x2 = circuit.add_gate(x1, x2, '0110')
    x3_xor_x4 = circuit.add_gate(x3, x4, '0110')
    x5_xor_x6 = circuit.add_gate(x5, x6, '0110')
    x7_xor_x8 = circuit.add_gate(x7, x8, '0110')
    b0, e1, e1_xor_f1 = add_mdfa(circuit, [x1, x1_xor_x2, zero, x3, x3_xor_x4])
    w0, g1, g1_xor_h1 = add_mdfa(circuit, [x5, x5_xor_x6, b0, x7, x7_xor_x8])

    w1, i1, i1_xor_j1 = add_mdfa(circuit, [e1, e1_xor_f1, zero, g1, g1_xor_h1])

    w2, w3 = add_stockmeyers_block(circuit, [i1, i1_xor_j1, zero])

    return w0, w1, w2, w3


def add_sum15(circuit, input_labels):
    assert len(input_labels) == 15
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15] = input_labels

    a0, a1 = add_sum3(circuit, [x1, x2, x3])
    x4_xor_x5 = circuit.add_gate(x4, x5, '0110')
    x6_xor_x7 = circuit.add_gate(x6, x7, '0110')
    b0, e1, e1_xor_f1 = add_mdfa(circuit, [x4, x4_xor_x5, a0, x6, x6_xor_x7])
    x8_xor_x9 = circuit.add_gate(x8, x9, '0110')
    x10_xor_x11 = circuit.add_gate(x10, x11, '0110')
    c0, g1, g1_xor_h1 = add_mdfa(circuit, [x8, x8_xor_x9, b0, x10, x10_xor_x11])
    x12_xor_x13 = circuit.add_gate(x12, x13, '0110')
    x14_xor_x15 = circuit.add_gate(x14, x15, '0110')
    w0, i1, i1_xor_j1 = add_mdfa(circuit, [x12, x12_xor_x13, c0, x14, x14_xor_x15])
    n1, k2, k2_xor_l2 = add_mdfa(circuit, [e1, e1_xor_f1, a1, g1, g1_xor_h1])
    w1, m2 = add_stockmeyers_block(circuit, [i1_xor_j1, i1, n1])
    w2, w3 = add_stockmeyers_block(circuit, [k2_xor_l2, k2, m2])

    return w0, w1, w2, w3

def add_sum3sb(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels


    xor = circuit.add_gate(x2, x3, '0110')
    w2, w3 = add_stockmeyers_block(circuit, [xor, x2, x1])

    return w2, w3


# def add_stockmeyers_block(circuit, input_labels):
#     assert len(input_labels) == 3
#     for input_label in input_labels:
#         assert input_label in circuit.input_labels or input_label in circuit.gates
#
#     [x2, x1_xor_x2, x3] = input_labels
#     g2 = circuit.add_gate(x2, x1_xor_x2, '0110')
#     g3 = circuit.add_gate(x2, x3, '0110')
#     sum = circuit.add_gate(g2, x3, '0110')
#     sum_xor_carry = circuit.add_gate(g2, g3, '0111')
#     # g2 = circuit.add_gate(x2, x3, '0110')
#     # g3 = circuit.add_gate(x1_xor_x2, g2, '0111')
#     # g4 = circuit.add_gate(x1_xor_x2, x3, '0110')
#     # g5 = circuit.add_gate(g3, g4, '0110')
#
#     return sum, sum_xor_carry
#     # return g3, g5

def add_stockmeyers_block(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x2, x1_xor_x2, x3] = input_labels
    g2 = circuit.add_gate(x2, x3, '0110')
    g3 = circuit.add_gate(x1_xor_x2, g2, '0111')
    g4 = circuit.add_gate(x1_xor_x2, x3, '0110')
    g5 = circuit.add_gate(g3, g4, '0110')

    return g4, g5


def add_stockmeyers_block_cut(circuit, input_labels):
    assert len(input_labels) == 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x2, x1_xor_x2] = input_labels
    g5 = circuit.add_gate(x1_xor_x2, x2, '0100')

    return x1_xor_x2, g5


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


def add_sumn(circuit, input_labels):
    n = len(input_labels)
    output = []
    if n == 1:
        return [input_labels[0]]
    assert len(input_labels) == n
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x = input_labels
    a = [''] * (n // 2)
    b = [''] * (n // 2)
    if n % 2 == 0:
        a[0], b[0] = add_sum2(circuit, [x[0], x[1]])
    else:
        a[0], b[0] = add_sum3(circuit, [x[0], x[1], x[2]])
    for i in range(2 + n % 2, len(input_labels), 2):
        a[i // 2], b[i // 2] = add_sum3(circuit, [a[(i - 2) // 2], x[i], x[i + 1]])

    output.append(a[len(a) - 1])
    output.append(add_sumn(circuit, b))

    output = str(output).replace("[", "").replace("]", "").replace("'", "").replace(" ", "").split(',')
    return output


def add_sumn_mdfa(circuit, input_labels, is_first=True):
    n = len(input_labels)
    output = []
    if n == 1:
        return [input_labels[0]]
    assert len(input_labels) == n
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    x = input_labels
    a = [''] * (((n - 2) // 4) + 1)
    b = [''] * (((n - 2) // 2) + 1)

    if n % 4 == 2:
        xor = circuit.add_gate(x[0], x[1], '0110') if is_first else x[1]
        a[0], b[0] = add_stockmeyers_block_cut(circuit, [x[0], xor])
    if n % 4 == 3:
        xor = circuit.add_gate(x[1], x[2], '0110') if is_first else x[2]
        a[0], b[0] = add_stockmeyers_block(circuit, [x[1], xor, x[0]])
    if n % 4 == 0:
        xor1 = circuit.add_gate(x[0], x[1], '0110') if is_first else x[1]
        xor2 = circuit.add_gate(x[2], x[3], '0110') if is_first else x[3]
        a[0], b[0], b[1] = add_mdfa_cut(circuit, [x[0], xor1, x[2], xor2])
    if n % 4 == 1:
        xor1 = circuit.add_gate(x[1], x[2], '0110') if is_first else x[2]
        xor2 = circuit.add_gate(x[3], x[4], '0110') if is_first else x[4]
        a[0], b[0], b[1] = add_mdfa(circuit, [x[1], xor1, x[0], x[3], xor2])

    start = n % 4
    if start <= 1:
        start = start + 4

    for i in range(start, len(input_labels), 4):
        forb = 2 * ((i - 2) // 4)
        if start <= 3:
            forb = forb + 1
        else:
            forb = forb + 2

        xor1 = circuit.add_gate(x[i], x[i + 1], '0110') if is_first else x[i + 1]
        xor2 = circuit.add_gate(x[i + 2], x[i + 3], '0110') if is_first else x[i + 3]
        a[((i - 2) // 4) + 1], b[forb], b[forb + 1] = add_mdfa(circuit, [x[i], xor1, a[(i - 2) // 4], x[i + 2], xor2])

    output.append(a[len(a) - 1])
    output.append(add_sumn_mdfa(circuit, b, False))

    output = str(output).replace("[", "").replace("]", "").replace("'", "").replace(" ", "").split(',')
    return output


def add_xor_girl(circuit, input_labels):
    assert len(input_labels) == 9
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9] = input_labels

    z1 = circuit.add_gate(x1, x2, '0010')
    z2 = circuit.add_gate(x2, x3, '1101')
    z3 = circuit.add_gate(z1, z2, '1011')

    z4 = circuit.add_gate(x4, x5, '0010')
    z5 = circuit.add_gate(x5, x6, '1101')
    z6 = circuit.add_gate(z4, z5, '1011')

    z7 = circuit.add_gate(x7, x8, '0010')
    z8 = circuit.add_gate(x8, x9, '1101')
    z9 = circuit.add_gate(z7, z8, '1011')

    # z10 = circuit.add_gate(x7, x8, '0010')
    # z11 = circuit.add_gate(x8, x8, '1101')
    # z12 = circuit.add_gate(z7, z8, '1011')
    #
    # z13 = circuit.add_gate(x7, x8, '0010')
    # z14 = circuit.add_gate(x8, x8, '1101')
    # z15 = circuit.add_gate(z7, z8, '1011')

    z10 = circuit.add_gate(z3, z6, '0110')
    z11 = circuit.add_gate(z10, z9, '0110')

    return z3, z10, z11


def add_p(circuit, input_labels):
    assert len(input_labels) == 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2] = input_labels

    z1 = circuit.add_gate(x1, x2, '0110')

    return x1, z1


def add_pd(circuit, input_labels):
    assert len(input_labels) == 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2] = input_labels

    z1 = circuit.add_gate(x1, x2, '0110')

    return x1, z1


def add_cs(circuit, input_labels):
    assert len(input_labels) == 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2] = input_labels

    z1 = circuit.add_gate(x1, x2, '0001')
    z2 = circuit.add_gate(x1, x2, '0110')

    return z1, z2


def add_p1(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x5, x1, x2] = input_labels

    z1 = circuit.add_gate(x1, x5, '0110')
    mid1 = circuit.add_gate(x2, z1, '0111')
    mid2 = circuit.add_gate(x2, x5, '0110')
    c1 = circuit.add_gate(mid1, mid2, '0110')

    return mid1, mid2, c1


def add_p2(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [mid1, mid2, x3, x4] = input_labels

    z1 = circuit.add_gate(x3, mid2, '0110')
    s2 = circuit.add_gate(x4, mid2, '0110')
    z3 = circuit.add_gate(z1, x4, '0010')
    c2 = circuit.add_gate(mid1, z3, '0110')

    return s2, c2


def add_mdfa_sep(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    # s2, c1, c2 = add_mdfa(circuit, [x1, x2, x5, x3, x4])

    mid1, mid2, c1 = add_p1(circuit, [x5, x1, x2])
    s2, c2 = add_p2(circuit, [mid1, mid2, x3, x4])

    return s2, c1, c2


def add_mdfa_by_blocks(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    px1, px2 = add_p(circuit, [x1, x2])
    px3, px4 = add_p(circuit, [x3, x4])
    s3, c1, c2 = add_mdfa_sep(circuit, [px1, px2, px3, px4, x5])
    rc1, rc2 = add_pd(circuit, [c1, c2])
    s1, s2 = add_cs(circuit, [rc1, rc2])

    return s3, s2, s1


def add_upper_blocks(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x5, x1, x2, x3, x4] = input_labels

    z1 = circuit.add_gate(x5, x1, '0110')
    z2 = circuit.add_gate(x1, x2, '0110')
    z3 = circuit.add_gate(x5, z2, '0110')
    z4 = circuit.add_gate(z3, x3, '0110')
    z5 = circuit.add_gate(x3, x4, '0110')
    z6 = circuit.add_gate(z3, z5, '0110')

    return z1, z2, z3, z4, z5, z6


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
    tt = c.get_truth_tables()
    check_sum_circuit(c)
    # c.save_to_file(f'sum/sum{len(c.input_labels)}_size{len(c.gates)}')

def add_sum3_tt(tt, input_labels):

    [x1, x2, x3] = input_labels
    [ta, tb] = tt
    n = x1*4+x2*2+x3
    return ta[n], tb[n]


def add_mdfa_tt(tt, input_labels):

    [x1, x2, x3, x4, x5] = input_labels
    [ta, tb, tc] = tt
    n = x1*16+x2*8+x3*4+x4*2+x5
    return ta[n], tb[n], tc[n]


def add_stockmeyers_block_tt(tt, input_labels):

    [x1, x2, x3] = input_labels
    tt = [[0, 1, 1, 0, 0, 1, 1, 0], [0, 0, 0, 1, 1, 1, 0, 1]]
    n = x1*4+x2*2+x3
    return tt[0][n], tt[0][n]


def add_sum8_blocks(tt, input_labels):

    [x1, x2, x3, x4, x5, x6, x7, x8] = input_labels

    zero = 0

    a0, b0 = add_sum3_tt(tt,[zero, x1, x2])
    a1, b1 = add_sum3_tt(tt,[a0, x3, x4])
    a2, b2 = add_sum3_tt(tt,[a1, x5, x6])
    a3, b3 = add_sum3_tt(tt,[a2, x7, x8])

    c0, d0 = add_sum3_tt(tt,[zero, b0, b1])
    c1, d1 = add_sum3_tt(tt,[c0, b2, b3])

    e0, f0 = add_sum3_tt(tt,[zero, d0, d1])

    return [a3, c1, e0, f0]


def add_sum8_blocks_xors(tt, input_labels):

    [x1, x2, x3, x4, x5, x6, x7, x8] = input_labels

    zero = 0

    x1_xor_x2 = (x1 + x2) % 2
    x3_xor_x4 = (x3 + x4) % 2
    x5_xor_x6 = (x5 + x6) % 2
    x7_xor_x8 = (x7 + x8) % 2

    a0, b0 = add_sum3_tt(tt,[zero, x1, x1_xor_x2])
    a1, b1 = add_sum3_tt(tt,[a0, x3, x3_xor_x4])
    a2, b2 = add_sum3_tt(tt,[a1, x5, x5_xor_x6])
    a3, b3 = add_sum3_tt(tt,[a2, x7, x7_xor_x8])

    c0, d0 = add_sum3_tt(tt,[zero, b0, b1])
    c1, d1 = add_sum3_tt(tt,[c0, b2, b3])

    e0, f0 = add_sum3_tt(tt,[zero, d0, d1])

    return [a3, c1, e0, f0]


def add_sum8_mdfa(tt, input_labels):

    [x1, x2, x3, x4, x5, x6, x7, x8] = input_labels

    zero = 0

    x1_xor_x2 = (x1 + x2) % 2
    x3_xor_x4 = (x3 + x4) % 2
    x5_xor_x6 = (x5 + x6) % 2
    x7_xor_x8 = (x7 + x8) % 2
    b0, e1, e1_xor_f1 = add_mdfa_tt(tt, [x1, x1_xor_x2, zero, x3, x3_xor_x4])
    w0, g1, g1_xor_h1 = add_mdfa_tt(tt, [x5, x5_xor_x6, b0, x7, x7_xor_x8])

    w1, i1, i1_xor_j1 = add_mdfa_tt(tt, [e1, e1_xor_f1, zero, g1, g1_xor_h1])

    w2, w3 = add_stockmeyers_block_tt(tt, [i1, i1_xor_j1, zero])

    return [w0, w1, w2, w3]


def find():
    n = 8
    for arr1 in product(range(2), repeat=n):
        for arr2 in product(range(2), repeat=n):

            f = True
            tt = [list(arr1), list(arr2)]
            aaaa=0
            # tt = [[0, 1, 1, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1, 1, 1]]
            for x in product(range(2), repeat=n):
                # [a1, a2, a3, a4] = add_sum8_blocks(tt, x)
                arr = add_sum8_blocks(tt, x)
                # i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
                s = sum(arr[d] * (2 ** d) for d in range(len(arr)))
                if s != sum(x):
                    f = False
                    break
            if f:
                print(tt)
                break

def find_sum3_xors():
    n = 8
    for arr1 in product(range(2), repeat=n):
        for arr2 in product(range(2), repeat=n):

            f = True
            tt = [list(arr1), list(arr2)]
            aaaa=0
            # tt = [[0, 1, 1, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1, 1, 1]]
            for x in product(range(2), repeat=n):
                # [a1, a2, a3, a4] = add_sum8_blocks(tt, x)
                arr = add_sum8_blocks_xors(tt, x)
                arr[2] = 0
                arr[3] = 0
                # i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
                s = sum(arr[d] * (2 ** d) for d in range(len(arr)))
                if s != (sum(x) & 3):
                    f = False
                    break
            if f:
                print(tt)
                break

def find_mdfa():
    nn = 32
    n = 8
    for arr1 in product(range(2), repeat=nn):
        print(1)
        for arr2 in product(range(2), repeat=nn):
            print(2)
            for arr3 in product(range(2), repeat=nn):

                f = True
                tt = [list(arr1), list(arr2), list(arr3)]
                aaaa=0
                # tt = [[0, 1, 1, 0, 1, 0, 0, 1], [0, 0, 0, 1, 0, 1, 1, 1]]
                for x in product(range(2), repeat=n):
                    # [a1, a2, a3, a4] = add_sum8_blocks(tt, x)
                    arr = add_sum8_mdfa(tt, x)
                    # i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
                    s = sum(arr[d] * (2 ** d) for d in range(len(arr)))
                    if s != sum(x):
                        f = False
                        break
                if f:
                    print(tt)
                    break

def add_A(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1,x2,x3] = input_labels

    g3 = circuit.add_gate(x1, x2, '1001')
    g4 = circuit.add_gate(x2, x3, '1001')
    g5 = circuit.add_gate(g3, g4, '1011')
    g6 = circuit.add_gate(x1, g5, '1001')
    g7 = circuit.add_gate(x1, g4, '1001')

    return g7, g6

def add_B(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1,x2,x3] = input_labels

    g3 = circuit.add_gate(x1, x2, '0110')
    g4 = circuit.add_gate(x1, x3, '1001')
    g5 = circuit.add_gate(g3, g4, '0100')
    g6 = circuit.add_gate(x2, g4, '0110')

    return g6, g5

def add_mdfa222(circuit, input_labels):
    assert len(input_labels) == 15
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14] = input_labels

    zero = circuit.add_gate(x1, x1, '0110')
    b0, b1 = add_A(circuit, [zero, zero, x0])
    b2, b3 = add_A(circuit, [b0, x1, x2])
    b4, b5 = add_A(circuit, [b2, x3, x4])
    b6, b7 = add_A(circuit, [b4, x5, x6])

    bb0, bb1 = add_A(circuit, [b6, x14, x7])
    bb2, bb3 = add_A(circuit, [bb0, x8, x9])
    bb4, bb5 = add_A(circuit, [bb2, x10, x11])
    bb6, bb7 = add_A(circuit, [bb4, x12, x13])

    b10, b11, = add_B(circuit, [zero, b1, b3])
    b8, b9, = add_B(circuit, [b10, b5, b7])
    b12, b13, = add_B(circuit, [zero, b11, b9]) #22

    bb10, bb11 = add_B(circuit, [b8, bb1, bb3])
    bb8, bb9 = add_B(circuit, [bb10, bb5, bb7])
    bb12, bb13 = add_B(circuit, [b12, bb11, bb9]) #28

    # bb14, b14 = add_B(circuit, [zero, b13, bb13])

    b15 = circuit.add_gate(b13, bb13, '1110')

    return bb6, bb8, bb12, b15


def check_various_sum_circuits():
    for n in range(2, 16):
        run(add_sumn_mdfa, n)

    run(add_sum2, 2)
    run(add_sum3, 3)
    run(add_sum4, 4)
    run(add_sum5, 5)
    run(add_sum5_suboptimal, 5)
    run(add_sum7, 7)
    run(add_sum9, 9)
    run(add_sum10, 10)
    run(add_sum10_suboptimal, 10)

if __name__ == '__main__':
    check_various_sum_circuits()
