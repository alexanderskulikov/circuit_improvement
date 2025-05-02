from core.circuit import Circuit
from core.circuit_search import find_circuit
from datetime import datetime


# currently, works for the AIG basis only; time limit is given in seconds
def improve_single_circuit(input_path: str, output_path: str, speed: str='fast', time_limit: int=60) -> Circuit:
    assert input_path.endswith('.bench')
    circuit = Circuit()
    circuit.load_from_file(file_name=input_path[:-6], extension='bench')
    circuit.normalize(basis='aig')

