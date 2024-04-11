from functions.sum import *


def add_mul_n_m(circuit, n, m, input_labels):
    assert len(input_labels) == n + m
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    # in my mind a[0] is the smallest bit in a.

    a = [0] * n
    b = [0] * m
    for i in range(n):
        a[i] = input_labels[i]
    for i in range(m):
        b[i] = input_labels[i + n]

    c = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            c[i][j] = circuit.add_gate(a[j], b[i], '0001')

    d = [[0] for _ in range(n + m)]
    d[0] = [c[0][0]]
    for i in range(1, n + m):
        inp = []
        for j in range(i + 1):
            if j < m and i - j < n:
                inp.append(c[j][i - j])
        for j in range(i):
            if j + len(d[j]) > i:
                inp.append(d[j][i - j])
        d[i] = add_sum(circuit, inp)
    return [d[i][0] for i in range(n + m)]


def add_mul_6_6(circuit, input_labels):
    assert len(input_labels) == 12
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    # in my mind a[0] is the smallest bit in a.
    # the most easy implementation

    n = 6
    a = [0] * n
    b = [0] * n
    for i in range(n):
        a[i] = input_labels[i]
        b[i] = input_labels[i + n]

    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            c[i][j] = circuit.add_gate(a[i], b[j], '0001')

    d = [[0] for _ in range(2 * n)]
    d[0] = [c[0][0]]
    print(d)
    for i in range(1, 2 * n):
        inp = []
        for j in range(i + 1):
            if j < n and i - j < n:
                inp.append(c[j][i - j])
        for j in range(i):
            if j + len(d[j]) > i:
                inp.append(d[j][i - j])
        print(inp)
        # continue
        d[i] = add_sum(circuit, inp)
    return [d[i][0] for i in range(2 * n)]


def add_mul_4_4(circuit, input_labels):
    assert len(input_labels) == 8
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    # in my mind a[0] is the smallest bit in a

    # n = 4
    # a = [] * n
    # b = [] * n
    # for i in range(n):
    #     a[i] = input_labels[i]
    #     b[i] = input_labels[i + n]
    #
    # c = [[0] * n for _ in range(n)]
    # for i in range(n):
    #     for j in range(n):
    #         c[i][j] = circuit.add_gate(a[i], b[j], '0001')
    #
    # return c

    # the most easy implementation

    a0, a1, a2, a3, b0, b1, b2, b3 = input_labels
    c00 = circuit.add_gate(a0, b0, '0001')
    c01 = circuit.add_gate(a0, b1, '0001')
    c02 = circuit.add_gate(a0, b2, '0001')
    c03 = circuit.add_gate(a0, b3, '0001')
    c10 = circuit.add_gate(a1, b0, '0001')
    c11 = circuit.add_gate(a1, b1, '0001')
    c12 = circuit.add_gate(a1, b2, '0001')
    c13 = circuit.add_gate(a1, b3, '0001')
    c20 = circuit.add_gate(a2, b0, '0001')
    c21 = circuit.add_gate(a2, b1, '0001')
    c22 = circuit.add_gate(a2, b2, '0001')
    c23 = circuit.add_gate(a2, b3, '0001')
    c30 = circuit.add_gate(a3, b0, '0001')
    c31 = circuit.add_gate(a3, b1, '0001')
    c32 = circuit.add_gate(a3, b2, '0001')
    c33 = circuit.add_gate(a3, b3, '0001')

    d10, d11 = add_sum2(circuit, [c10, c01])
    d20, d21, d22 = add_sum4(circuit, [d11, c20, c11, c02])
    d30, d31, d32 = add_sum5_size11(circuit, [d21, c30, c21, c12, c03])
    d40, d41, d42 = add_sum5_size11(circuit, [c31, c22, c13, d31, d22])
    d50, d51, d52 = add_sum4(circuit, [c23, c32, d41, d32])
    d60, d61 = add_sum3(circuit, [c33, d51, d42])
    d70 = circuit.add_gate(d61, d50, '0111')

    return c00, d10, d20, d30, d40, d50, d60, d70
