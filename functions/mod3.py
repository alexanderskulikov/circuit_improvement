from functions.ib import *


def add_in2(circuit, input_labels):
    assert len(input_labels) == 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2] = input_labels

    z0 = circuit.add_gate(x1, x2, '0110')
    z1 = circuit.add_gate(x1, x2, '0001')

    return z1, z0


def add_in3(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels

    z0 = circuit.add_gate(x1, x2, '1001')
    z1 = circuit.add_gate(x1, x2, '1000')
    z2 = circuit.add_gate(z1, x3, '1001')
    z3 = circuit.add_gate(z0, z2, '1001')
    z4 = circuit.add_gate(z1, z3, '0100')

    return z4, z2


def add_in4(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [u1, x, y, z] = input_labels

    g1 = circuit.add_gate(x, u1, '1001')
    g3 = circuit.add_gate(g1, y, '0110')
    g5 = circuit.add_gate(x, g3, '0110')
    g6 = circuit.add_gate(g5, g1, '0001')
    g7 = circuit.add_gate(g6, z, '1001')
    g8 = circuit.add_gate(g3, g7, '1001')
    g9 = circuit.add_gate(g6, g8, '0100')

    return g9, g7


def add_mid3(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [u0, u1, x, y, z] = input_labels

    g1 = circuit.add_gate(x, u1, '1001')
    g2 = circuit.add_gate(g1, u0, '0111')
    g3 = circuit.add_gate(g2, y, '0110')
    g4 = circuit.add_gate(g3, u0, '0110')
    g5 = circuit.add_gate(g4, x, '0110')
    g6 = circuit.add_gate(g5, g2, '0001')
    g7 = circuit.add_gate(g6, z, '1001')
    g8 = circuit.add_gate(g3, g7, '1001')
    g9 = circuit.add_gate(g6, g8, '0100')

    return g9, g7


def add_out1_mod1(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels

    a3 = circuit.add_gate(x3, x2, '0110')
    a4 = circuit.add_gate(x1, a3, '0100')

    return a4


def add_out2_mod0(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [z0, z1, x1, x2] = input_labels

    g1 = circuit.add_gate(z0, x2, '1001')
    g2 = circuit.add_gate(x1, z1, '0110')
    g3 = circuit.add_gate(g1, x1, '1001')
    g4 = circuit.add_gate(z0, g2, '0100')
    g5 = circuit.add_gate(g3, g4, '1000')

    return g5


def add_out3_mod2(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [z0, z1, x1, x2, x3] = input_labels

    g1 = circuit.add_gate(x1, z1, '1001')
    g2 = circuit.add_gate(g1, z0, '0111')
    g3 = circuit.add_gate(x2, g2, '0110')
    g4 = circuit.add_gate(g3, z0, '0110')
    g5 = circuit.add_gate(g4, x1, '0110')
    g6 = circuit.add_gate(g5, g2, '0001')
    g7 = circuit.add_gate(x3, g3, '1001')
    g8 = circuit.add_gate(g6, g7, '1000')

    return g8


def add_out1_mod0(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels

    a3 = circuit.add_gate(x2, x1, '1101')
    a4 = circuit.add_gate(x3, a3, '0100')
    a5 = circuit.add_gate(x1, a4, '0110')

    return a5


def add_out3_mod0(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels
    z0 = circuit.add_gate(x3, x2, '1001')
    a5 = circuit.add_gate(z0, x1, '0111')
    a6 = circuit.add_gate(x4, a5, '0110')
    z3 = circuit.add_gate(a6, x1, '0110')
    z4 = circuit.add_gate(z3, x3, '0110')
    z5 = circuit.add_gate(z4, a5, '0001')
    z6 = circuit.add_gate(z5, x5, '1001')
    a7 = circuit.add_gate(z5, a6, '0111')
    a8 = circuit.add_gate(z6, a7, '0100')

    return a8


def add_out4_mod0(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels
    z0 = circuit.add_gate(x3, x2, '1001')
    z1 = circuit.add_gate(z0, x1, '0111')
    z2 = circuit.add_gate(z1, x4, '0110')
    z3 = circuit.add_gate(z2, x1, '0110')
    z4 = circuit.add_gate(z3, x3, '0110')
    a6 = circuit.add_gate(z4, z1, '0001')
    b4 = circuit.add_gate(a6, x5, '1001')
    z7 = circuit.add_gate(z2, b4, '1001')
    a7 = circuit.add_gate(z7, a6, '0010')
    b5 = circuit.add_gate(x6, b4, '1011')
    b6 = circuit.add_gate(a7, x6, '1001')
    b7 = circuit.add_gate(b5, b6, '0001')

    return b7


def add_out2_mod1(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4] = input_labels
    a7 = circuit.add_gate(x2, x1, '0010')
    b4 = circuit.add_gate(x4, x3, '0001')
    b5 = circuit.add_gate(a7, b4, '0111')
    b6 = circuit.add_gate(x4, x3, '0111')
    b7 = circuit.add_gate(x1, b6, '0100')
    b8 = circuit.add_gate(b5, b7, '0110')

    return b8


def add_out3_mod1(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    z0 = circuit.add_gate(x3, x2, '1001')
    a5 = circuit.add_gate(x1, z0, '0111')
    a6 = circuit.add_gate(x4, a5, '0110')
    z3 = circuit.add_gate(a6, x1, '0110')
    z4 = circuit.add_gate(z3, x3, '0110')
    z5 = circuit.add_gate(z4, a5, '0001')
    z6 = circuit.add_gate(z5, x5, '1001')
    a7 = circuit.add_gate(z5, a6, '1011')
    a8 = circuit.add_gate(z6, a7, '0001')

    return a8


def add_out4_mod1(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels

    z0 = circuit.add_gate(x3, x2, '1001')
    a6 = circuit.add_gate(z0, x1, '0111')
    b7 = circuit.add_gate(a6, x4, '0110')
    z3 = circuit.add_gate(b7, x1, '0110')
    z4 = circuit.add_gate(z3, x3, '0110')
    c5 = circuit.add_gate(z4, a6, '0001')
    b6 = circuit.add_gate(c5, x5, '1001')
    b8 = circuit.add_gate(b6, b7, '1001')
    c6 = circuit.add_gate(b8, c5, '0010')
    c7 = circuit.add_gate(b6, x6, '0110')
    c8 = circuit.add_gate(c6, c7, '0100')

    return c8


def add_out1_mod2(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels

    a3 = circuit.add_gate(x3, x1, '1001')
    a4 = circuit.add_gate(x2, x1, '0111')
    a5 = circuit.add_gate(a3, a4, '0100')

    return a5


def add_out2_mod2(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4] = input_labels

    a4 = circuit.add_gate(x1, x2, '1011')
    a5 = circuit.add_gate(x3, a4, '1011')
    a6 = circuit.add_gate(x1, a5, '1001')
    a7 = circuit.add_gate(x4, a4, '0110')
    z2 = circuit.add_gate(x3, a7, '0110')
    z6 = circuit.add_gate(z2, a6, '0010')

    return z6


def add_out4_mod2(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels
    z0 = circuit.add_gate(x3, x2, '1001')
    a6 = circuit.add_gate(z0, x1, '0111')
    z2 = circuit.add_gate(a6, x4, '0110')
    z3 = circuit.add_gate(z2, x1, '0110')
    z4 = circuit.add_gate(z3, x3, '0110')
    a7 = circuit.add_gate(z4, a6, '0001')
    a8 = circuit.add_gate(x5, a7, '1001')
    z7 = circuit.add_gate(z2, a8, '1001')
    z8 = circuit.add_gate(a7, z7, '0100')
    a9 = circuit.add_gate(z8, a8, '1000')
    z10 = circuit.add_gate(x6, a9, '0010')
    z12 = circuit.add_gate(z8, z10, '0110')

    return z12


def add_mod3_9_0(circuit, input_labels):
    assert len(input_labels) == 9
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates
    # 3k
    [x1, x2, x3, x4, x5, x6, x7, x8, x9] = input_labels

    a1, a2 = add_in4(circuit, [x1, x2, x3, x4])
    b1, b2 = add_ib_3(circuit, [a1, a2, x5, x6, x7])
    c1 = add_out2_mod0(circuit, [b1, b2, x8, x9])
    return c1


def add_mod3_6_0(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates
    # 3k
    [x1, x2, x3, x4, x5, x6] = input_labels

    a1, a2 = add_in4(circuit, [x1, x2, x3, x4])
    c1 = add_out2_mod0(circuit, [a1, a2, x5, x6])
    return c1


def add_mod3_9_1(circuit, input_labels):
    assert len(input_labels) == 9
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates
    # 3k + 1
    [x1, x2, x3, x4, x5, x6, x7, x8, x9] = input_labels

    a1, a2 = add_in2(circuit, [x1, x2])
    b1, b2 = add_ib_3(circuit, [a1, a2, x3, x4, x5])
    c1, c2 = add_ib_3(circuit, [b1, b2, x6, x7, x8])
    d1 = add_out1_mod1(circuit, [c1, c2, x9])
    return d1


def check_mod3_circuit(circuit, modd):
    tt = circuit.get_truth_tables()
    n = len(circuit.input_labels)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = tt[circuit.outputs[0]][i]
        value = sum(x[j] for j in range(n))
        assert (value % 3 == modd) == s


def check_out_circuit(circuit, modd):
    tt = circuit.get_truth_tables()
    n = len(circuit.input_labels)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = tt[circuit.outputs[0]][i]
        value = sum(x[j] for j in range(2, n))
        if x[0] == 1:
            value += 2
        else:
            if x[1] == 1:
                value += 1
        assert (value % 3 == modd) == s


def run(fun, size, modd):
    c = Circuit(input_labels=[f'x{i}' for i in range(1, size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    check_mod3_circuit(c, modd)
    # c.save_to_file(f'mod3/mod3_{len(c.input_labels)}_{modd}_size{len(c.gates)}')


def run_out(fun, size, modd):
    c = Circuit(input_labels=[f'x{i}' for i in range(1, size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    check_out_circuit(c, modd)
    # c.save_to_file(f'mod3/out/out_{len(c.input_labels)-2}_{modd}_size{len(c.gates)}')


def check_various_maj_circuits():

    run_out(add_out1_mod0, 3, 0)
    run_out(add_out2_mod0, 4, 0)
    run_out(add_out3_mod0, 5, 0)
    run_out(add_out4_mod0, 6, 0)

    run_out(add_out1_mod1, 3, 1)
    run_out(add_out2_mod1, 4, 1)
    run_out(add_out3_mod1, 5, 1)
    run_out(add_out4_mod1, 6, 1)

    run_out(add_out1_mod2, 3, 2)
    run_out(add_out2_mod2, 4, 2)
    run_out(add_out3_mod2, 5, 2)
    run_out(add_out4_mod2, 6, 2)

    run(add_mod3_9_1, 9, 1)
    run(add_mod3_9_0, 9, 0)
    run(add_mod3_6_0, 6, 0)


if __name__ == '__main__':
    check_various_maj_circuits()
