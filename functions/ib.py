from circuit import Circuit
from itertools import product


def add_ib_1(circuit, input_labels):
    assert len(input_labels) == 1 + 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [u0, u1, z] = input_labels

    a3 = circuit.add_gate(u1, u0, '1000')
    a5 = circuit.add_gate(z, a3, '0010')
    a6 = circuit.add_gate(z, a3, '1001')
    a7 = circuit.add_gate(u0, a5, '0110')

    return a7, a6


def add_ib_2(circuit, input_labels):
    assert len(input_labels) == 2 + 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [u0, u1, x1, x2] = input_labels

    a4 = circuit.add_gate(u1, u0, '0010')
    a5 = circuit.add_gate(x2, a4, '1001')
    a6 = circuit.add_gate(x1, a5, '0110')
    a7 = circuit.add_gate(x1, a4, '1000')
    a8 = circuit.add_gate(u0, a7, '0110')
    z6 = circuit.add_gate(x2, a8, '1001')
    a9 = circuit.add_gate(a6, a8, '0010')

    return a9, z6


def add_ib_3(circuit, input_labels):
    assert len(input_labels) == 3 + 2
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


def add_ib_4(circuit, input_labels):
    assert len(input_labels) == 4 + 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [u0, u1, x1, x2, x3, x4] = input_labels

    a0, a1 = add_ib_3(circuit, [u0, u1, x1, x2, x3])
    a2, a3 = add_ib_1(circuit, [a0, a1, x4])

    return a2, a3


def add_ib_5(circuit, input_labels):
    assert len(input_labels) == 5 + 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [u0, u1, x1, x2, x3, x4, x5] = input_labels

    a0, a1 = add_ib_3(circuit, [u0, u1, x1, x2, x3])
    a2, a3 = add_ib_2(circuit, [a0, a1, x4, x5])

    return a2, a3


def add_ib_6(circuit, input_labels):
    assert len(input_labels) == 6 + 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [u0, u1, x1, x2, x3, x4, x5, x6] = input_labels

    a0, a1 = add_ib_3(circuit, [u0, u1, x1, x2, x3])
    a2, a3 = add_ib_3(circuit, [a0, a1, x4, x5, x6])

    return a2, a3


def check_ib_circuit(circuit):
    tt = circuit.get_truth_tables()
    n = len(circuit.input_labels)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = tt[circuit.outputs[0]][i] * 2 + tt[circuit.outputs[1]][i]
        value = sum(x[j] for j in range(2, n))
        modd = sum((2 ** (1 - j)) * x[j] for j in range(0, 2))
        if modd == 3:
            modd = 2
        if s == 3:
            s = 2
        assert (modd + value) % 3 == s


def run(fun, size):
    c = Circuit(input_labels=[f'x{i}' for i in range(1, size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    check_ib_circuit(c)
    # c.save_to_file(f'ib/ib{len(c.input_labels) - 2}_size{len(c.gates)}')


def check_various_maj_circuits():
    run(add_ib_1, 3)
    run(add_ib_2, 4)
    run(add_ib_3, 5)
    run(add_ib_4, 6)
    run(add_ib_5, 7)
    run(add_ib_6, 8)


if __name__ == '__main__':
    check_various_maj_circuits()
