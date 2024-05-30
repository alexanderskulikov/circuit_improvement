from __future__ import annotations

import copy
import itertools
import pickle
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Union, Iterable, Optional, List, Dict, Callable, Any

Monom = Union[int, Iterable[int]]
InputType = Union[int, Iterable]


class ZhegalkinPolynomial:
    def __init__(self, input_labels: List[str], monomials: Optional[Iterable[Monom]] = None):
        self.input_labels = input_labels
        if monomials is None:
            self.monomials = set()
        else:
            self.monomials = set([self._monom_to_int(m) for m in monomials])

    merge_ops: Dict[str, Callable[[ZhegalkinPolynomial, ZhegalkinPolynomial], ZhegalkinPolynomial]] = {
        "0000": lambda x, y: ZhegalkinPolynomial(x.input_labels, []),
        "1111": lambda x, y: ZhegalkinPolynomial(x.input_labels, [0]),
        "0011": lambda x, y: x,
        "1100": lambda x, y: ~x,
        "0101": lambda x, y: y,
        "1010": lambda x, y: ~y,
        "0110": lambda x, y: x ^ y,
        "1001": lambda x, y: x == y,
        "0001": lambda x, y: x & y,
        "1110": lambda x, y: ~(x & y),
        '0111': lambda x, y: x | y,
        '1000': lambda x, y: (~x & ~y),
        '0010': lambda x, y: x > y,
        '0100': lambda x, y: x < y,
        '1011': lambda x, y: x >= y,
        '1101': lambda x, y: x <= y,
    }

    def save_pickle(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_pickle(cls, filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

    @classmethod
    def merge_polynomials(cls, x: ZhegalkinPolynomial, y: ZhegalkinPolynomial, op: str) -> ZhegalkinPolynomial:
        assert len(x.input_labels) == len(y.input_labels)
        assert len(op) == 4
        assert op in cls.merge_ops, f"Unsupported operation {op}"
        f = cls.merge_ops[op]
        return f(x, y)

    def __call__(self, x: InputType) -> bool:
        x = self._input_to_int(x)
        res = False
        for m in self.monomials:
            res ^= ((m & x) == m)
        return res

    def truth_table(self) -> List[int]:
        res = []
        for inp in itertools.product(range(2), repeat=len(self.input_labels)):
            inp = inp[::-1]
            res.append(int(self(inp)))
        return res

    def monom_to_str(self, monom: int) -> str:
        if monom == 0:
            return 'ONE' if '1' in map(str, self.input_labels) else '1'
        labels = []
        for i, label in enumerate(self.input_labels):
            if (monom >> i) & 1:
                labels.append(label)
        return ' * '.join(map(str, labels))

    def __str__(self) -> str:
        strings = [self.monom_to_str(m) for m in sorted(self.monomials)]
        return ' + '.join(strings)

    def __repr__(self):
        return self.__str__()

    def is_linear(self) -> bool:
        return all(m.bit_count() <= 1 for m in self.monomials)

    def common_inputs(self) -> List:
        common_components = 2 ** len(self.input_labels) - 1
        for m in self.monomials:
            if m == 0:
                continue
            common_components &= m
        if common_components == 0:
            return list()
        result = []
        for i, label in enumerate(self.input_labels):
            if (common_components >> i) & 1:
                result.append(label)
        return result

    def is_monom(self) -> bool:
        return len(self.monomials) <= 1 + int(0 in self.monomials)

    def is_common_inputs_and_linear(self) -> bool:
        common_inputs = self.common_inputs()
        if len(common_inputs) == 0:
            return False
        return all(m.bit_count() <= 1 + len(common_inputs) for m in self.monomials)

    def _input_to_int(self, inp: InputType) -> int:
        if isinstance(inp, int):
            return inp
        else:
            assert isinstance(inp, Iterable)
            mask = 0
            for i, v in enumerate(inp):
                assert i < len(self.input_labels), "Too many inputs"
                if v:
                    mask |= 1 << (len(self.input_labels) - i - 1)
            return mask

    def _monom_to_int(self, monom: Monom) -> int:
        if isinstance(monom, int):
            return monom
        else:
            assert isinstance(monom, Iterable)
            val = 0
            for v in monom:
                assert isinstance(v, int)
                assert 0 <= v < len(self.input_labels), "Monom value is out of range"
                val |= 1 << v
            return val

    def _ixor_with_monom(self, monom: Monom):
        monom = self._monom_to_int(monom)
        if monom in self.monomials:
            self.monomials.remove(monom)
        else:
            self.monomials.add(monom)

    def _imul_with_monom(self, monom: Monom):
        monom = self._monom_to_int(monom)
        new_monomials = set()
        for m in self.monomials:
            m |= monom
            if m in new_monomials:
                new_monomials.remove(m)
            else:
                new_monomials.add(m)
        self.monomials = new_monomials

    def __ixor__(self, other: Union[ZhegalkinPolynomial, Monom]):
        if isinstance(other, int) or isinstance(other, Iterable):
            self._ixor_with_monom(other)
        else:
            assert isinstance(other, ZhegalkinPolynomial)
            for monom in other.monomials:
                self._ixor_with_monom(monom)
        return self

    def __iand__(self, other: Union[ZhegalkinPolynomial, Monom]):
        if isinstance(other, int) or isinstance(other, Iterable):
            self._imul_with_monom(other)
        else:
            assert isinstance(other, ZhegalkinPolynomial)
            res = ZhegalkinPolynomial(self.input_labels)
            for monom in other.monomials:
                tmp = self & monom
                res ^= tmp
            self.monomials = res.monomials
        return self

    def inplace_not(self):
        self._ixor_with_monom(0)

    def __xor__(self, other: Union[ZhegalkinPolynomial, Monom]) -> ZhegalkinPolynomial:
        res = copy.deepcopy(self)
        res ^= other
        return res

    def __and__(self, other: Union[ZhegalkinPolynomial, Monom]) -> ZhegalkinPolynomial:
        res = copy.deepcopy(self)
        res &= other
        return res

    def __invert__(self) -> ZhegalkinPolynomial:
        res = copy.deepcopy(self)
        res.inplace_not()
        return res

    def __or__(self, other: ZhegalkinPolynomial) -> ZhegalkinPolynomial:
        return ~(~self & ~other)

    def __le__(self, other: ZhegalkinPolynomial) -> ZhegalkinPolynomial:
        return ~(self & ~other)

    def __ge__(self, other: ZhegalkinPolynomial) -> ZhegalkinPolynomial:
        return ~(~self & other)

    def __lt__(self, other: ZhegalkinPolynomial) -> ZhegalkinPolynomial:
        return ~self & other

    def __gt__(self, other: ZhegalkinPolynomial) -> ZhegalkinPolynomial:
        return self & ~other

    def __eq__(self, other: ZhegalkinPolynomial) -> ZhegalkinPolynomial:
        return ~(self ^ other)


class ZhegalkinTree:
    @dataclass
    class Node:
        left: Union[ZhegalkinTree, ZhegalkinTree.Node, ZhegalkinPolynomial]
        right: Union[ZhegalkinTree, ZhegalkinTree.Node, ZhegalkinPolynomial]
        op: str

        def truth_table(self) -> List[int]:
            left_tt = self.left.truth_table()
            right_tt = self.right.truth_table()
            assert len(left_tt) == len(right_tt)
            return list(int(self.op[i * 2 + j]) for i, j in zip(left_tt, right_tt))

    def __init__(self, root: Union[ZhegalkinPolynomial, ZhegalkinTree.Node]):
        self.root: Union[ZhegalkinPolynomial, ZhegalkinTree.Node] = root

    def truth_table(self) -> List[int]:
        if isinstance(self.root, ZhegalkinPolynomial):
            return self.root.truth_table()
        else:
            assert isinstance(self.root, ZhegalkinTree.Node)
            return self.root.truth_table()

    @staticmethod
    def collect_inputs_stat(polynomial: ZhegalkinPolynomial) -> Dict[Any, int]:
        stat = defaultdict(int)
        for monom in polynomial.monomials:
            inputs = [i for i in range(len(polynomial.input_labels)) if monom >> i & 1]
            for inp in inputs:
                stat[inp] += 1
        return stat

    @staticmethod
    def split_polynom_by_most_common_input(polynomial: ZhegalkinPolynomial) -> ZhegalkinTree.Node:
        stat = ZhegalkinTree.collect_inputs_stat(polynomial)
        split_input = max(stat, key=lambda x: stat[x])
        polynomial_with_inp = ZhegalkinPolynomial(polynomial.input_labels,
                                                  [m for m in polynomial.monomials if m >> split_input & 1])
        assert polynomial_with_inp
        polynomial_other = ZhegalkinPolynomial(polynomial.input_labels,
                                               [m for m in polynomial.monomials if m != 0 and not m >> split_input & 1])
        left_op = '1110' if 0 in polynomial.monomials else '0001'
        left = ZhegalkinTree.Node(left=ZhegalkinPolynomial(polynomial.input_labels, [[split_input]]),
                                  right=polynomial_with_inp, op=left_op)
        if not polynomial_other:
            return left
        else:
            return ZhegalkinTree.Node(left=left, right=polynomial_other, op="0110")

    @staticmethod
    def extract_common_inputs(polynomial: ZhegalkinPolynomial) -> ZhegalkinTree.Node:
        common_components = 2 ** len(polynomial.input_labels) - 1
        for m in polynomial.monomials:
            if m == 0:
                continue
            common_components &= m
        assert common_components != 0
        left = ZhegalkinPolynomial(polynomial.input_labels, [common_components])
        right_monomials = []
        for m in polynomial.monomials:
            if m == 0:
                continue
            assert m & common_components == common_components
            right_monomials.append(m ^ common_components)
        right = ZhegalkinPolynomial(polynomial.input_labels, right_monomials)
        op = '1110' if 0 in polynomial.monomials else '0001'
        return ZhegalkinTree.Node(left=left, right=right, op=op)

    @classmethod
    def simplest_optimized_polynomial(cls, polynomial: ZhegalkinPolynomial) -> ZhegalkinTree:
        if polynomial.is_monom() or polynomial.is_linear() or not polynomial.common_inputs():
            return ZhegalkinTree(root=polynomial)
        result = cls.extract_common_inputs(polynomial)
        result.left = cls.simplest_optimized_polynomial(result.left)
        result.right = cls.simplest_optimized_polynomial(result.right)
        return ZhegalkinTree(root=result)
