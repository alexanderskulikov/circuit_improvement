from copy import deepcopy, copy
from core.circuit_search import find_circuit
from datetime import datetime
from functions.sum import *
from itertools import combinations
import networkx as nx
import time
from core.run_circuit import add_buff_inputs
from queue import Queue

hist_subcurcuits = set()
circuit_graph, circuit_truth_tables = None, None
stats_all, stats_optimal, stats_time_limit = 0, 0, 0

def improve_circuit(circuit, max_gates_for_inputs_numbers_dict, inputs_size=7, max_subcircuit_size=7, basis='xaig', time_limit=None, verify_new_circuit=False, global_time_limit=60):
    global circuit_graph, circuit_truth_tables, hist_subcurcuits
    global stats_optimal, stats_time_limit, stats_all
    print(f'    subcircuit size<={max_subcircuit_size}, inputs<={inputs_size}, '
          f'solver limit={time_limit}sec, time={datetime.now()}')
    start_time = datetime.now()

    def verify_better_circuit(original_circuit, smaller_circuit):
        assert smaller_circuit.get_nof_true_binary_gates() < original_circuit.get_nof_true_binary_gates()
        assert len(original_circuit.outputs) == len(smaller_circuit.outputs)

        original_circuit_truth_tables = original_circuit.get_truth_tables()
        smaller_circuit_truth_tables = smaller_circuit.get_truth_tables()

        for i in range(len(original_circuit.outputs)):
            assert original_circuit_truth_tables[original_circuit.outputs[i]] == smaller_circuit_truth_tables[
                smaller_circuit.outputs[i]]

    # corner case: there are two equal outputs
    for first_gate, second_gate in combinations(list(nx.topological_sort(circuit_graph)), 2):
        if first_gate not in circuit.input_labels and second_gate not in circuit.input_labels and circuit_truth_tables[first_gate] == circuit_truth_tables[second_gate]:
            better_circuit = deepcopy(circuit)
            better_circuit.merge_gates(first_gate, second_gate)
            if verify_new_circuit:
                verify_better_circuit(circuit, better_circuit)
            print(f'    Better circuit found with merged gates {first_gate} and {second_gate}')
            return better_circuit


    stats_all, stats_optimal, stats_time_limit = 0, 0, 0
    def print_stats():
        print(f'    cnt subcircuits={stats_all}, '
            f'time limit={stats_time_limit}, '
              f'optimal={stats_optimal}')

    topsort_array = list(nx.topological_sort(circuit_graph))
    number_of_vertex = len(topsort_array)
    inv_topsort_array = dict()
    for i in range(len(topsort_array)):
        inv_topsort_array[topsort_array[i]] = i

    def compute_subcircuit_outputs(gate_subset):
        subcircuit_outputs = set()
        for gate_ind in gate_subset:
            gate = topsort_array[gate_ind]
            if gate in circuit.input_labels:
                continue
            if gate in circuit.outputs:
                subcircuit_outputs.add(gate)
            else:
                for successor in circuit_graph.successors(gate):
                    if inv_topsort_array[successor] not in gate_subset:
                        subcircuit_outputs.add(gate)
                        break

        return list(subcircuit_outputs)


    def processing_of_one_subcircuit(gate_subset_inds, subcircuit_inputs_inds):
        gate_subset = []
        gate_subset_size = 0
        for ind in gate_subset_inds:
            gate_subset.append(topsort_array[ind])
            if topsort_array[ind] not in circuit.input_labels:
                gate_subset_size += 1

        if frozenset(gate_subset) in hist_subcurcuits:
            return False

        subcircuit_inputs = []
        for ind in subcircuit_inputs_inds:
            subcircuit_inputs.append(topsort_array[ind])

        for inp in subcircuit_inputs:
            if inp not in circuit.input_labels:
                for parent in circuit_graph.predecessors(inp):
                    if parent in gate_subset:
                        hist_subcurcuits.add(frozenset(gate_subset))
                        return False

        subcircuit_outputs = compute_subcircuit_outputs(gate_subset_inds)
        if len(subcircuit_outputs) == gate_subset_size:
            hist_subcurcuits.add(frozenset(gate_subset))
            del gate_subset, subcircuit_inputs, subcircuit_outputs
            return False

        output_truth_tables = [-1 for _ in range(1 << len(subcircuit_inputs))]
        for i, x in enumerate(product((0, 1), repeat=len(circuit.input_labels))):
            input, output = 0, 0
            for gate in subcircuit_inputs:
                input = (input << 1) + int(circuit_truth_tables[gate][i])
            for gate in subcircuit_outputs:
                output = (output << 1) + int(circuit_truth_tables[gate][i])

            if output_truth_tables[input] != -1:
                assert output_truth_tables[input] == output
            else:
                output_truth_tables[input] = output

        final_truth_tables = [['-' for __ in range(1 << len(subcircuit_inputs))] for _ in range(len(subcircuit_outputs))]
        for mask, x in enumerate(product((0, 1), repeat=len(subcircuit_inputs))):
            if output_truth_tables[mask] != -1:
                output = output_truth_tables[mask]
                for i in range(len(subcircuit_outputs) - 1, -1, -1):
                    final_truth_tables[i][mask] = str(output & 1)
                    output >>= 1
            else:
                for i in range(len(subcircuit_outputs)):
                    final_truth_tables[i][mask] = '*'

        final_truth_tables = [''.join(table) for table in final_truth_tables]

        # corner case: there are two equal outputs
        for i, j in combinations(range(len(subcircuit_outputs)), 2):
            if final_truth_tables[i] == final_truth_tables[j]:
                first_gate, second_gate = subcircuit_outputs[i], subcircuit_outputs[j]
                better_circuit = deepcopy(circuit)
                better_circuit.merge_gates(first_gate, second_gate)

                if verify_new_circuit:
                    verify_better_circuit(circuit, better_circuit)
                print(f'    Better subcircuit found with merged gates {subcircuit_outputs[i]} and {subcircuit_outputs[j]} in subcircuit with {len(subcircuit_inputs_inds)} inputs and {len(gate_subset)} gates')
                del gate_subset, subcircuit_inputs, subcircuit_outputs, output_truth_tables, final_truth_tables
                return better_circuit

        better_subcircuit = find_circuit(
            dimension=len(subcircuit_inputs),
            number_of_gates=gate_subset_size - 1,
            output_truth_tables=final_truth_tables,
            input_labels=list(subcircuit_inputs),
            input_truth_tables=None,
            basis=basis,
            time_limit=time_limit
        )
        del output_truth_tables

        if better_subcircuit is None:
            del gate_subset, subcircuit_inputs, subcircuit_outputs, final_truth_tables
            return None
        if better_subcircuit is False:
            hist_subcurcuits.add(frozenset(gate_subset))
            del gate_subset, subcircuit_inputs, subcircuit_outputs, final_truth_tables
            return False

        # the second check is a dirty hack
        if better_subcircuit and len(better_subcircuit.gates):
            better_subcircuit.rename_internal_gates()
            better_subcircuit.rename_output_gates(subcircuit_outputs)

            assert better_subcircuit.input_labels == subcircuit_inputs
            assert better_subcircuit.outputs == subcircuit_outputs

            better_subcircuit_graph = better_subcircuit.construct_graph()

            better_circuit = deepcopy(circuit)

            for gate in gate_subset:
                if gate not in better_circuit.input_labels:
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
                print(f'    Better subcircuit with {gate_subset_size} gates and {len(subcircuit_inputs)} inputs found for the following truth tables:', final_truth_tables)
                del gate_subset, subcircuit_inputs, subcircuit_outputs, final_truth_tables
                return better_circuit
        hist_subcurcuits.add(frozenset(gate_subset))
        del gate_subset, subcircuit_inputs, subcircuit_outputs, final_truth_tables
        return False

    def extend_gate_set(first_gate):
        global stats_time_limit, stats_optimal, stats_all

        def get_mask_by_subcircuit(subcircuit):
            mask = 0
            for gate_ind in subcircuit:
                mask |= (1 << gate_ind)
            return mask

        max_ind_v = inv_topsort_array[first_gate]
        all_masks_of_subcircuits = set()
        q = Queue()
        q.put(([inv_topsort_array[first_gate]], {inv_topsort_array[circuit.gates[first_gate][0]], inv_topsort_array[circuit.gates[first_gate][1]]}))
        all_masks_of_subcircuits.add(get_mask_by_subcircuit([inv_topsort_array[first_gate]]))
        while not q.empty():
            if (datetime.now() - start_time).total_seconds() > global_time_limit:
                print_stats()
                del all_masks_of_subcircuits, q
                return None

            current_gate_set, inputs = q.get()
            if len(inputs) > inputs_size or len(current_gate_set) > max_subcircuit_size or max_gates_for_inputs_numbers_dict[len(inputs)] < len(current_gate_set):
                continue

            stats_all += 1
            result = processing_of_one_subcircuit(current_gate_set, inputs)
            if result is None:
                stats_time_limit += 1
            elif result is False:
                stats_optimal += 1
            else:
                del all_masks_of_subcircuits, q
                return result

            if len(current_gate_set) == max_subcircuit_size or max_gates_for_inputs_numbers_dict[len(inputs)] == len(current_gate_set):
                continue

            set_of_nxt_gates = set()
            for gate_ind in current_gate_set:
                gate = topsort_array[gate_ind]
                if gate not in circuit.input_labels:
                    for parent in circuit_graph.predecessors(gate):
                        if inv_topsort_array[parent] not in current_gate_set and inv_topsort_array[parent] < max_ind_v:
                            set_of_nxt_gates.add(parent)
                for successor in circuit_graph.neighbors(gate):
                    if inv_topsort_array[successor] not in current_gate_set and inv_topsort_array[successor] < max_ind_v:
                        set_of_nxt_gates.add(successor)

            for nxt_gate in set_of_nxt_gates:
                new_mask = get_mask_by_subcircuit(current_gate_set + [inv_topsort_array[nxt_gate]])
                if new_mask in all_masks_of_subcircuits:
                    continue
                all_masks_of_subcircuits.add(new_mask)
                new_inputs = deepcopy(inputs)
                new_inputs.discard(inv_topsort_array[nxt_gate])
                if nxt_gate in circuit.input_labels:
                    new_inputs.add(inv_topsort_array[nxt_gate])
                else:
                    for parent in circuit_graph.predecessors(nxt_gate):
                        if inv_topsort_array[parent] not in current_gate_set and parent != nxt_gate:
                            new_inputs.add(inv_topsort_array[parent])
                q.put((current_gate_set + [inv_topsort_array[nxt_gate]], new_inputs))
        del all_masks_of_subcircuits
        return False

    def create_all_sub_circuits():
        global stats_all
        last_cnt_of_subcircuits = 0
        last_time = datetime.now()
        for gate in topsort_array:
            time_remaining = int(global_time_limit - (datetime.now() - start_time).total_seconds())
            if time_remaining < 0:
                print(f'...shutting down iterative improvement since {global_time_limit} seconds have passed')
                break

            if gate not in circuit.input_labels:
                res = extend_gate_set(gate)
                if res is None:
                    print(f'...shutting down iterative improvement since {global_time_limit} seconds have passed')
                    return None # GLOBAL TL
                if res is not False:
                    print_stats()
                    return res
                # print("processed all with", gate, inv_topsort_array[gate], "/", number_of_vertex,
                #       "   subcircuits processed -", stats_all,
                #       "with this gate -", (stats_all - last_cnt_of_subcircuits),
                #       "avg_speed -", (stats_all - last_cnt_of_subcircuits) / max(1.0, (datetime.now() - last_time).total_seconds()))
                last_time = datetime.now()
                last_cnt_of_subcircuits = stats_all
        print_stats()
        return None

    return create_all_sub_circuits()


def improve_circuit_iteratively(circuit, file_name='', basis='xaig', save_circuits=True, speed='easy', global_time_limit=60):
    print(f'Iterative improvement of {file_name}, size={circuit.get_nof_true_binary_gates()}, number_of_inputs={len(circuit.input_labels)}, basis={basis}, speed={speed}, time={datetime.now()}')

    assert basis in ('xaig', 'aig')
    assert speed in ('easy', 'medium', 'hard')

    start_time = datetime.now()

    global hist_subcurcuits, circuit_graph, circuit_truth_tables

    hist_subcurcuits = set()

    predefined_params = {
        'easy' : ({0: 7, 1 : 7, 2 : 7, 3 : 7, 4 : 6, 5 : 6, 6 : 6}, 6, 7, 30),
        'medium' : ({0 : 9, 1 : 9, 2 : 9, 3 : 8, 4 : 8, 5 : 7, 6 : 7, 7 : 7}, 7, 9, 30),
        'hard' : ({0: 10, 1 : 10, 2 : 10, 3 : 10, 4 : 9, 5 : 8, 6 : 8, 7 : 8, 8 : 8}, 8, 10, 30)
    }

    dict_inps_to_number_of_gates, max_inputs, max_subcircuit_size, time_limit = predefined_params[speed]
    was_improved = True
    while was_improved:
        time_remaining = int(global_time_limit - (datetime.now() - start_time).total_seconds())
        if time_remaining < 0:
            print(f'...shutting down iterative improvement since {global_time_limit} seconds have passed')
            break

        was_improved = False
        circuit_graph, circuit_truth_tables = circuit.construct_graph(), circuit.get_truth_tables()

        better_circuit = improve_circuit(
            circuit,
            max_gates_for_inputs_numbers_dict=dict_inps_to_number_of_gates,
            inputs_size=max_inputs,
            max_subcircuit_size=max_subcircuit_size,
            basis=basis,
            time_limit=time_limit,
            global_time_limit=time_remaining
        )

        if better_circuit:
            # assert better_circuit.get_nof_true_binary_gates() < circuit.get_nof_true_binary_gates()
            better_circuit.normalize(basis=basis)
            print(f'    \033[92m{file_name} improved to {better_circuit.get_nof_true_binary_gates()}!\033[0m')
            was_improved = True
            circuit = better_circuit

            if save_circuits:
                circuit.save_to_file(f'circuits/_{file_name}-{basis}-size{str(better_circuit.get_nof_true_binary_gates())}.bench')


    print(f'  Done! time={datetime.now()}, start time={start_time}, processing time={datetime.now() - start_time}')
    return circuit

def improve_single_circuit(input_path: str, output_path: str, speed: str = 'easy', global_time_limit: int = 60):
    assert input_path.endswith('.bench') and output_path.endswith('.bench')
    circuit = Circuit()
    circuit.load_from_file(path=input_path)
    circuit = improve_circuit_iteratively(circuit=circuit, basis='aig', file_name=input_path, save_circuits=False, speed=speed, global_time_limit=global_time_limit)
    circuit.save_to_file(path=output_path)