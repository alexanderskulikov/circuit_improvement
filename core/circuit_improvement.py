from copy import deepcopy
from core.circuit_search import find_circuit
from datetime import datetime
from functions.sum import *
from itertools import combinations
import networkx as nx
from tqdm import tqdm


def improve_circuit(circuit, max_inputs=7, subcircuit_size=7, basis='xaig', time_limit=None, verify_new_circuit=False):
    print(f'    subcircuit size={subcircuit_size}, inputs<={max_inputs}, '
          f'solver limit={time_limit}sec, time={datetime.now()}')
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

    stats_too_many_inputs, stats_trivially_optimal, stats_optimal, stats_time_limit = 0, 0, 0, 0

    def print_stats():
        print(f'      stats: subcircuits={len(gate_subsets)}; '
              f'out of them: too many inputs={stats_too_many_inputs}, '
              f'trivially optimal={stats_trivially_optimal}, '
              f'time limit={stats_time_limit}, '
              f'optimal={stats_optimal}')

    # main loop
    for gate_subset in tqdm(sorted(gate_subsets), leave=False):
        subcircuit_inputs, subcircuit_outputs = compute_subcircuit_inputs_and_outputs(gate_subset)

        if len(subcircuit_inputs) > max_inputs:
            stats_too_many_inputs += 1
            continue
        if len(subcircuit_outputs) == len(gate_subset):
            stats_trivially_optimal += 1
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
            assert len(original_circuit.outputs) == len(smaller_circuit.outputs)

            original_circuit_truth_tables = original_circuit.get_truth_tables()
            smaller_circuit_truth_tables = smaller_circuit.get_truth_tables()

            for i in range(len(original_circuit.outputs)):
                assert original_circuit_truth_tables[original_circuit.outputs[i]] == smaller_circuit_truth_tables[smaller_circuit.outputs[i]]

        # corner case: there are two equal outputs
        for i, j in combinations(range(len(subcircuit_outputs)), 2):
            if final_truth_tables[i] == final_truth_tables[j]:
                first_gate, second_gate = subcircuit_outputs[i], subcircuit_outputs[j]
                better_circuit = deepcopy(circuit)
                better_circuit.merge_gates(first_gate, second_gate)

                if verify_new_circuit:
                    verify_better_circuit(circuit, better_circuit)
                return better_circuit

        better_subcircuit = find_circuit(
            dimension=len(subcircuit_inputs),
            number_of_gates=len(gate_subset) - 1,
            output_truth_tables=final_truth_tables,
            input_labels=subcircuit_inputs,
            input_truth_tables=None,
            basis=basis,
            time_limit=time_limit
        )

        if better_subcircuit is None:
            stats_time_limit += 1
        if better_subcircuit is False:
            stats_optimal += 1

        # the second check is a dirty hack
        if better_subcircuit and len(better_subcircuit.gates):
            better_subcircuit.rename_internal_gates()
            better_subcircuit.rename_output_gates(subcircuit_outputs)

            assert better_subcircuit.input_labels == subcircuit_inputs
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
                if verify_new_circuit:
                    verify_better_circuit(circuit, better_circuit)
                print_stats()
                print('    Better subcircuit found for the following truth tables:', final_truth_tables)
                circuit.draw(f'{datetime.now()}-size{circuit.get_nof_true_binary_gates()}', highlight_gates=gate_subset)
                better_circuit.draw(f'{datetime.now()}-size{better_circuit.get_nof_true_binary_gates()}', highlight_gates=better_subcircuit.gates)
                return better_circuit

    print_stats()
    return None


def improve_circuit_iteratively(circuit, file_name='', basis='xaig', save_circuits=True, speed=10):
    print(f'Iterative improvement of {file_name}, size={circuit.get_nof_true_binary_gates()}, basis={basis}, speed={speed}, time={datetime.now()}')

    assert basis in ('xaig', 'aig')

    predefined_parameters = {
        18: (3, 3, 3, 1),
        17: (5, 3, 3, 1),
        16: (5, 4, 4, 1),
        15: (6, 3, 5, 1),   # previous name: fast
        14: (6, 5, 5, 3),
        13: (7, 5, 5, 3),
        12: (7, 6, 6, 3),
        11: (12, 6, 6, 10),
        10: (7, 3, 7, 5),   # previous name: medium
        9: (7, 7, 7, 10),
        8: (7, 3, 7, 20),
        7: (8, 8, 8, 10),
        6: (16, 8, 8, 20),
        5: (8, 9, 9, 10),   # previous name: slow
        4: (8, 9, 9, 20),
        3: (10, 10, 15, 10),
        2: (20, 3, 15, 20),
        1: (20, 3, 20, 20),
    }
    max_inputs, min_subcircuit_size, max_subcircuit_size, time_limit = predefined_parameters[speed]

    was_improved = True
    while was_improved:
        was_improved = False

        for subcircuit_size in range(min_subcircuit_size, max_subcircuit_size + 1):
            better_circuit = improve_circuit(
                circuit,
                max_inputs=max_inputs,
                subcircuit_size=subcircuit_size,
                basis=basis,
                time_limit=time_limit
            )

            if better_circuit:
                assert better_circuit.get_nof_true_binary_gates() < circuit.get_nof_true_binary_gates()
                better_circuit.normalize(basis=basis)
                print(f'    \033[92m{file_name} improved to {better_circuit.get_nof_true_binary_gates()}!\033[0m')
                was_improved = True

                circuit = better_circuit

                if save_circuits:
                    circuit.save_to_file(f'_{file_name}-{basis}-size{str(better_circuit.get_nof_true_binary_gates())}', extension='bench')

                break

    print(f'  Done! time={datetime.now()}')
    return circuit
