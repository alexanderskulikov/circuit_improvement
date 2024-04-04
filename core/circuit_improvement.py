from core.circuit_search import find_circuit
from core.circuit import Circuit
from datetime import datetime
from itertools import combinations, product
import networkx as nx
import random
from string import ascii_lowercase
from timeit import default_timer as timer
from tqdm import tqdm


def correct_subcircuit_count(circuit, subcircuit_size=7, connected=True):
    circuit_graph, count = circuit.construct_graph(), 0

    for graph in (circuit_graph.subgraph(selected_nodes) for selected_nodes in
                  combinations(circuit.gates, subcircuit_size)):
        if (not connected) or (connected and nx.is_weakly_connected(graph)):
            count += 1
    return count


def make_output_truth_tables(circuit, subcircuit_inputs, subcircuit_outputs):
    sub_input_truth_table = {}
    sub_output_truth_table = {}
    truth_tables = circuit.get_truth_tables()

    for i in range(1 << len(circuit.input_labels)):
        str_in = [''.join(map(str, [truth_tables[g][i] for g in subcircuit_inputs]))][0]
        sub_input_truth_table[str_in] = i
        if len(sub_input_truth_table) == 1 << len(subcircuit_inputs):
            break
    sub_input_truth_table = {value: key for key, value in sub_input_truth_table.items()}
    sub_input_truth_table2 = {value: key for key, value in sub_input_truth_table.items()}

    for i in sub_input_truth_table:
        str_out = [''.join(map(str, [truth_tables[g][i] for g in subcircuit_outputs]))][0]
        sub_output_truth_table[i] = str_out

    sub_output_truth_table2 = [''] * len(subcircuit_outputs)
    for bits in product([0, 1], repeat=len(subcircuit_inputs)):
        row = "".join(str(bit) for bit in bits)
        if row not in sub_input_truth_table2:
            for j in range(len(subcircuit_outputs)):
                sub_output_truth_table2[j] += '*'
        else:
            for j in range(len(subcircuit_outputs)):
                sub_output_truth_table2[j] += sub_output_truth_table[sub_input_truth_table2[row]][j]

    return sub_output_truth_table2


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


def convert_keys_to_strings(dictionary):
    new_dict = {}
    for key, value in dictionary.items():
        if isinstance(key, int):
            new_key = str(key)
        else:
            new_key = key
        new_dict[new_key] = value
    return new_dict


def fix_internal_gates_names(circuit):
    random.seed(datetime.now().timestamp())
    prefix = ''.join(random.choice(ascii_lowercase) for _ in range(5))
    new_gates = dict()

    def new_name(old_name):
        return old_name if not str(old_name).isnumeric() else prefix + str(old_name)

    for gate in circuit.gates:
        first, second, gate_type = circuit.gates[gate]
        new_gates[new_name(gate)] = new_name(first), new_name(second), gate_type

    circuit.gates = new_gates

    new_outputs = [new_name(g) for g in circuit.outputs]
    circuit.outputs = new_outputs


def improve_circuit(circuit, subcircuit_size=5, connected=True):
    # print('Trying to improve a circuit of size', circuit.get_nof_true_binary_gates(), flush=True)
    circuit_graph = circuit.construct_graph()
    total, current, current_percent, time = correct_subcircuit_count(circuit, subcircuit_size, connected=connected), 0, 0, 0
    print(f'Enumerating subcircuits of size {subcircuit_size} (total={total})...', flush=True, end='')

    for graph in (circuit_graph.subgraph(selected_nodes) for selected_nodes in
                  combinations(circuit.gates, subcircuit_size)):
        if connected and not nx.is_weakly_connected(graph):
            continue
        subcircuit = tuple(graph.nodes)
        # start = timer()
        subcircuit_inputs, subcircuit_outputs = get_inputs_and_outputs(circuit, circuit_graph, subcircuit)
        if len(subcircuit_outputs) == subcircuit_size:
            continue

        current += 1
        # print(f'\n{subcircuit_size}: {current}/{total} ({100 * current // total}%) ', end='', flush=True)
        if current / total > current_percent / 100:
            print('.', end='')
            current_percent += 1

        random.shuffle(subcircuit_inputs)
        output_truth_tables = make_output_truth_tables(circuit, subcircuit_inputs, subcircuit_outputs)
        improved_circuit = find_circuit(dimension=len(subcircuit_inputs),
                                        number_of_gates=subcircuit_size - 1,
                                        output_truth_tables=output_truth_tables,
                                        input_labels=subcircuit_inputs,
                                        input_truth_tables=None,
                                        forbidden_operations=[])

        if isinstance(improved_circuit, Circuit):
            replaced_graph = circuit.replace_subgraph(improved_circuit, subcircuit, subcircuit_outputs)
            if nx.is_directed_acyclic_graph(replaced_graph):
                print('\nCircuit Improved!\n', end='', flush=True)
                improved_full_circuit = Circuit(input_labels=circuit.input_labels,
                                                outputs=make_improved_circuit_outputs(circuit.outputs,
                                                                                      subcircuit_outputs,
                                                                                      improved_circuit.outputs),
                                                graph=replaced_graph)

                # improved_full_circuit.gates = convert_keys_to_strings(improved_full_circuit.gates)
                fix_internal_gates_names(improved_full_circuit)
                return improved_full_circuit

        # stop = timer()
        # time += stop - start
        # remaining = time / current * (total - current)
        # print(f' | curr: {int(stop - start)} sec | rem: {int(remaining)} sec ({round(remaining / 60, 1)} min)', end='',
        #       flush=True)
    print()


def improve_circuit_iteratively(circuit, max_subcircuit_size=5, save_intermediate_circuits=True):
    was_improved = True
    while was_improved:
        was_improved = False

        for subcircuit_size in range(2, max_subcircuit_size + 1):
            better_circuit = improve_circuit(circuit, subcircuit_size=subcircuit_size)
            if isinstance(better_circuit, Circuit):
                was_improved = True
                if save_intermediate_circuits:
                    better_circuit.save_to_file(f'improved{better_circuit.get_nof_true_binary_gates()}', extension='ckt')
                circuit = better_circuit
                break

    return circuit
