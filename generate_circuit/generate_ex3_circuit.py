from circuit import Circuit
from itertools import product
from itertools import permutations


def add_ex3_3(circuit, input_labels):
    assert len(input_labels) == 3
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3] = input_labels

    a0 = circuit.add_gate(x1, x2, '0001')
    a1 = circuit.add_gate(a0, x3, '0001')

    return a1


def add_ex3_4(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4] = input_labels

    a0 = circuit.add_gate(x1, x2, '0001')
    a1 = circuit.add_gate(x3, x4, '0110')
    a2 = circuit.add_gate(a0, a1, '0001')

    b0 = circuit.add_gate(x1, x2, '0110')
    b1 = circuit.add_gate(x3, x4, '0001')
    b2 = circuit.add_gate(b0, b1, '0001')

    c0 = circuit.add_gate(a2, b2, '0111')

    return c0


# сумма двух спешассых сумм и входного бита, результат уже ex3
def add_ex3_221(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5] = input_labels
    k6 = circuit.add_gate(x4, x2, '1001')
    g4 = circuit.add_gate(x4, x3, '1011')
    j8 = circuit.add_gate(k6, x3, '1001')
    m6 = circuit.add_gate(x5, x1, '0010')
    m7 = circuit.add_gate(k6, m6, '0110')
    m8 = circuit.add_gate(x5, g4, '0001')
    m9 = circuit.add_gate(x1, m8, '0010')
    m10 = circuit.add_gate(j8, m9, '0110')
    m11 = circuit.add_gate(m7, m10, '0001')

    return m11


# получение смешанной суммы для трех гейтов
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


def add_ex3_7_sum(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels
    a1, a2 = add_ex32_sum(circuit, [x1, x2, x3])
    b1, b2 = add_ex32_sum(circuit, [x4, x5, x6])
    c1 = add_ex3_221(circuit, [a2, a1, b2, b1, x7])

    return c1


# сложение двух смешанных сумм, плюс индикатор переполнения
def add_ex3_over(circuit, input_labels):
    assert len(input_labels) == 4
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x4, x3, x2] = input_labels
    z4 = circuit.add_gate(x1, x3, '0110')
    z5 = circuit.add_gate(x1, z4, '1101')
    z6 = circuit.add_gate(x4, x2, '0110')
    z7 = circuit.add_gate(z5, z6, '1101')
    z8 = circuit.add_gate(x1, z7, '1110')
    z9 = circuit.add_gate(z4, z6, '1001')
    z10 = circuit.add_gate(x4, z9, '1110')
    z11 = circuit.add_gate(z8, z10, '0110')

    return z11, z4, z7


# сложение двух смешанных сумм и еще одного входного бита, плюс индикатор переполнения
def add_ex3_over1(circuit, input_labels):
    assert len(input_labels) == 5
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [a2, b1, b2, a1, x] = input_labels
    z5 = circuit.add_gate(a1, b1, '1001')
    z6 = circuit.add_gate(x, a2, '1001')
    z7 = circuit.add_gate(a2, z5, '0110')
    z8 = circuit.add_gate(z5, z6, '1110')
    z9 = circuit.add_gate(b2, z7, '0110')
    z10 = circuit.add_gate(z6, z9, '0111')
    z11 = circuit.add_gate(a1, z8, '0110')
    z12 = circuit.add_gate(z9, z11, '1011')
    z13 = circuit.add_gate(a1, z12, '1001')
    z14 = circuit.add_gate(z7, z13, '1001')
    z15 = circuit.add_gate(b2, z6, '1001')
    z16 = circuit.add_gate(z8, z10, '1001')

    return z14, z15, z16


def add_ex3_6_withover(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6] = input_labels
    a1, a2 = add_ex32_sum(circuit, [x1, x2, x3])
    b1, b2 = add_ex32_sum(circuit, [x4, x5, x6])
    over, c1, c0 = add_ex3_over(circuit, [a2, a1, b2, b1])
    d1 = circuit.add_gate(c1, c0, '0010')
    d2 = circuit.add_gate(over, d1, '0100')

    return d2


def add_ex3_7_withover(circuit, input_labels):
    assert len(input_labels) == 7
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7] = input_labels
    a1, a2 = add_ex32_sum(circuit, [x1, x2, x3])
    b1, b2 = add_ex32_sum(circuit, [x4, x5, x6])
    over, c1, c0 = add_ex3_over1(circuit, [a2, a1, b2, b1, x7])
    d1 = circuit.add_gate(c1, c0, '0010')
    d2 = circuit.add_gate(over, d1, '0100')

    return d2


def add_ex3_3megrg3(circuit, input_labels):
    assert len(input_labels) == 6
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [a3, a2, a1, b3, b2, b1] = input_labels
    ans1 = circuit.add_gate(a1, b1, '0111')
    c1 = circuit.add_gate(a1, b1, '0001')
    c2 = circuit.add_gate(a2, b2, '0111')
    ans2 = circuit.add_gate(c1, c2, '0111')

    d1 = circuit.add_gate(a1, b2, '0001')
    d2 = circuit.add_gate(a2, b1, '0001')
    d3 = circuit.add_gate(a3, b3, '0111')
    d5 = circuit.add_gate(d1, d2, '0111')
    ans3 = circuit.add_gate(d5, d3, '0111')

    return ans3, ans2, ans1

def add_ex3_9(circuit, input_labels):
    assert len(input_labels) == 9
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9] = input_labels
    a1, a2 = add_ex32_sum(circuit, [x1, x2, x3])
    b1, b2 = add_ex32_sum(circuit, [x4, x5, x6])
    c1, c2 = add_ex32_sum(circuit, [x7, x8, x9])
    over1, e1, e0 = add_ex3_over(circuit, [a2, a1, b2, b1])
    over2, g1, g0 = add_ex3_over(circuit, [c2, c1, e1, e0])
    ans = circuit.add_gate(g1, g0, '0010')
    o1 = circuit.add_gate(over1, over2, '0111')
    o3 = circuit.add_gate(o1, ans, '0100')
    return o3


def add_ex3_15(circuit, input_labels):
    assert len(input_labels) == 15
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    [x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15] = input_labels
    a1, a2 = add_ex32_sum(circuit, [x1, x2, x3])
    b1, b2 = add_ex32_sum(circuit, [x4, x5, x6])
    c1, c2 = add_ex32_sum(circuit, [x7, x8, x9])
    d1, d2 = add_ex32_sum(circuit, [x10, x11, x12])
    over1, e1, e0 = add_ex3_over1(circuit, [a2, a1, b2, b1, x13])
    over2, f1, f0 = add_ex3_over1(circuit, [c2, c1, d2, d1, x14])
    over3, g1, g0 = add_ex3_over1(circuit, [e1, e0, f1, f0, x15])
    ans = circuit.add_gate(g1, g0, '0010')
    o1 = circuit.add_gate(over1, over2, '0111')
    o2 = circuit.add_gate(o1, over3, '0111')
    o3 = circuit.add_gate(o2, ans, '0100')
    return o3


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
    run(add_ex3_3, 3, 3)
    run(add_ex3_4, 4, 3)
    run(add_ex3_7_sum, 7, 3)
    run(add_ex3_6_withover, 6, 3)
    run(add_ex3_7_withover, 7, 3)
    run(add_ex3_9, 9, 3)
    run(add_ex3_15, 15, 3)

    #c = Circuit()
    #c.load_from_file('ex/ex2_5_size14')
    #check_ex_circuit(c, 2)


check_various_ex_circuits()
