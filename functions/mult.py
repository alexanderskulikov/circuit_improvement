from functions.sum import *


def add_mul(circuit, input_labels_a, input_labels_b):
    n = len(input_labels_a)
    m = len(input_labels_b)
    for input_label in input_labels_a:
        assert input_label in circuit.input_labels or input_label in circuit.gates
    for input_label in input_labels_b:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    # in my mind a[0] is the smallest bit in a
    c = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            c[i][j] = circuit.add_gate(input_labels_a[j], input_labels_b[i], '0001')

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
        if(len(inp) == 1):
            d[i] = [inp[0]]
        else:
            d[i] = add_sum(circuit, inp)
    return [d[i][0] for i in range(n + m)]


def add_mul_alter(circuit, input_labels_a, input_labels_b):
    n = len(input_labels_a)
    m = len(input_labels_b)
    for input_label in input_labels_a:
        assert input_label in circuit.input_labels or input_label in circuit.gates
    for input_label in input_labels_b:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    # in my mind a[0] is the smallest bit in a
    c = [[0] * n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            c[i][j] = circuit.add_gate(input_labels_a[j], input_labels_b[i], '0001')
    if m == 1:
        return [c[0]]

    res = add_sum_two_numbers_with_shift(circuit, 1, c[0], c[1])
    for i in range(2, m):
        res = add_sum_two_numbers_with_shift(circuit, i, res, c[i])

    return res
