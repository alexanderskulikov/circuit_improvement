from functions import BooleanFunction
from itertools import product
import unittest


class TestBooleanFunction(unittest.TestCase):
    def test_conjunction(self):
        for n in range(2, 6):
            f = BooleanFunction('0' * (2 ** n - 1) + '1')
            for a in product(range(2), repeat=n):
                assignment = ''.join(map(str, a))
                self.assertEqual(all(b == 1 for b in a), f.get_value(assignment) == 1)

    def test_parity(self):
        for n in range(2, 6):
            f = BooleanFunction(''.join(map(str, [sum(a) % 2 for a in product(range(2), repeat=n)])))
            for a in product(range(2), repeat=n):
                assignment = ''.join(map(str, a))
                self.assertEqual(sum(a) % 2 == 1, f.get_value(assignment) == 1)

    def test_conjunction_constant_substitution(self):
        for n in range(2, 6):
            f = BooleanFunction('0' * (2 ** n - 1) + '1')

            zero_substitution = BooleanFunction('0' * (2 ** (n - 1)))
            one_substitution = BooleanFunction('1' * (2 ** (n - 1)))

            for i in range(n):
                g = f.get_subfunction(i, zero_substitution)
                self.assertEqual(g.truth_table, '0' * (2 ** (n - 1)))

                h = f.get_subfunction(i, one_substitution)
                self.assertEqual(h.truth_table, '0' * (2 ** (n - 1) - 1) + '1')

    def test_literal(self):
        for n in range(2, 6):
            for i, c in product(range(n), range(2)):
                truth_table = [(a[i] + c) % 2 for a in product(range(2), repeat=n)]
                f = BooleanFunction(truth_table)
                self.assertTrue(f.is_any_literal())
                self.assertTrue(f.is_specific_literal(i, c))

                for j, b in product(range(n), range(2)):
                    if i != j or b != c:
                        self.assertFalse(f.is_specific_literal(j, b))


if __name__ == '__main__':
    unittest.main()
