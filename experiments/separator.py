from core.circuit import Circuit
from networkx import dag_longest_path_length
from itertools import combinations

ckt = Circuit()
ckt.load_from_file('circuits/ex277_depth40_size94.bench')
ckt.normalize(basis='aig')
# ckt.draw('ex277_highlighted.png', highlight_gates=['new_n82', ])

graph = ckt.construct_graph()
min_depth = dag_longest_path_length(graph)

for gate_set in combinations(graph.nodes(), 5):
    tmp_graph = ckt.construct_graph()
    tmp_graph.remove_nodes_from(gate_set)
    min_depth = min(min_depth, dag_longest_path_length(tmp_graph))
    print(gate_set, min_depth)

print(min_depth)

