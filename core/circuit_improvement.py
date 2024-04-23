from copy import deepcopy
from core.circuit_search import find_circuit
from datetime import datetime
from functions.sum import *
from itertools import combinations
import networkx as nx
from tqdm import tqdm


def improve_circuit(circuit, max_inputs=6, subcircuit_size=7, forbidden_operations=None):
    print(f'  Enumerating subcircuits of size {subcircuit_size} with at most {max_inputs} inputs ({datetime.now()})')
    circuit_graph, circuit_truth_tables = circuit.construct_graph(), circuit.get_truth_tables()

    gate_subsets = set()

    def extend_gate_set(current_gate_set):
        gate_subsets.add(frozenset(current_gate_set))

        if len(current_gate_set) == subcircuit_size:
            return

        if len(current_gate_set) == subcircuit_size - 1:
            for gate in current_gate_set:
                for successor in circuit_graph.neighbors(gate):
                    if successor not in current_gate_set:
                        gate_subsets.add(frozenset(current_gate_set + [successor]))

        for gate in current_gate_set:
            assert gate not in circuit.input_labels
            for parent in (circuit.gates[gate][0], circuit.gates[gate][1]):
                if parent not in current_gate_set and parent not in circuit.input_labels:
                    extend_gate_set(current_gate_set + [parent])

    for gate in reversed(list(nx.topological_sort(circuit_graph))):
        if gate not in circuit.input_labels:
            extend_gate_set([gate, ])

    def compute_subcircuit_inputs_and_outputs(gate_subset):
        subcircuit_inputs, subcircuit_outputs = set(), set()
        for gate in gate_subset:
            for parent in circuit_graph.predecessors(gate):
                if parent not in gate_subset:
                    subcircuit_inputs.add(parent)

            if gate in circuit.outputs:
                subcircuit_outputs.add(gate)
            else:
                for successor in circuit_graph.successors(gate):
                    if successor not in gate_subset:
                        subcircuit_outputs.add(gate)
                        break

        return list(subcircuit_inputs), list(subcircuit_outputs)

    for gate_subset in tqdm(sorted(gate_subsets)):
        subcircuit_inputs, subcircuit_outputs = compute_subcircuit_inputs_and_outputs(gate_subset)
        if len(subcircuit_inputs) > max_inputs or len(subcircuit_outputs) == len(gate_subset):
            continue

        output_truth_tables = dict()
        for i, x in enumerate(product((0, 1), repeat=len(circuit.input_labels))):
            input = tuple(circuit_truth_tables[gate][i] for gate in subcircuit_inputs)
            output = tuple(circuit_truth_tables[gate][i] for gate in subcircuit_outputs)

            if input in output_truth_tables:
                assert output_truth_tables[input] == output
            else:
                output_truth_tables[input] = output

        final_truth_tables = [[] for _ in range(len(subcircuit_outputs))]
        for x in product((0, 1), repeat=len(subcircuit_inputs)):
            if tuple(x) in output_truth_tables:
                output = output_truth_tables[tuple(x)]
                assert len(output) == len(subcircuit_outputs)
                for i in range(len(output)):
                    final_truth_tables[i].append(output[i])
            else:
                for i in range(len(subcircuit_outputs)):
                    final_truth_tables[i].append('*')

        final_truth_tables = [''.join(map(str, table)) for table in final_truth_tables]

        def verify_better_circuit(original_circuit, smaller_circuit):
            assert smaller_circuit.get_nof_true_binary_gates() < original_circuit.get_nof_true_binary_gates()
            assert original_circuit.outputs == smaller_circuit.outputs

            original_circuit_truth_tables = original_circuit.get_truth_tables()
            smaller_circuit_truth_tables = smaller_circuit.get_truth_tables()
            for output_gate in smaller_circuit.outputs:
                assert original_circuit_truth_tables[output_gate] == smaller_circuit_truth_tables[output_gate]

        # corner case: there are two equal outputs
        for i, j in combinations(range(len(subcircuit_outputs)), 2):
            if final_truth_tables[i] == final_truth_tables[j]:
                first_gate, second_gate = subcircuit_outputs[i], subcircuit_outputs[j]
                better_circuit = deepcopy(circuit)
                better_circuit.merge_gates(first_gate, second_gate)

                verify_better_circuit(circuit, better_circuit)
                return better_circuit

        better_subcircuit = find_circuit(
            dimension=len(subcircuit_inputs),
            number_of_gates=len(gate_subset) - 1,
            output_truth_tables=final_truth_tables,
            input_labels=subcircuit_inputs,
            input_truth_tables=None,
            forbidden_operations=forbidden_operations
        )

        if better_subcircuit:
            if forbidden_operations:
                assert all(better_subcircuit.gates[gate][2] not in forbidden_operations for gate in better_subcircuit.gates)

            better_subcircuit.rename_internal_gates()
            better_subcircuit.rename_output_gates(subcircuit_outputs)

            assert better_subcircuit.input_labels == subcircuit_inputs, f'{better_subcircuit.input_labels}, {subcircuit_inputs}'
            assert better_subcircuit.outputs == subcircuit_outputs

            better_subcircuit_graph = better_subcircuit.construct_graph()

            better_circuit = deepcopy(circuit)
            for gate in gate_subset:
                better_circuit.gates.pop(gate)

            for gate in nx.topological_sort(better_subcircuit_graph):
                if gate in better_subcircuit.input_labels:
                    continue
                first_predecessor, second_predecessor, gate_type = better_subcircuit.gates[gate]
                assert first_predecessor in better_circuit.gates or first_predecessor in better_circuit.input_labels
                assert second_predecessor in better_circuit.gates or second_predecessor in better_circuit.input_labels
                better_circuit.add_gate(first_predecessor, second_predecessor, gate_type, gate)

            better_circuit_graph = better_circuit.construct_graph()
            if nx.is_directed_acyclic_graph(better_circuit_graph):
                verify_better_circuit(circuit, better_circuit)
                return better_circuit


def improve_circuit_iteratively(circuit, file_name='', forbidden_operations=None, max_inputs=5, max_subcircuit_size=6):
    was_improved = True
    while was_improved:
        was_improved = False

        for subcircuit_size in range(2, max_subcircuit_size + 1):
            better_circuit = improve_circuit(
                circuit,
                max_inputs=max_inputs,
                subcircuit_size=subcircuit_size,
                forbidden_operations=forbidden_operations
            )

            if better_circuit:
                assert better_circuit.get_nof_true_binary_gates() < circuit.get_nof_true_binary_gates()
                print(f'{file_name} improved to {better_circuit.get_nof_true_binary_gates()}')
                was_improved = True
                circuit = better_circuit
                circuit.save_to_file('y_' + file_name + '_size' + str(better_circuit.get_nof_true_binary_gates()), extension='bench')
                break

    return circuit
