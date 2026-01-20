from itertools import product


def mod3_5_2_first(x1, x2, x3, x4, x5):
    g5 = x1 ^ x2
    g6 = x3 ^ g5
    g7 = x4 ^ x5
    g8 = g6 ^ g7
    g9 = x3 ^ x4
    g10 = g7 | g9
    g11 = x1 * x2
    g12 = g10 ^ g11
    g13 = g8 * g10
    g14 = g12 * (1 - g13)
    return g14


def mod3_5_2_second(x1, x2, x3, x4, x5):
    g5 = x1 | x2
    g6 = x3 ^ g5
    g7 = x4 ^ x5
    g8 = g6 ^ g7
    g9 = x3 ^ x4
    g10 = g7 | g9
    g11 = x1 * x2
    g12 = g10 ^ g11
    g13 = g8 * g10
    g14 = g12 * (1 - g13)
    return g14


for x in product((0, 1), repeat=5):
    if sum(x) % 3 == 2:
        assert mod3_5_2_first(*x) == 1 and mod3_5_2_second(*x) == 1
    else:
        assert mod3_5_2_first(*x) == 0 and mod3_5_2_second(*x) == 0
        