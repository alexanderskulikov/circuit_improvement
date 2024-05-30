import itertools
import random
import unittest
from typing import Optional, List

from core.circuit import Circuit
from core.circuit_search import CircuitFinder
from core.zhegalkin_polynomial import ZhegalkinTree


def get_circuit_size(circuit: Circuit) -> int:
    circuit.normalize('xaig')
    size = len(list(filter(lambda x: x[-1] not in ('1100', '1010'), circuit.gates.values())))
    return size


random.seed(0)


def generate_circuit(dimension: int, number_of_gates: int, number_of_outputs: int, tl: int) -> Optional[Circuit]:
    truth_tables = [
        ''.join(random.choice('01') for _ in range(2 ** dimension))
        for i in range(number_of_outputs)
    ]
    finder = CircuitFinder(
        dimension=dimension,
        number_of_gates=number_of_gates,
        output_truth_tables=truth_tables,
    )
    ckt = finder.solve_cnf_formula(time_limit=tl)
    if not ckt:
        return None
    return ckt


def gen_zhegalkin_trees(circuit: Circuit) -> List[ZhegalkinTree]:
    polynomials = circuit.get_zhegalkin_polynomials()
    out_polynomials = [polynomials[i] for i in circuit.outputs]
    circuit_tt = circuit.get_truth_tables()
    zhegalkin_trees = [ZhegalkinTree.simplest_optimized_polynomial(p) for p in out_polynomials]
    return zhegalkin_trees


def get_out_truth_tables(circuit: Circuit) -> List[List[int]]:
    circuit_tt = circuit.get_truth_tables()
    out_tt = [circuit_tt[i] for i in circuit.outputs]
    return out_tt


class ZhegalkinTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.circuits = []
        self.generate_circuits(range(1, 5), range(1, 8), range(1, 4), 1)

    def generate_circuits(self, dim_range, gates_range, outputs_range, tl):
        self.circuits = []
        for dim, gates, outputs in itertools.product(dim_range, gates_range, outputs_range):
            print(f"Generating circuit: {dim} {gates} {outputs}")
            circuit = generate_circuit(dim, gates, outputs, tl)
            if circuit is None:
                print("Circuit not found => Skip")
                continue
            self.circuits.append(circuit)

    def compare_circuits(self, ckt1: Circuit, ckt2: Circuit):
        all_tt_1 = ckt1.get_truth_tables()
        all_tt_2 = ckt2.get_truth_tables()
        tt_1 = [all_tt_1[i] for i in ckt1.outputs]
        tt_2 = [all_tt_2[i] for i in ckt2.outputs]
        self.assertEqual(len(tt_1), len(tt_2))
        for i in range(len(tt_1)):
            self.assertEqual(tt_1[i], tt_2[i], f"{i}:\n\t{tt_1[i]}\n\t{tt_2[i]}")

    def run_test_on_many_circuits(self, test):
        for circuit in self.circuits:
            test(self, circuit)

    def check_zhegalkin_polynomial(self, circuit: Circuit):
        truth_tables = circuit.get_truth_tables()
        poly = circuit.get_zhegalkin_polynomials()
        for key, tt_ckt in truth_tables.items():
            tt_poly = poly[key].truth_table()
            self.assertEqual(tt_poly, tt_ckt, f"{key}:\n\t{tt_poly}\n\t{tt_ckt}")

    def test_zhegalkin_polynomials(self):
        self.run_test_on_many_circuits(ZhegalkinTests.check_zhegalkin_polynomial)

    def check_circuit_from_zhegalkin_polynomial(self, circuit: Circuit):
        polynomials = circuit.get_zhegalkin_polynomials()
        out_polynomials = [polynomials[i] for i in circuit.outputs]
        new_circuit = Circuit(circuit.input_labels)
        new_circuit.add_zhegalkin_polynomials(out_polynomials, add_outputs=True)
        self.compare_circuits(circuit, new_circuit)

    def test_circuits_from_zhegalkin_polynomials(self):
        self.run_test_on_many_circuits(ZhegalkinTests.check_circuit_from_zhegalkin_polynomial)

    def check_simple_zhegalkin_tree(self, circuit):
        out_tt = get_out_truth_tables(circuit)
        zhegalkin_trees = gen_zhegalkin_trees(circuit)
        tree_tt = [t.truth_table() for t in zhegalkin_trees]
        ''
        self.assertEqual(len(out_tt), len(tree_tt))
        for i in range(len(out_tt)):
            self.assertEqual(tree_tt[i], out_tt[i])

    def test_simple_zhegalkin_trees(self):
        self.run_test_on_many_circuits(ZhegalkinTests.check_simple_zhegalkin_tree)

    def check_circuit_from_zhegalkin_tree(self, circuit):
        zhegalkin_trees = gen_zhegalkin_trees(circuit)

        new_circuit = Circuit(circuit.input_labels)
        new_circuit.add_zhegalkin_trees(zhegalkin_trees, add_outputs=True)

        self.compare_circuits(circuit, new_circuit)

    def test_circuits_from_zhegalkin_trees(self):
        self.run_test_on_many_circuits(ZhegalkinTests.check_circuit_from_zhegalkin_tree)


if __name__ == '__main__':
    unittest.main()
