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


def add_mod3_30(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels

    g1 = circuit.add_gate(x2, x3, '1001')
    g2 = circuit.add_gate(x1, x2, '0110')
    g3 = circuit.add_gate(g1, g2, '0010')

    return g3


def add_mod3_32(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels

    g1 = circuit.add_gate(x2, x3, '0110')
    g2 = circuit.add_gate(x3, g1, '0111')
    g3 = circuit.add_gate(x1, g2, '0100')
    g4 = circuit.add_gate(g1, g3, '0110')

    return g4


def add_mod3_42(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4] = input_labels

    g1 = circuit.add_gate(x1, x2, '0110')
    g2 = circuit.add_gate(x3, x4, '0110')
    g3 = circuit.add_gate(x1, x3, '0110')
    g4 = circuit.add_gate(g2, g3, '0111')
    g5 = circuit.add_gate(g1, g4, '0100')
    g6 = circuit.add_gate(g2, g5, '0110')

    return g6


def add_mod3(size, modd):
    circuit = Circuit(input_labels=[f'x{i}' for i in range(1, size + 1)], gates={})

    if size == 3 and modd == 0:
        circuit.outputs = add_mod3_30(circuit, circuit.input_labels[0:3])
        return circuit

    if size == 3 and modd == 2:
        circuit.outputs = add_mod3_32(circuit, circuit.input_labels[0:3])
        return circuit

    if size == 4 and modd == 2:
        circuit.outputs = add_mod3_42(circuit, circuit.input_labels[0:4])
        return circuit

    first = [None] * size
    last = [None] * size
    first_shift = 0
    last_shift = 0

    if modd == 0:
        last_shift = 2
    if modd == 1:
        last_shift = 1
    if modd == 2:
        last_shift = 3

    if (size - last_shift) % 3 == 0:
        first[0], last[0] = add_in3(circuit, circuit.input_labels[0:3])
        first_shift = 3

    if (size - last_shift) % 3 == 1:
        first[0], last[0] = add_in4(circuit, circuit.input_labels[0:4])
        first_shift = 4

    if (size - last_shift) % 3 == 2:
        first[0], last[0] = add_in2(circuit, circuit.input_labels[0:2])
        first_shift = 2

    count = int((size - first_shift - last_shift) / 3)
    for i in range(1, count + 1):
        first[i], last[i] = add_ib_3(circuit, [first[i - 1], last[i - 1]] + circuit.input_labels[first_shift + (i - 1) * 3:first_shift + i * 3])

    result = 0
    if modd == 0:
        result = add_out2_mod0(circuit, [first[count], last[count]] + circuit.input_labels[size - 2: size])
    if modd == 1:
        result = add_out1_mod1(circuit, [first[count], last[count]] + circuit.input_labels[size - 1: size])
    if modd == 2:
        result = add_out3_mod2(circuit, [first[count], last[count]] + circuit.input_labels[size - 3: size])

    circuit.outputs = result
    return circuit


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


def check_mod3_circuit_and_size(size, modd):
    circuit = add_mod3(size, modd)
    tt = circuit.get_truth_tables()
    n = len(circuit.input_labels)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = tt[circuit.outputs[0]][i]
        value = sum(x[j] for j in range(n))
        assert (value % 3 == modd) == s
    assert len(circuit.gates) == 3 * size - 5 - ((size + modd) % 3 == 0)


def run(fun, size, modd):
    c = Circuit(input_labels=[f'x{i}' for i in range(1, size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    check_mod3_circuit(c, modd)
    # c.save_to_file(f'mod3/mod3_{len(c.input_labels)}_{modd}_size{len(c.gates)}')


def check_various_maj_circuits():
    for i in range(3, 9):
        for j in range(0, 3):
            check_mod3_circuit_and_size(i, j)


if __name__ == '__main__':
    check_various_maj_circuits()
