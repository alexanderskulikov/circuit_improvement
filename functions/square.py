from functions.sum import *


def add_square(circuit, input_labels):
    n = len(input_labels)
    for input_label in input_labels:
        assert input_label in circuit.input_labels or input_label in circuit.gates

    # in my mind a[0] is the smallest bit in a
    c = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            c[i][j] = circuit.add_gate(input_labels[i], input_labels[j], '0001')
    for i in range(n):
        c[i][i] = input_labels[i]

    d = [[0] for _ in range(2*n)]
    d[0] = [[c[0][0]]]
    d[1] = [["0"]]
    for i in range(2, 2*n):
        print(*d)
        inp = []
        for j in range(i//2):
            if j < n and  -1 < i - j - 1 < n:
                inp.append(c[j][i - j - 1])
        if i%2 == 0:
            inp.append(c[i//2][i//2])
        #print(len(inp), end = "/")
        for j in range(i):
            if j + len(d[j]) > i:
                inp += (d[j][i - j])
        #print(len(inp))
        if(len(inp) == 1):
            d[i] = [[inp[0]]]
        else:
            d[i] = add_sum_alter(circuit, inp)
    return [d[i][0][0] for i in range(2*n)]


ckt = Circuit(input_labels=[f'x{i}' for i in range(12)])
print(add_square(ckt, ckt.input_labels))
print(ckt)