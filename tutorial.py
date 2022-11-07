# This tutorial shows the main features of the program.
# To run it in the cloud, press the Google Colab badge above
# and run the notebook.


from core.circuit import Circuit
from math import ceil, log2
from functions.sum import add_sum2, add_sum3, check_sum_circuit, add_sum5_suboptimal
from functions.th import add_naive_thr2_circuit, add_efficient_thr2_circuit
from core.circuit_search import CircuitFinder
from core.circuit_improvement import improve_circuit


# Straight line program computing the binary representation of x1+x2
def sum2(x1, x2):
    w0 = x1 ^ x2
    w1 = x1 * x2
    return w0, w1


# Straight line program computing the binary representation of x1+x2+x3
def sum3(x1, x2, x3):
    a = x1 ^ x2
    b = x2 ^ x3
    c = a | b
    w0 = a ^ x3
    w1 = c ^ w0
    return w0, w1


# Verify correctness of the SUM3 circuit
from itertools import product

for x1, x2, x3 in product(range(2), repeat=3):
    w0, w1 = sum3(x1, x2, x3)
    assert x1 + x2 + x3 == w0 + 2 * w1


# Build a circuit for SUM5 out of SUM2 and SUM3 blocks
circuit = Circuit(input_labels=['x1', 'x2', 'x3', 'x4', 'x5'])
x1, x2, x3, x4, x5 = circuit.input_labels
a0, a1 = add_sum3(circuit, [x1, x2, x3])
b0, b1 = add_sum3(circuit, [a0, x4, x5])
w1, w2 = add_sum2(circuit, [a1, b1])
circuit.outputs = [b0, w1, w2]
check_sum_circuit(circuit)
circuit.draw('sum5')


# Find an optimum circuit for SUM3 using SAT-solvers
def sum_n(x):
    return [(sum(x) >> i) & 1 for i in range(ceil(log2(len(x) + 1)))]


circuit_finder = CircuitFinder(dimension=3, number_of_gates=5,
                               function=sum_n)
circuit = circuit_finder.solve_cnf_formula()
circuit.draw('sum3')


# Improve the SUM5 circuit of size 12
circuit = Circuit(input_labels=[f'x{i}' for i in range(1, 6)], gates={})
circuit.outputs = add_sum5_suboptimal(circuit, circuit.input_labels)
improved_circuit = improve_circuit(circuit, subcircuit_size=5,
                                   connected=True)
print(improved_circuit)
improved_circuit.draw('sum5')


# Find a circuit for SUM_n (for n=3,4,5) with special structure
def sum_n(x):
    return [(sum(x) >> i) & 1 for i in range(ceil(log2(len(x) + 1)))]


for n, size in ((3, 5), (4, 9), (5, 11)):
    circuit_finder = CircuitFinder(dimension=n, number_of_gates=size,
                                   function=sum_n)
    circuit_finder.fix_gate(n, 0, 1, '0110')
    for k in range(n - 2):
        circuit_finder.fix_gate(n + k + 1, k + 2, n + k, '0110')
    for i in range(1, n):
        for j in range(n, n + size):
            if i + n - 1 != j:
                circuit_finder.forbid_wire(i, j)
    circuit = circuit_finder.solve_cnf_formula(verbose=0)
    circuit.draw(f'sum{n}')


# Construct two circuits for THR2 for n=12: of size 3n-5 and of size 2n+o(n)
c = Circuit(input_labels=[f'x{i}' for i in range(1, 13)], gates={})
c.outputs = add_naive_thr2_circuit(c, c.input_labels)
c.draw('thr2naive')

c = Circuit(input_labels=[f'x{i}' for i in range(1, 13)], gates={})
c.outputs = add_efficient_thr2_circuit(c, c.input_labels, 3, 4)
c.draw('thr2efficient')
