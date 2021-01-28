from circuit import Circuit
from itertools import product


def add_maj2(circuit, input_labels):
    assert len(input_labels) == 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2] = input_labels

    a0 = circuit.add_gate(x1, x2, '0111')

    return a0


def add_maj3(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels

    a0 = circuit.add_gate(x1, x2, '0001')
    a1 = circuit.add_gate(x1, x2, '1000')
    a2 = circuit.add_gate(x3, a1, '0010')
    a3 = circuit.add_gate(a0, a2, '0111')

    return a3


def add_maj4(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4] = input_labels

    a0 = circuit.add_gate(x1, x2, '0001')
    a1 = circuit.add_gate(x3, x4, '0111')
    a2 = circuit.add_gate(x3, x4, '0001')
    a3 = circuit.add_gate(x1, a2, '1000')
    a4 = circuit.add_gate(x2, a3, '1011')
    a5 = circuit.add_gate(a1, a4, '1110')
    a6 = circuit.add_gate(a0, a5, '1011')

    return a6


def add_maj5(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    a0 = circuit.add_gate(x1, x2, '1001')
    a1 = circuit.add_gate(x3, x4, '0110')
    a2 = circuit.add_gate(x3, x4, '0001')
    a3 = circuit.add_gate(x2, a1, '0001')
    a4 = circuit.add_gate(a0, a1, '1001')
    a5 = circuit.add_gate(a2, a3, '0110')
    a6 = circuit.add_gate(x1, a5, '0110')
    a7 = circuit.add_gate(a4, a6, '1011')
    a8 = circuit.add_gate(x5, a7, '1000')
    a9 = circuit.add_gate(a7, a5, '1101')
    a10 = circuit.add_gate(a8, a9, '0110')

    return a10


def add_maj5_new(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    a1 = circuit.add_gate(x1, x2, '0110')
    a2 = circuit.add_gate(a1, x3, '0110')
    a3 = circuit.add_gate(a2, x4, '0110')
    a4 = circuit.add_gate(a3, x5, '0110')

    a5 = circuit.add_gate(a2, a4, '0110')
    a6 = circuit.add_gate(x1, a2, '0110')
    a7 = circuit.add_gate(a3, a5, '0111')
    a8 = circuit.add_gate(a1, a6, '0111')
    a9 = circuit.add_gate(a7, a8, '0001')
    a10 = circuit.add_gate(a2, a9, '0110')

    return a10


def add_maj6(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels

    a0 = circuit.add_gate(x1, x2, '1000')
    a1 = circuit.add_gate(x2, x3, '0110')
    a2 = circuit.add_gate(x4, x5, '1001')
    a3 = circuit.add_gate(x5, x6, '1110')
    a4 = circuit.add_gate(x1, a1, '1001')
    a5 = circuit.add_gate(x6, a2, '1001')
    a6 = circuit.add_gate(x3, a4, '1000')
    a7 = circuit.add_gate(a5, x4, '0100')
    a8 = circuit.add_gate(a3, a7, '1101')
    a9 = circuit.add_gate(a0, a8, '0110')
    a10 = circuit.add_gate(a5, a9, '1000')
    a11 = circuit.add_gate(a4, a10, '1110')
    a12 = circuit.add_gate(a6, a0, '0110')
    a13 = circuit.add_gate(a8, a12, '0100')
    a14 = circuit.add_gate(a11, a13, '0110')

    return a14


def add_maj7(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels
    z0 = circuit.add_gate(x1, x2, '0110')
    z1 = circuit.add_gate(x2, x3, '0110')
    z2 = circuit.add_gate(z0, z1, '0111')
    z3 = circuit.add_gate(z0, x3, '0110')
    z4 = circuit.add_gate(z2, z3, '0110')
    z5 = circuit.add_gate(x4, z3, '0110')
    z6 = circuit.add_gate(x4, x5, '0110')
    z7 = circuit.add_gate(z5, z6, '0010')
    z8 = circuit.add_gate(z3, z6, '0110')
    z9 = circuit.add_gate(z2, z7, '0110')
    z10 = circuit.add_gate(z4, z9, '0010')
    z11 = circuit.add_gate(z8, x6, '0110')
    z12 = circuit.add_gate(x6, x7, '0110')
    z13 = circuit.add_gate(z11, z12, '0111')
    z14 = circuit.add_gate(z11, x7, '0110')
    z15 = circuit.add_gate(z13, z14, '0110')
    z17 = circuit.add_gate(z9, z15, '0001')
    z18 = circuit.add_gate(z10, z17, '0110')

    return z18


def add_op36(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels
    z0 = circuit.add_gate(x1, x2, '0110')
    z1 = circuit.add_gate(z0, x3, '0110')
    z2 = circuit.add_gate(z1, x4, '0110')
    z3 = circuit.add_gate(z2, x5, '0110')
    z4 = circuit.add_gate(z3, x6, '0110')

    y0 = circuit.add_gate(x1, z0, '0111')
    y1 = circuit.add_gate(y0, z1, '0111')
    y2 = circuit.add_gate(y1, z2, '0111')
    y3 = circuit.add_gate(y2, z3, '0111')
    y4 = circuit.add_gate(y3, z4, '0111')

    t0 = circuit.add_gate(x1, z0, '0010')
    t1 = circuit.add_gate(z1, z2, '0010')
    t2 = circuit.add_gate(z3, z4, '0010')
    t3 = circuit.add_gate(t0, t1, '0001')
    t4 = circuit.add_gate(t3, t2, '0001')

    return z4, y4, t4


def check_maj_circuit(circuit):
    truth_tables = circuit.get_truth_tables()
    n = len(circuit.input_labels)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    maj = n//2 if n % 2 == 0 else n//2+1
    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = truth_tables[circuit.outputs[0]][i]
        assert (sum(x) >= maj) == s


def proof_maj_circuit(size):
    n = size
    ans = []
    maj = n//2 if n % 2 == 0 else n//2+1
    for x in product(range(2), repeat=n):
        ans.append(1 if sum(x) >= maj else 0)
    print(ans)


def run(fun, size):
    c = Circuit(input_labels=[f'x{i}' for i in range(1, size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    check_maj_circuit(c)
    # c.save_to_file(f'maj/maj{len(c.input_labels)}_size{len(c.gates)}')


def check_various_maj_circuits():
    run(add_maj2, 2)
    run(add_maj3, 3)
    run(add_maj4, 4)
    run(add_maj5, 5)
    run(add_maj6, 6)
    run(add_maj7, 7)
    run(add_maj5_new, 5)


if __name__ == '__main__':
    check_various_maj_circuits()
