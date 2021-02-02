from itertools import product

enc = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 2}

# in_2
for x1, x2 in product(range(2), repeat=2):
    g1 = x1 ^ x2
    g2 = x1 & x2
    assert (x1 + x2) % 3 == enc[g2, g1]

# in_3
for x1, x2, x3 in product(range(2), repeat=3):
    g1 = x1 == x2
    g2 = 1 - (x1 | x2)
    g3 = g2 == x3
    g4 = g1 == g3
    g5 = g2 < g4
    assert (x1 + x2 + x3) % 3 == enc[g5, g3]

# in_4
for x1, x2, x3, x4 in product(range(2), repeat=4):
    g1 = x1 == x2
    g2 = g1 ^ x3
    g3 = g2 ^ x2
    g4 = g1 & g3
    g5 = g4 == x4
    g6 = g2 == g5
    g7 = g4 < g6
    assert (x1 + x2 + x3 + x4) % 3 == enc[g7, g5]

# mid_3
for x1, x2, x3, z0, z1 in product(range(2), repeat=5):
    g1 = x1 == z1
    g2 = g1 | z0
    g3 = g2 ^ x2
    g4 = g3 ^ z0
    g5 = g4 ^ x1
    g6 = g2 & g5
    g7 = g6 == x3
    g8 = g3 == g7
    g9 = g6 < g8
    assert (enc[z0, z1] + x1 + x2 + x3) % 3 == enc[g9, g7]

# out_1^1
for x1, z0, z1 in product(range(2), repeat=3):
    g1 = x1 ^ z1
    g2 = z0 < g1
    assert ((enc[z0, z1] + x1) % 3 == 1) == g2

# out_2^0
for x1, x2, z0, z1 in product(range(2), repeat=4):
    g1 = z0 == x2
    g2 = x1 ^ z1
    g3 = g1 == x1
    g4 = z0 < g2
    g5 = 1 - (g3 | g4)
    assert ((enc[z0, z1] + x1 + x2) % 3 == 0) == g5

# out_3^2
for x1, x2, x3, z0, z1 in product(range(2), repeat=5):
    g1 = x1 == z1
    g2 = g1 | z0
    g3 = g2 ^ x2
    g4 = g3 ^ z0
    g5 = g4 ^ x1
    g6 = g2 & g5
    g7 = g3 == x3
    g8 = 1 - (g6 | g7)
    assert ((enc[z0, z1] + x1 + x2 + x3) % 3 == 2) == g8

# mod3_3^0
for x1, x2, x3 in product(range(2), repeat=3):
    g1 = x2 == x3
    g2 = x1 ^ x2
    g3 = g1 > g2
    assert ((x1 + x2 + x3) % 3 == 0) == g3

# mod3_3^2
for x1, x2, x3 in product(range(2), repeat=3):
    g1 = x2 ^ x3
    g2 = x3 | g1
    g3 = x1 < g2
    g4 = g1 ^ g3
    assert ((x1 + x2 + x3) % 3 == 2) == g4

# mod3_4^2
for x1, x2, x3, x4 in product(range(2), repeat=4):
    g1 = x1 ^ x2
    g2 = x3 ^ x4
    g3 = x1 ^ x3
    g4 = g2 | g3
    g5 = g1 < g4
    g6 = g2 ^ g5
    assert ((x1 + x2 + x3 + x4) % 3 == 2) == g6
