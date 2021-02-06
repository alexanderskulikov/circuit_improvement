from circuit_improvement import *
from functions.ex3 import *
from functions.ex2 import *
from functions.sum import *
from functions.ib import *
from functions.maj import *
from functions.mod3 import *
from functions.th import *


def run_file(filename, subcircuit_size=5, connected=True):
    print(f'Run {filename}...')
    circuit = Circuit()
    circuit.load_from_file(filename)
    improve_circuit(circuit, subcircuit_size, connected)


def run(fun, input_size, subcircuit_size=5, connected=True):
    print(f'Run {fun.__name__}...')
    circuit = Circuit(input_labels=[f'x{i}' for i in range(1, input_size + 1)], gates={})
    circuit.outputs = fun(circuit, circuit.input_labels)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    improve_circuit(circuit, subcircuit_size, connected)


if __name__ == '__main__':
    command = 'r'

    if command == 'r':
        run(add_sum5_suboptimal, 5, subcircuit_size=5, connected=True)
    elif command == 'rf':
        run_file('sum/sum7_sub', subcircuit_size=5, connected=True)
    elif command == 'mc':
        Circuit.make_code('ex/ex2_over1_size13', 'code')
    elif command == 'd':
        c = Circuit(fn='sum/sum3_size5').draw('sum3_size5')
