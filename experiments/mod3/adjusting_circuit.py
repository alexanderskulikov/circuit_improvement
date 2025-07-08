# checking what happens if one changes one of the top-xors of a circuit:
# will it still compute smth like mod3?

from core.circuit import Circuit
from itertools import combinations, product, permutations

ckt = Circuit()
ckt.load_from_file('circuits/adjusted.ckt')
# ckt.draw('adjusted.png')
tt = ckt.get_truth_tables()['s10']
print(tt)

for c0, c1, c2, c3, c01, c02, c03, c12, c13, c23, r in product(range(3), repeat=11):
    dd = [
        1 if ((c0 * x[0] + c1 * x[1] + c2 * x[2] + c3 * x[3] +
                       c01 * x[0] * x[1] +
                       c02 * x[0] * x[2] +
                       c03 * x[0] * x[3] +
                       c12 * x[1] * x[2] +
                       c13 * x[1] * x[3] +
                       c23 * x[2] * x[3]) % 3 == r) else 0
        for x in product(range(2), repeat=4)
    ]
    if dd == tt:
        print(c0, c1, c2, c3, c01, c02, c03, c12, c13, c23, r)
