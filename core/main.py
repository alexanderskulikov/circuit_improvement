from circuit_improvement import *
from circuit_pair_finder import *
from functions.ex3 import *
from functions.ex2 import *
from functions.sum import *
from functions.ib import *
from functions.maj import *
from functions.mod3 import *
from functions.th import *


def run_file_improve_circuit(filename, subcircuit_size=5, connected=True):
    print(f'Run {filename}...')
    circuit = Circuit()
    circuit.load_from_file(filename, extension='ckt')
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    return improve_circuit(circuit, subcircuit_size, connected)


def run_improve_circuit(fun, input_size, subcircuit_size=5, connected=True):
    print(f'Run {fun.__name__}...')
    circuit = Circuit(input_labels=[f'x{i}' for i in range(1, input_size + 1)], gates={})
    circuit.outputs = fun(circuit, circuit.input_labels)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    return improve_circuit(circuit)


if __name__ == '__main__':
    command = 'rf'

    if command == 'r':
        start = timer()
        improved_circuit = run_improve_circuit(add_sum7_exp, 7, subcircuit_size=6, connected=True)
        print(timer() - start)
        if improved_circuit is not None:
            print(improved_circuit)
            improved_circuit.save_to_file('sum7_min')
    elif command == 'rf':
        start = timer()
        filename = "sum7_min_B"
        improved_circuit = run_file_improve_circuit(filename, subcircuit_size=7, connected=True)
        print(timer() - start)
        if improved_circuit is not None:
            print(improved_circuit)
            improved_circuit.save_to_file('sum7_min_B')
    elif command == 'mc':
        Circuit.make_code('ex/ex2_over1_size13', 'code')
    elif command == 'd':
        c = Circuit(fn='sum/sum3_size5').draw('sum3_size5')
