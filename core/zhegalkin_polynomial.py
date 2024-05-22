from __future__ import annotations

import copy
import itertools
from typing import Union, Iterable, Optional, List, Dict, Callable

Monom = Union[int, Iterable[int]]
InputType = Union[int, Iterable]


class ZhegalkinPolynomial:
    def __init__(self, input_labels: List[str], monomials: Optional[Iterable[Monom]] = None):
        self._input_labels = input_labels
        if monomials is None:
            self._monomials = set()
        else:
            self._monomials = set([self._monom_to_int(m) for m in monomials])

    merge_ops: Dict[str, Callable[[ZhegalkinPolynomial, ZhegalkinPolynomial], ZhegalkinPolynomial]] = {
        "0000": lambda x, y: ZhegalkinPolynomial(x._input_labels, []),
        "1111": lambda x, y: ZhegalkinPolynomial(x._input_labels, [0]),
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

    @classmethod
    def merge_polynomials(cls, x: ZhegalkinPolynomial, y: ZhegalkinPolynomial, op: str) -> ZhegalkinPolynomial:
        assert len(x._input_labels) == len(y._input_labels)
        assert len(op) == 4
        assert op in cls.merge_ops, f"Unsupported operation {op}"
        f = cls.merge_ops[op]
        return f(x, y)

    def __call__(self, x: InputType) -> bool:
        x = self._input_to_int(x)
        res = False
        for m in self._monomials:
            res ^= ((m & x) == m)
        return res

    def truth_table(self) -> List[int]:
        res = []
        for inp in itertools.product(range(2), repeat=len(self._input_labels)):
            inp = inp[::-1]
            res.append(int(self(inp)))
        return res

    def monom_to_str(self, monom: int) -> str:
        if monom == 0:
            return 'ONE' if '1' in map(str, self._input_labels) else '1'
        labels = []
        for i, label in enumerate(self._input_labels):
            if (monom >> i) & 1:
                labels.append(label)
        return ' * '.join(map(str, labels))

    def __str__(self) -> str:
        strings = [self.monom_to_str(m) for m in sorted(self._monomials)]
        return ' + '.join(strings)

    def __repr__(self):
        return self.__str__()

    def _input_to_int(self, inp: InputType) -> int:
        if isinstance(inp, int):
            return inp
        else:
            assert isinstance(inp, Iterable)
            mask = 0
            for i, v in enumerate(inp):
                assert i < len(self._input_labels), "Too many inputs"
                if v:
                    mask |= 1 << (len(self._input_labels) - i - 1)
            return mask

    def _monom_to_int(self, monom: Monom) -> int:
        if isinstance(monom, int):
            return monom
        else:
            assert isinstance(monom, Iterable)
            val = 0
            for v in monom:
                assert isinstance(v, int)
                assert 0 <= v < len(self._input_labels), "Monom value is out of range"
                val |= 1 << v
            return val

    def _ixor_with_monom(self, monom: Monom):
        monom = self._monom_to_int(monom)
        if monom in self._monomials:
            self._monomials.remove(monom)
        else:
            self._monomials.add(monom)

    def _imul_with_monom(self, monom: Monom):
        monom = self._monom_to_int(monom)
        new_monomials = set()
        for m in self._monomials:
            m |= monom
            if m in new_monomials:
                new_monomials.remove(m)
            else:
                new_monomials.add(m)
        self._monomials = new_monomials

    def __ixor__(self, other: Optional[ZhegalkinPolynomial, Monom]):
        if isinstance(other, int) or isinstance(other, Iterable):
            self._ixor_with_monom(other)
        else:
            assert isinstance(other, ZhegalkinPolynomial)
            for monom in other._monomials:
                self._ixor_with_monom(monom)
        return self

    def __iand__(self, other: Optional[ZhegalkinPolynomial, Monom]):
        if isinstance(other, int) or isinstance(other, Iterable):
            self._imul_with_monom(other)
        else:
            assert isinstance(other, ZhegalkinPolynomial)
            res = ZhegalkinPolynomial(self._input_labels)
            for monom in other._monomials:
                tmp = self & monom
                res ^= tmp
            self._monomials = res._monomials
        return self

    def inplace_not(self):
        self._ixor_with_monom(0)

    def __xor__(self, other: Optional[ZhegalkinPolynomial, Monom]) -> ZhegalkinPolynomial:
        res = copy.deepcopy(self)
        res ^= other
        return res

    def __and__(self, other: Optional[ZhegalkinPolynomial, Monom]) -> ZhegalkinPolynomial:
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
