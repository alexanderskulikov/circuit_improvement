from circuit import Circuit
from circuit_search import find_circuit
from itertools import combinations
import networkx as nx
from scipy.special import comb


def improve_circuit(circuit):
    print('Trying to improve a circuit of size', len(circuit.gates), flush=True)
    truth_tables = circuit.get_truth_tables()
    circuit_graph = circuit.construct_graph()

    for subcircuit_size in range(3, 4):
        total, current, solver = comb(len(circuit.gates), subcircuit_size, exact=True), 0, 0
        print(f'\nEnumerating subcircuits of size {subcircuit_size} (total={total})...')
        for subcircuit in combinations(circuit.gates, subcircuit_size):
            current += 1
            print(f'{subcircuit_size}: {solver}/{current}/{total} ({100 * current // total}%)', flush=True)

            subcircuit_inputs, subcircuit_outputs = set(), set()

            for gate in subcircuit:
                for p in circuit_graph.predecessors(gate):
                    if p not in subcircuit:
                        subcircuit_inputs.add(p)

                if gate in circuit.outputs:
                    subcircuit_outputs.add(gate)
                else:
                    for s in circuit_graph.successors(gate):
                        if s not in subcircuit:
                            subcircuit_outputs.add(gate)
                            break

            subcircuit_inputs = list(subcircuit_inputs)
            subcircuit_outputs = list(subcircuit_outputs)

            subcircuit_graph = circuit_graph.subgraph(subcircuit)
            if not nx.algorithms.components.is_weakly_connected(subcircuit_graph):
                print('disconnected')
                continue

            if len(subcircuit_outputs) != subcircuit_size:
                solver += 1
                # assert find_circuit(
                #     dimension=len(circuit.input_labels),
                #     input_labels=subcircuit_inputs,
                #     input_truth_tables=[''.join(map(str, truth_tables[g])) for g in subcircuit_inputs],
                #     number_of_gates=subcircuit_size,
                #     output_truth_tables=[''.join(map(str, truth_tables[g])) for g in subcircuit_outputs]
                # )

                improved_circuit = find_circuit(
                    dimension=len(circuit.input_labels),
                    input_labels=subcircuit_inputs,
                    input_truth_tables=[''.join(map(str, truth_tables[g])) for g in subcircuit_inputs],
                    number_of_gates=subcircuit_size - 1,
                    output_truth_tables=[''.join(map(str, truth_tables[g])) for g in subcircuit_outputs]
                )
                if isinstance(improved_circuit, Circuit):
                    print('x', end='', flush=True)
                    circuit_graph_copy = circuit.construct_graph()
                    improved_circuit_graph = improved_circuit.construct_graph()

                    for gate in subcircuit:
                        if gate not in subcircuit_inputs:
                            circuit_graph_copy.remove_node(gate)
                    for gate in improved_circuit.gates:
                        assert gate not in subcircuit_inputs
                        circuit_graph_copy.add_node(gate)
                        for p in improved_circuit_graph.predecessors(gate):
                            circuit_graph_copy.add_edge(p, gate)

                    for i in range(len(subcircuit_outputs)):
                        for s in circuit_graph.successors(subcircuit_outputs[i]):
                            circuit_graph_copy.add_edge(improved_circuit.outputs[i], s)

                    if nx.is_directed_acyclic_graph(circuit_graph_copy):
                        print('Found improved circuit!')
                        print('Inputs and outputs:', subcircuit_inputs, subcircuit_outputs)
                        a = nx.nx_agraph.to_agraph(circuit_graph_copy)
                        a.layout(prog='dot')
                        a.draw('circuit_improved.png')
                        print(improved_circuit)
                        exit()


