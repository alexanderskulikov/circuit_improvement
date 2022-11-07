from core.circuit import Circuit
from itertools import product


def add_ex2_2(circuit, input_labels):
    assert len(input_labels) == 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2] = input_labels

    a0 = circuit.add_gate(x1, x2, '0001')

    return a0


def add_ex2_3(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels

    a3 = circuit.add_gate(x1, x2, '1001')
    a4 = circuit.add_gate(x1, x2, '0111')
    a5 = circuit.add_gate(x3, a4, '1011')
    a6 = circuit.add_gate(a3, a5, '0110')

    return a6


def add_ex32_sum(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels
    z1 = circuit.add_gate(x1, x2, '1001')
    z2 = circuit.add_gate(x2, x3, '1001')
    z3 = circuit.add_gate(x1, z2, '1001')
    z4 = circuit.add_gate(z1, z2, '1110')

    return z4, z3


def add_ex2_over1(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x0, x3, x2, x4] = input_labels

    z5 = circuit.add_gate(x1, x4, '0110')
    z7 = circuit.add_gate(x2, z5, '1101')
    z8 = circuit.add_gate(x3, z7, '0100')
    z9 = circuit.add_gate(x4, z5, '0111')
    z10 = circuit.add_gate(z7, z9, '1001')
    z11 = circuit.add_gate(x3, z5, '0110')
    z12 = circuit.add_gate(x0, z10, '0111')
    z13 = circuit.add_gate(x0, z10, '1110')
    z14 = circuit.add_gate(x2, z8, '1001')
    z15 = circuit.add_gate(x1, z13, '1001')
    z16 = circuit.add_gate(z14, z15, '1000')

    return z16, z11, z12


def add_ex2_7_withover(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels
    a1, a2 = add_ex32_sum(circuit, [x1, x2, x3])
    b1, b2 = add_ex32_sum(circuit, [x4, x5, x6])
    over, c1, c0 = add_ex2_over1(circuit, [a2, a1, b2, b1, x7])
    d1 = circuit.add_gate(c1, c0, '0100')
    d2 = circuit.add_gate(over, d1, '0001')

    return d2


def add_sq2(circuit, input_labels):
    assert len(input_labels) == 8
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [a1, a2, a3, a4, b1, b2, b3, b4] = input_labels
    z11 = circuit.add_gate(a1, b1, '0001')
    z23 = circuit.add_gate(a2, b3, '0001')
    z12 = circuit.add_gate(a1, b2, '0001')
    z24 = circuit.add_gate(a2, b4, '0001')
    z31 = circuit.add_gate(a3, b1, '0001')
    z43 = circuit.add_gate(a4, b3, '0001')
    z32 = circuit.add_gate(a3, b2, '0001')
    z44 = circuit.add_gate(a4, b4, '0001')

    y1 = circuit.add_gate(z11, z23, '0110')
    y2 = circuit.add_gate(z12, z24, '0110')
    y3 = circuit.add_gate(z31, z43, '0110')
    y4 = circuit.add_gate(z32, z44, '0110')

    return y1, y2, y3, y4


def add_sq3(circuit, input_labels):
    assert len(input_labels) == 18
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [a1, a2, a3, a4, a5, a6, a7, a8, a9, b1, b2, b3, b4, b5, b6, b7, b8, b9] = input_labels
    z11 = circuit.add_gate(a1, b1, '0001')
    z24 = circuit.add_gate(a2, b4, '0001')
    z37 = circuit.add_gate(a3, b7, '0001')

    y1 = circuit.add_gate(z11, z24, '0110')
    y11 = circuit.add_gate(y1, z37, '0110')

    z12 = circuit.add_gate(a1, b2, '0001')
    z25 = circuit.add_gate(a2, b5, '0001')
    z38 = circuit.add_gate(a3, b8, '0001')

    y2 = circuit.add_gate(z12, z25, '0110')
    y12 = circuit.add_gate(y2, z38, '0110')

    z13 = circuit.add_gate(a1, b3, '0001')
    z26 = circuit.add_gate(a2, b6, '0001')
    z39 = circuit.add_gate(a3, b9, '0001')

    y3 = circuit.add_gate(z13, z26, '0110')
    y13 = circuit.add_gate(y3, z39, '0110')

    z41 = circuit.add_gate(a4, b1, '0001')
    z54 = circuit.add_gate(a5, b4, '0001')
    z67 = circuit.add_gate(a6, b7, '0001')

    y4 = circuit.add_gate(z41, z54, '0110')
    y21 = circuit.add_gate(y4, z67, '0110')

    z42 = circuit.add_gate(a4, b2, '0001')
    z55 = circuit.add_gate(a5, b5, '0001')
    z68 = circuit.add_gate(a6, b8, '0001')

    y5 = circuit.add_gate(z42, z55, '0110')
    y22 = circuit.add_gate(y5, z68, '0110')

    z43 = circuit.add_gate(a4, b3, '0001')
    z56 = circuit.add_gate(a5, b6, '0001')
    z69 = circuit.add_gate(a6, b9, '0001')

    y6 = circuit.add_gate(z43, z56, '0110')
    y23 = circuit.add_gate(y6, z69, '0110')

    z71 = circuit.add_gate(a7, b1, '0001')
    z84 = circuit.add_gate(a8, b4, '0001')
    z97 = circuit.add_gate(a9, b7, '0001')

    y7 = circuit.add_gate(z71, z84, '0110')
    y31 = circuit.add_gate(y7, z97, '0110')

    z72 = circuit.add_gate(a7, b2, '0001')
    z85 = circuit.add_gate(a8, b5, '0001')
    z98 = circuit.add_gate(a9, b8, '0001')

    y8 = circuit.add_gate(z72, z85, '0110')
    y32 = circuit.add_gate(y8, z98, '0110')

    z73 = circuit.add_gate(a7, b3, '0001')
    z86 = circuit.add_gate(a8, b6, '0001')
    z99 = circuit.add_gate(a9, b9, '0001')

    y9 = circuit.add_gate(z73, z86, '0110')
    y33 = circuit.add_gate(y9, z99, '0110')

    return y11, y12, y13, y21, y22, y23, y31, y32, y33


def check_ex_circuit(circuit, k):
    truth_tables = circuit.get_truth_tables()
    n = len(circuit.input_labels)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = truth_tables[circuit.outputs[0]][i]
        assert (sum(x) == k) == s, f'{x}'


def run(fun, size, k):
    c = Circuit(input_labels=[f'x{i}' for i in range(1, size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    check_ex_circuit(c, k)
    # c.save_to_file(f'ex/ex{k}_{len(c.input_labels)}_size{len(c.gates)}')


def check_various_ex_circuits():
    run(add_ex2_2, 2, 2)
    run(add_ex2_3, 3, 2)


if __name__ == '__main__':
    check_various_ex_circuits()
