from circuit import Circuit
from itertools import product
from functions.sum import add_sum4, add_sum5, add_sum6, add_sum7


def add_th2_2(circuit, input_labels):
    assert len(input_labels) == 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2] = input_labels

    a0 = circuit.add_gate(x1, x2, '0001')

    return a0


def add_2th2_2(circuit, input_labels):
    assert len(input_labels) == 2
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2] = input_labels

    a0 = circuit.add_gate(x1, x2, '0001')
    a1 = circuit.add_gate(x1, x2, '0111')

    return a0, a1


def add_th2_3(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels

    z1 = circuit.add_gate(x1, x2, '0001')
    z2 = circuit.add_gate(x1, x2, '0111')
    z3 = circuit.add_gate(z2, x3, '0001')
    z4 = circuit.add_gate(z1, z3, '0111')

    return z4


def add_th2_4(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4] = input_labels

    z1 = circuit.add_gate(x1, x2, '0001')
    z2 = circuit.add_gate(x1, x2, '0111')

    z3 = circuit.add_gate(z2, x3, '0001')
    z4 = circuit.add_gate(z2, x3, '0111')

    z5 = circuit.add_gate(z4, x4, '0001')

    z6 = circuit.add_gate(z1, z3, '0111')
    z7 = circuit.add_gate(z5, z6, '0111')

    return z7


def add_th32_sum(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels
    z1 = circuit.add_gate(x1, x2, '0110')
    z2 = circuit.add_gate(x2, x3, '0110')
    z3 = circuit.add_gate(x3, z1, '1001')
    z4 = circuit.add_gate(z2, z1, '1000')

    return z3, z4


def add_th3_6_sum(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels
    a1, a2 = add_th32_sum(circuit, [x1, x2, x3])
    b1, b2 = add_th32_sum(circuit, [x4, x5, x6])
    c1 = add_th22_sum(circuit, [a2, a1, b2, b1])

    return c1


def add_th22_sum(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4] = input_labels
    b5 = circuit.add_gate(x3, x1, '1000')
    c5 = circuit.add_gate(x2, x1, '0100')
    d5 = circuit.add_gate(x2, x3, '1101')
    d6 = circuit.add_gate(x4, d5, '1011')
    d7 = circuit.add_gate(c5, d6, '0100')
    d8 = circuit.add_gate(b5, d7, '1001')
    return d8


def add_th3_4(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4] = input_labels

    a0, a1, a2 = add_sum4(circuit, [x1, x2, x3, x4])
    b1 = circuit.add_gate(a0, a1, '0001')
    b2 = circuit.add_gate(b1, a2, '0111')

    return b2


def add_th3_5(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels

    a0, a1, a2 = add_sum5(circuit, [x1, x2, x3, x4, x5])
    b1 = circuit.add_gate(a0, a1, '0001')
    b2 = circuit.add_gate(b1, a2, '0111')

    return b2


def add_th3_6(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels

    a0, a1, a2 = add_sum6(circuit, [x1, x2, x3, x4, x5, x6])
    b1 = circuit.add_gate(a0, a1, '0001')
    b2 = circuit.add_gate(b1, a2, '0111')

    return b2


def add_th3_7(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels

    a0, a1, a2 = add_sum7(circuit, [x1, x2, x3, x4, x5, x6, x7])
    b1 = circuit.add_gate(a0, a1, '0001')
    b2 = circuit.add_gate(b1, a2, '0111')
    return b2


def add_th2_12_29(circuit, input_labels):
    assert len(input_labels) == 12
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12] = input_labels

    z1 = circuit.add_gate(x1, x2, '0111')
    z2 = circuit.add_gate(z1, x3, '0111')
    zz1 = circuit.add_gate(z2, x4, '0111')

    z3 = circuit.add_gate(x5, x6, '0111')
    z4 = circuit.add_gate(z3, x7, '0111')
    zz2 = circuit.add_gate(z4, x8, '0111')

    z5 = circuit.add_gate(x9, x10, '0111')
    z6 = circuit.add_gate(z5, x11, '0111')
    zz3 = circuit.add_gate(z6, x12, '0111')

    z7 = circuit.add_gate(x1, x5, '0111')
    zzz1 = circuit.add_gate(z7, x9, '0111')

    z8 = circuit.add_gate(x2, x6, '0111')
    zzz2 = circuit.add_gate(z8, x10, '0111')

    z9 = circuit.add_gate(x3, x7, '0111')
    zzz3 = circuit.add_gate(z9, x11, '0111')

    z10 = circuit.add_gate(x4, x8, '0111')
    zzz4 = circuit.add_gate(z10, x12, '0111')

    a1 = add_th2_3(circuit, [zz1, zz2, zz3])
    a2 = add_th2_4(circuit, [zzz1, zzz2, zzz3, zzz4])

    a3 = circuit.add_gate(a1, a2, '0111')

    return a3


def add_th2_12_31(circuit, input_labels):
    assert len(input_labels) == 12
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12] = input_labels

    z1 = circuit.add_gate(x1, x2, '0001')
    z2 = circuit.add_gate(x1, x2, '0111')

    z3 = circuit.add_gate(z2, x3, '0001')
    z4 = circuit.add_gate(z2, x3, '0111')

    z5 = circuit.add_gate(z4, x4, '0001')
    z6 = circuit.add_gate(z4, x4, '0111')

    z7 = circuit.add_gate(z6, x5, '0001')
    z8 = circuit.add_gate(z6, x5, '0111')

    z9 = circuit.add_gate(z8, x6, '0001')
    z10 = circuit.add_gate(z8, x6, '0111')

    z11 = circuit.add_gate(z10, x7, '0001')
    z12 = circuit.add_gate(z10, x7, '0111')

    z13 = circuit.add_gate(z12, x8, '0001')
    z14 = circuit.add_gate(z12, x8, '0111')

    z15 = circuit.add_gate(z14, x9, '0001')
    z16 = circuit.add_gate(z14, x9, '0111')

    z17 = circuit.add_gate(z16, x10, '0001')
    z18 = circuit.add_gate(z16, x10, '0111')

    z19 = circuit.add_gate(z18, x11, '0001')
    z20 = circuit.add_gate(z18, x11, '0111')

    z21 = circuit.add_gate(z20, x12, '0001')

    z22 = circuit.add_gate(z1, z3, '0111')
    z23 = circuit.add_gate(z22, z5, '0111')
    z24 = circuit.add_gate(z23, z7, '0111')
    z25 = circuit.add_gate(z24, z9, '0111')
    z26 = circuit.add_gate(z25, z11, '0111')
    z27 = circuit.add_gate(z26, z13, '0111')
    z28 = circuit.add_gate(z27, z15, '0111')
    z29 = circuit.add_gate(z28, z17, '0111')
    z30 = circuit.add_gate(z29, z19, '0111')
    z21 = circuit.add_gate(z30, z21, '0111')

    return z21


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


def check_th_circuit(circuit, k):
    truth_tables = circuit.get_truth_tables()
    n = len(circuit.input_labels)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = truth_tables[circuit.outputs[0]][i]
        assert (sum(x) >= k) == s


def check_2th_circuit(circuit, k):
    truth_tables = circuit.get_truth_tables()
    n = len(circuit.input_labels)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = truth_tables[circuit.outputs[0]][i]
        t = truth_tables[circuit.outputs[1]][i]
        assert ((sum(x) >= k) == s) and ((sum(x) != 0) == t)


def run(fun, size, k):
    c = Circuit(input_labels=[f'x{i}' for i in range(1, size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    check_th_circuit(c, k)
    # c.save_to_file(f'th/ans29')


def run31():
    c = Circuit(input_labels=[f'x{i}' for i in range(1, 12 + 1)], gates={})
    c.outputs = add_naive_thr2_circuit(c, c.input_labels)
    check_th_circuit(c, 2)


def run29():
    c = Circuit(input_labels=[f'x{i}' for i in range(1, 12 + 1)], gates={})
    c.outputs = add_efficient_thr2_circuit(c, c.input_labels,3,4)
    check_th_circuit(c, 2)


def run2(fun, size, k):
    c = Circuit(input_labels=[f'x{i}' for i in range(1, size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    check_2th_circuit(c, k)
    # c.save_to_file(f'maj/maj{len(c.input_labels)}_size{len(c.gates)}')


def check_various_th_circuits():
    # run(add_th2_2, 2, 2)
    # run(add_th2_3, 3, 2)
    # run(add_th2_4, 4, 2)
    # run(add_th3_4, 4, 3)
    # run(add_th3_5, 5, 3)
    # run(add_th3_6, 6, 3)
    # run(add_th3_7, 7, 3)
    # run(add_th3_6_sum, 6, 3)
    # run(add_th2_12, 12, 2)
    # run(add_th2_12_29, 12, 2)
    # run(add_th2_12_31, 12, 2)
    run31()
    run29()


if __name__ == '__main__':
    check_various_th_circuits()
