from networkx.algorithms.approximation import treewidth_min_degree, treewidth_min_fill_in
from core.circuit import *
from os import listdir

folder = 'circuits'
for file_name in sorted(listdir(folder)):
    if file_name.startswith('.'):
        continue
    circuit = Circuit()
    circuit.load_from_file(path=folder + '/' + file_name)
    circuit.normalize(basis='aig')
    directed_graph = circuit.construct_graph()
    undirected_graph = directed_graph.to_undirected()

    for x in circuit.input_labels:
        undirected_graph.remove_node(x)

    tw = min(treewidth_min_degree(undirected_graph)[0], treewidth_min_fill_in(undirected_graph)[0])
    print(f'The treewidth of {file_name} is at most {tw}')

