from core.circuit_improvement import improve_circuit
from functions.sum import *
from core.circuit_search import *

circuit = Circuit()
circuit.load_from_file('ex98', extension='bench')

was_improved = True
while was_improved:
    was_improved = False

    for subcircuit_size in range(2, 6):
        better_circuit = improve_circuit(circuit, subcircuit_size=subcircuit_size)
        if isinstance(better_circuit, Circuit):
            was_improved = True
            circuit = better_circuit
            break
