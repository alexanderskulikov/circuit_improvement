from circuit import Circuit
from itertools import product


def check_sum_circuit(circuit):
    truth_tables = circuit.get_truth_tables()
    n = len(circuit.input_labels)

    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = sum(truth_tables[circuit.outputs[d]][i] * (2 ** d) for d in range(len(circuit.outputs)))
        assert s == sum(x)


def run(fun, size):
    c = Circuit(input_labels=[f'x{i}' for i in range(1, size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    check_sum_circuit(c)
    # c.save_to_file(f'sum/sum{len(c.input_labels)}_size{len(c.gates)}')


def check_various_sum_circuits():
    run(add_sum2, 2)


    #c = Circuit(input_labels=[f'x{i}' for i in range(1, 7 + 1)], gates={})
    #c.outputs = add_sum7_suboptimal(c, c.input_labels)
    #check_sum_circuit(c)
    #c.save_to_file(f'sum/sum7_sub')

    #c = Circuit()
    #c.load_from_file('sum/sum7_size20')
    #check_sum_circuit(c)


check_various_sum_circuits()
