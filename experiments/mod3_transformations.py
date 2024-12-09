from core.circuit import Circuit
from core.circuit_improvement import improve_circuit, improve_circuit_iteratively
from itertools import product


def check_mod3_circuit(circuit, modd):
    tt = circuit.get_truth_tables()
    n = len(circuit.input_labels)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = tt[circuit.outputs[0]][i]
        value = sum(x[j] for j in range(n))
        assert (value % 3 == modd) == s


ckt = Circuit()
ckt.load_from_file('mod3_4_2_transformed')
print(ckt.get_nof_true_binary_gates())
ckt.draw(file_name='mod3_4_2_transformed', detailed_labels=True)
check_mod3_circuit(ckt, modd=1)
ckt.normalize(basis='xaig')
print(ckt.get_nof_true_binary_gates())
ckt.draw(file_name='mod3_4_2_transformed_simplified', detailed_labels=True)
check_mod3_circuit(ckt, modd=1)

ckt2 = improve_circuit_iteratively(ckt, speed=12)
print(ckt2.get_nof_true_binary_gates())
ckt2.draw(file_name='mod3_4_2_transformed_improved', detailed_labels=True)
