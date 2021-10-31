from itertools import product
from math import log2


class BooleanFunction:
    def __init__(self, truth_table) -> None:
        if isinstance(truth_table, list) or isinstance(truth_table, tuple):
            truth_table = ''.join(map(str, truth_table))
        assert isinstance(truth_table, str) and all(c in ('0', '1') for c in truth_table)
        assert log2(len(truth_table)).is_integer()

        self.truth_table = truth_table
        self.number_of_variables = int(log2(len(truth_table)))

    def get_value(self, assignment: str) -> int:
        assert isinstance(assignment, str) and all(c in ('0', '1') for c in assignment)
        assert len(assignment) == self.number_of_variables

        index = sum(int(assignment[i]) * (2 ** (self.number_of_variables - i - 1)) for i in range(self.number_of_variables))
        return int(self.truth_table[index])

    def get_subfunction(self, variable: int, substitution: 'BooleanFunction') -> 'BooleanFunction':
        assert variable in range(self.number_of_variables)
        assert substitution.number_of_variables == self.number_of_variables - 1

        resulting_truth_table = []
        for a in product(range(2), repeat=self.number_of_variables - 1):
            assignment = ''.join(map(str, a))
            assignment = assignment[:variable] + str(substitution.get_value(assignment)) + assignment[variable:]
            resulting_truth_table.append(self.get_value(assignment))

        return BooleanFunction(''.join(map(str, resulting_truth_table)))

    def is_constant(self) -> bool:
        return any(self.truth_table == str(b) * (2 ** self.number_of_variables) for b in range(2))

    def is_specific_literal(self, variable: int, free_constant: int) -> bool:
        assert variable in range(self.number_of_variables)
        assert free_constant in range(2)

        for a in product(range(2), repeat=self.number_of_variables):
            assignment = ''.join(map(str, a))
            if self.get_value(assignment) != ((a[variable] + free_constant) % 2):
                return False

        return True

    def is_any_literal(self) -> bool:
        return any(self.is_specific_literal(i, c) for i, c in product(range(self.number_of_variables), range(2)))
