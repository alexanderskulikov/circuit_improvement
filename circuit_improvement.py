from circuit_search_for_improvement import find_circuit
from circuit import Circuit
from itertools import combinations
import networkx as nx
from timeit import default_timer as timer
import random


def correct_subcircuit_count(circuit, subcircuit_size=7, connected=True):
    circuit_graph, count = circuit.construct_graph(), 0

    for graph in (circuit_graph.subgraph(selected_nodes) for selected_nodes in
                  combinations(circuit.gates, subcircuit_size)):
        if (not connected) or (connected and nx.is_weakly_connected(graph)):
            count += 1
    return count


def make_truth_tables(circuit, subcircuit_inputs, subcircuit_outputs):
    sub_input_truth_table = {}
    sub_output_truth_table = {}
    truth_tables = circuit.get_truth_tables()

    for i in range(1 << len(circuit.input_labels)):
        str_in = [''.join(map(str, [truth_tables[g][i] for g in subcircuit_inputs]))][0]
        sub_input_truth_table[str_in] = i
        if len(sub_input_truth_table) == 1 << len(subcircuit_inputs):
            break
    sub_input_truth_table = {value: key for key, value in sub_input_truth_table.items()}

    for i in sub_input_truth_table:
        str_out = [''.join(map(str, [truth_tables[g][i] for g in subcircuit_outputs]))][0]
        sub_output_truth_table[i] = str_out
    return sub_input_truth_table, sub_output_truth_table


def make_improved_circuit_outputs(cir_out, sub_out, imp_out):
    result = list(cir_out)
    imp_out = list(imp_out)
    for index in range(0, len(result)):
        if result[index] in sub_out:
            result[index] = imp_out[sub_out.index(result[index])]
    return result


def get_inputs_and_outputs(circuit, circuit_graph, subcircuit):
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
    return subcircuit_inputs, subcircuit_outputs


def improve_circuit(circuit, subcircuit_size=5, connected=True):
    print('Trying to improve a circuit of size', len(circuit.gates), flush=True)
    circuit_graph = circuit.construct_graph()
    total, current, time = correct_subcircuit_count(circuit, subcircuit_size, connected=connected), 0, 0
    print(f'\nEnumerating subcircuits of size {subcircuit_size} (total={total})...')
    for graph in (circuit_graph.subgraph(selected_nodes) for selected_nodes in
                  combinations(circuit.gates, subcircuit_size)):
        if connected and not nx.is_weakly_connected(graph):
            continue
        subcircuit = tuple(graph.nodes)
        start = timer()
        subcircuit_inputs, subcircuit_outputs = get_inputs_and_outputs(circuit, circuit_graph, subcircuit)
        if len(subcircuit_outputs) == subcircuit_size:
            continue
        current += 1
        print(f'\n{subcircuit_size}: {current}/{total} ({100 * current // total}%) ', end='', flush=True)

        random.shuffle(subcircuit_inputs)
        sub_in_tt, sub_out_tt = make_truth_tables(circuit, subcircuit_inputs, subcircuit_outputs)
        improved_circuit = find_circuit(subcircuit_inputs, subcircuit_size - 1, sub_in_tt, sub_out_tt)

        if isinstance(improved_circuit, Circuit):
            replaced_graph = circuit.replace_subgraph(improved_circuit, subcircuit, subcircuit_outputs)
            if nx.is_directed_acyclic_graph(replaced_graph):
                print('\nCircuit Improved!\n', end='', flush=True)
                improved_full_circuit = Circuit.make_circuit(replaced_graph, circuit.input_labels,
                                                             make_improved_circuit_outputs(circuit.outputs,
                                                                                           subcircuit_outputs,
                                                                                           improved_circuit.outputs))
                return improved_full_circuit

        stop = timer()
        time += stop - start
        remaining = time / current * (total - current)
        print(f' | curr: {int(stop - start)} sec | rem: {int(remaining)} sec ({round(remaining / 60, 1)} min)', end='',
              flush=True)
