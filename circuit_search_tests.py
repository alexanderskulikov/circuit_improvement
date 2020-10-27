from itertools import product
from circuit import Circuit
from circuit_search import find_circuit, CircuitFinder
import unittest


def verify_sum_circuit(circuit):
    truth_tables = circuit.get_truth_tables()
    n = len(circuit.input_labels)

    for x in product(range(2), repeat=n):
        i = sum((2 ** (n - 1 - j)) * x[j] for j in range(n))
        s = sum(truth_tables[circuit.outputs[d]][i] * (2 ** d) for d in range(len(circuit.outputs)))
        if s != sum(x):
            return False

    return True


class TestCircuitSearch(unittest.TestCase):
    def check_exact_circuit_size(self, n, size, truth_tables):
        circuit = find_circuit(n, None, None, size, truth_tables)
        self.assertIsInstance(circuit, Circuit)
        circuit_truth_tables = circuit.get_truth_tables()
        self.assertTrue(all(truth_tables[i] == ''.join(map(str, circuit_truth_tables[circuit.outputs[i]]))
                            for i in range(len(truth_tables))))
        self.assertEqual(find_circuit(n, None, None, size - 1, truth_tables), False)

    def test_small_xors(self):
        for n in range(2, 7):
            tt = [''.join(str(sum(x) % 2) for x in product(range(2), repeat=n))]
            self.check_exact_circuit_size(n, n - 1, tt)

    def test_small_xors_with_fixed_gates(self):
        for n in range(2, 7):
            tt = [''.join(str(sum(x) % 2) for x in product(range(2), repeat=n))]

            circuit_finder = CircuitFinder(n, None, None, n - 1, tt)
            circuit_finder.fix_gate(n, 0, 1, '0110')
            c = circuit_finder.solve_cnf_formula(verbose=0)
            self.assertIsInstance(c, Circuit)

            circuit_finder = CircuitFinder(n, None, None, n - 1, tt)
            circuit_finder.fix_gate(n, 0, 1, '0001')
            c = circuit_finder.solve_cnf_formula(verbose=0)
            self.assertEqual(c, False)

            circuit_finder = CircuitFinder(n, None, None, n - 1, tt)
            for i in range(n - 2):
                circuit_finder.forbid_wire(i, n)
            c = circuit_finder.solve_cnf_formula(verbose=0)
            self.assertIsInstance(c, Circuit)

    def test_and_ors(self):
        for n in range(2, 5):
            tt = [
                ''.join(('1' if all(x[i] == 1 for i in range(n)) else '0') for x in product(range(2), repeat=n)),
                ''.join(('1' if any(x[i] == 1 for i in range(n)) else '0') for x in product(range(2), repeat=n))
            ]
            self.check_exact_circuit_size(n, 2 * n - 2, tt)

    def test_all_equal(self):
        for n in range(2, 5):
            tt = [''.join('1' if all(x[i] == x[i + 1] for i in range(n - 1)) else '0' for x in product(range(2), repeat=n))]
            self.check_exact_circuit_size(n, 2 * n - 3, tt)

    def test_sum_circuits(self):
        for n, l, size in ((2, 2, 2), (3, 2, 5), (4, 3, 9)):
            tt = [''.join(str((sum(x) >> i) & 1) for x in product(range(2), repeat=n))
                  for i in range(l)]
            circuit = find_circuit(n, None, None, size, tt)
            self.assertIsInstance(circuit, Circuit)
            self.assertTrue(verify_sum_circuit(circuit))

    def test_sum5_local_improvement(self):
        tt = [[] for _ in range(18)]
        for x1, x2, x3, x4, x5 in product(range(2), repeat=5):
            x6 = x1 ^ x2
            x7 = x2 ^ x3
            x8 = x6 | x7
            x9 = x3 ^ x6
            x10 = x8 ^ x9
            x11 = x4 ^ x9
            x12 = x4 ^ x5
            x13 = x11 | x12
            x14 = x5 ^ x11
            x15 = x13 ^ x14
            x16 = x10 ^ x15
            x17 = x10 * x15

            tt[5].append(x5)
            tt[8].append(x8)
            tt[9].append(x9)
            tt[11].append(x11)
            tt[12].append(x12)
            tt[14].append(x14)
            tt[16].append(x16)
            tt[17].append(x17)

        for i in range(18):
            tt[i] = ''.join(map(str, tt[i]))

        circuit = find_circuit(5, ['g5', 'g8', 'g9', 'g11', 'g12'], [tt[5], tt[8], tt[9], tt[11], tt[12]], 6, [tt[14], tt[16], tt[17]])
        self.assertIsInstance(circuit, Circuit)

        circuit = find_circuit(5, ['g5', 'g8', 'g9', 'g11', 'g12'], [tt[5], tt[8], tt[9], tt[11], tt[12]], 5, [tt[14], tt[16], tt[17]])
        self.assertIsInstance(circuit, Circuit)

    def test_sum_with_precomputed_xor(self):
        for n, l, size in ((2, 2, 2), (3, 2, 5), (4, 3, 9)):
            tt = [''.join(str((sum(x) >> i) & 1) for x in product(range(2), repeat=n))
                  for i in range(l)]

            circuit_finder = CircuitFinder(n, None, None, size, tt)
            circuit_finder.fix_gate(n, 0, 1, '0110')
            for k in range(n - 2):
                circuit_finder.fix_gate(n + k + 1, k + 2, n + k, '0110')
            circuit = circuit_finder.solve_cnf_formula(verbose=0)
            self.assertIsInstance(circuit, Circuit)
            self.assertTrue(verify_sum_circuit(circuit))


if __name__ == '__main__':
    unittest.main()
