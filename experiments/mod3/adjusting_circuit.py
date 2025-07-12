# checking what happens if one changes one of the top-xors of a circuit:
# will it still compute smth like mod3?

from core.circuit import Circuit
from itertools import combinations, product, permutations
from tqdm import tqdm

ckt = Circuit()
ckt.load_from_file('circuits/mod3_5_2_topxor.ckt')
