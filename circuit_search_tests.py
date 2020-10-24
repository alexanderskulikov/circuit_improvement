from itertools import product
from circuit import Circuit
from circuit_search import find_circuit
import unittest


class TestCircuitSearch(unittest.TestCase):
    def check_exact_circuit_size(self, n, size, truth_tables):
        self.assertIsInstance(find_circuit(n, None, None, size, truth_tables), Circuit)
        self.assertEqual(find_circuit(n, None, None, size - 1, truth_tables), False)

    def test_small_xors(self):
        for n in range(2, 7):
            tt = [''.join(str(sum(x) % 2) for x in product(range(2), repeat=n))]
            self.check_exact_circuit_size(n, n - 1, tt)

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
        # full adder
        tt = [
            ''.join(str(sum(x) & 1) for x in product(range(2), repeat=3)),
            ''.join(str((sum(x) >> 1) & 1) for x in product(range(2), repeat=3))
        ]
        self.check_exact_circuit_size(3, 5, tt)

        # SUM_4
        self.assertIsInstance(
            find_circuit(4, None, None, 9, [
                ''.join(str(sum(x) & 1) for x in product(range(2), repeat=4)),
                ''.join(str((sum(x) >> 1) & 1) for x in product(range(2), repeat=4)),
                ''.join(str((sum(x) >> 2) & 1) for x in product(range(2), repeat=4))
            ]),
            Circuit
        )
        # # this already takes too long
        # self.assertEqual(
        #     find_circuit(4, None, None, 8, [
        #         ''.join(str(sum(x) & 1) for x in product(range(2), repeat=4)),
        #         ''.join(str((sum(x) >> 1) & 1) for x in product(range(2), repeat=4)),
        #         ''.join(str((sum(x) >> 2) & 1) for x in product(range(2), repeat=4))
        #     ]),
        #     Circuit
        # )

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

        self.assertIsInstance(
            find_circuit(5, ['g5', 'g8', 'g9', 'g11', 'g12'], [tt[5], tt[8], tt[9], tt[11], tt[12]], 6,
                         [tt[14], tt[16], tt[17]]), Circuit)
        self.assertIsInstance(
            find_circuit(5, ['g5', 'g8', 'g9', 'g11', 'g12'], [tt[5], tt[8], tt[9], tt[11], tt[12]], 5,
                         [tt[14], tt[16], tt[17]]), Circuit)


if __name__ == '__main__':
    unittest.main()
