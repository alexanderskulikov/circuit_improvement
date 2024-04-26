from core.circuit_improvement import *
from functions.mult import *
from core.circuit_search import *

ckt = Circuit()
ckt.load_from_file('ex43', extension='bench')
ckt.draw('before')
ckt.normalize(basis='xaig')
ckt.draw('after')