import cProfile
import sys
from copy import deepcopy, copy
from core.circuit_search import find_circuit
from datetime import datetime
from functions.sum import *
from itertools import combinations
import networkx as nx
from tqdm import tqdm
# import winsound
import time


hist_subcurcuits = set()
circuit_graph, circuit_truth_tables = None, None


def improve_circuit(circuit, max_gates_for_inputs_numbers_dict, inputs_size=7, max_subcircuit_size=7, basis='xaig', time_limit=None, verify_new_circuit=False, global_time_limit=60):
    global circuit_graph, circuit_truth_tables, hist_subcurcuits
    print(f'    subcircuit size<={max_subcircuit_size}, inputs<={inputs_size}, '
          f'solver limit={time_limit}sec, time={datetime.now()}, global time limit={global_time_limit}sec')
    start_time = datetime.now()
    gate_subsets = set()
    # topsort_array = list(nx.topological_sort(circuit_graph))[::-1]
    topsort_array = list(nx.topological_sort(circuit_graph))
    inv_topsort_array = dict()
    for i in range(len(topsort_array)):
        inv_topsort_array[topsort_array[i]] = i

    def extend_gate_set(current_gate_set, max_ind_v, inputs):
        if (frozenset(current_gate_set), frozenset(inputs)) in gate_subsets or len(inputs) > inputs_size or len(current_gate_set) > max_subcircuit_size or max_gates_for_inputs_numbers_dict[len(inputs)] < len(current_gate_set):
            return
        gate_subsets.add((frozenset(current_gate_set), frozenset(inputs)))

        if len(current_gate_set) == max_subcircuit_size or max_gates_for_inputs_numbers_dict[len(inputs)] == len(current_gate_set):
            return

        set_of_nxt_gates = set()
        for gate_ind in current_gate_set:
            gate = topsort_array[gate_ind]
            for parent in (circuit.gates[gate][0], circuit.gates[gate][1]):
                if inv_topsort_array[parent] not in current_gate_set and parent not in circuit.input_labels and inv_topsort_array[parent] < max_ind_v:
                    set_of_nxt_gates.add(parent)
            for successor in circuit_graph.neighbors(gate):
                if inv_topsort_array[successor] not in current_gate_set and inv_topsort_array[successor] < max_ind_v:
                    set_of_nxt_gates.add(successor)

        for nxt_gate in set_of_nxt_gates:
            new_inputs = deepcopy(inputs)
            new_inputs.discard(inv_topsort_array[nxt_gate])
            for parent in circuit_graph.predecessors(nxt_gate):
                if inv_topsort_array[parent] not in current_gate_set and parent != nxt_gate:
                    new_inputs.add(inv_topsort_array[parent])
            extend_gate_set(current_gate_set + [inv_topsort_array[nxt_gate]], max_ind_v, new_inputs)

    def create_all_sub_circuits():
        for gate in topsort_array:
            if gate not in circuit.input_labels:
                extend_gate_set([inv_topsort_array[gate], ], inv_topsort_array[gate], {inv_topsort_array[circuit.gates[gate][0]], inv_topsort_array[circuit.gates[gate][1]]})

    # print("START SEARCHING SUBCIRCUITS")
    # start = time.time()
    create_all_sub_circuits()
    # print("STOP SEARCHING SUBCIRCUITS", time.time() - start)
    # print("CNT", len(gate_subsets))

    # def compute_subcircuit_inputs_and_outputs(gate_subset):
    #     subcircuit_inputs, subcircuit_outputs = set(), set()
    #     for gate in gate_subset:
    #         for parent in circuit_graph.predecessors(gate):
    #             if parent not in gate_subset:
    #                 subcircuit_inputs.add(parent)
    #
    #         if gate in circuit.outputs:
    #             subcircuit_outputs.add(gate)
    #         else:
    #             for successor in circuit_graph.successors(gate):
    #                 if successor not in gate_subset:
    #                     subcircuit_outputs.add(gate)
    #                     break
    #
    #     return list(subcircuit_inputs), list(subcircuit_outputs)

    def compute_subcircuit_outputs(gate_subset):
        subcircuit_outputs = set()
        for gate_ind in gate_subset:
            gate = topsort_array[gate_ind]
            if gate in circuit.outputs:
                subcircuit_outputs.add(gate)
            else:
                for successor in circuit_graph.successors(gate):
                    if inv_topsort_array[successor] not in gate_subset:
                        subcircuit_outputs.add(gate)
                        break

        return list(subcircuit_outputs)

    stats_trivially_optimal, stats_optimal, stats_time_limit = 0, 0, 0

    def print_stats():
        print(f'      stats: subcircuits={len(gate_subsets)}; '
              f'trivially optimal={stats_trivially_optimal}, '
              f'time limit={stats_time_limit}, '
              f'optimal={stats_optimal}')

    lst = (-1, -1)
    cnt_passed = 0
    last_time = 0
    arr_of_all_subsets = sorted(list(gate_subsets), key=lambda x: (len(x[1]), len(x[0])))
    for gate_subset_inds, subcircuit_inputs_inds in tqdm(arr_of_all_subsets, leave=False, smoothing=0.03):
        # if len(subcircuit_inputs_inds) <= 5:
        #     continue
        #
        # if (len(subcircuit_inputs_inds), len(gate_subset_inds)) != lst:
        #     if lst != (-1, -1):
        #         print("PASSED", lst, (time.time() - last_time), cnt_passed, "  ", cnt_passed / (time.time() - last_time))
        #     lst = (len(subcircuit_inputs_inds), len(gate_subset_inds))
        #     print("NEW", lst)
        #     cnt_passed = 0
        #     last_time = time.time()
        # else:
        #     cnt_passed += 1
        if (datetime.now() - start_time).total_seconds() > global_time_limit:
            print_stats()
            return None

        gate_subset = []
        for ind in gate_subset_inds:
            gate_subset.append(topsort_array[ind])
        subcircuit_inputs = []
        for ind in subcircuit_inputs_inds:
            subcircuit_inputs.append(topsort_array[ind])


        if frozenset(gate_subset) in hist_subcurcuits:
            stats_trivially_optimal += 1
            continue
        # subcircuit_inputs, subcircuit_outputs = compute_subcircuit_inputs_and_outputs(gate_subset)
        subcircuit_outputs = compute_subcircuit_outputs(gate_subset_inds)
        if len(subcircuit_outputs) == len(gate_subset):
            stats_trivially_optimal += 1
            continue

        # print("YEEE", gate_subset, subcircuit_inputs, subcircuit_outputs)

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

        # res = False
        # for win_in_gates in range(min(len(gate_subset) - len(final_truth_tables), 3), 0, -1):
        # for win_in_gates in range(1, 2):
        better_subcircuit = find_circuit(
            dimension=len(subcircuit_inputs),
            number_of_gates=len(gate_subset) - 1,
            output_truth_tables=final_truth_tables,
            input_labels=list(subcircuit_inputs),
            input_truth_tables=None,
            basis=basis,
            time_limit=time_limit
        )

        if better_subcircuit is None:
            # winsound.Beep(10000, 1000)
            stats_time_limit += 1
            hist_subcurcuits.add(frozenset(gate_subset))
            print("TL", len(gate_subset), len(subcircuit_inputs), len(subcircuit_outputs))
            continue
        if better_subcircuit is False:
            stats_optimal += 1
            hist_subcurcuits.add(frozenset(gate_subset))
            continue

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
                print(f'    Better subcircuit with {len(gate_subset)} gates and {len(subcircuit_inputs)} inputs found for the following truth tables:', final_truth_tables)
                # circuit.draw(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}-size{circuit.get_nof_true_binary_gates()}_init', highlight_gates=gate_subset)
                # better_circuit.draw(f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}-size{better_circuit.get_nof_true_binary_gates()}_new', highlight_gates=better_subcircuit.gates)
                return better_circuit

    print_stats()
    return None


def improve_circuit_iteratively(circuit, file_name='', basis='xaig', save_circuits=True, speed='easy', global_time_limit=60):
    print(f'Iterative improvement of {file_name}, size={circuit.get_nof_true_binary_gates()}, nof inputs={len(circuit.input_labels)}, basis={basis}, speed={speed}, time={datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, global time limit={global_time_limit} seconds')

    assert basis in ('xaig', 'aig')
    assert speed in ('easy', 'medium', 'hard')

    start_time = datetime.now()

    global hist_subcurcuits, circuit_graph, circuit_truth_tables

    hist_subcurcuits = set()

    # predefined_parameters = {
    #     18: (3, 3, 1),
    #     17: (5, 3, 1),
    #     16: (5, 4, 1),
    #     15: (6, 5, 1),   # previous name: fast
    #     14: (6, 5, 3),
    #     13: (7, 5, 3),
    #     12: (7, 6, 3),
    #     11: (12, 6, 10),
    #     10: (7, 7, 5),   # previous name: medium
    #     9: (7, 7, 10),
    #
    #     8: (7, 9, 30),
    #
    #     7: (8, 8, 10),
    #     6: (16, 8, 20),
    #     5: (8, 8, 20),   # previous name: slow
    #     4: (8, 9, 20),
    #     3: (10, 15, 10),
    #     2: (20, 15, 20),
    #     1: (20, 20, 20),
    # }

    predefined_params = {
        'easy' : ({1 : 7, 2 : 7, 3 : 7, 4 : 6, 5 : 6, 6 : 6}, 6, 7, 30),
        'medium' : ({1 : 9, 2 : 9, 3 : 8, 4 : 8, 5 : 7, 6 : 7, 7 : 7}, 7, 9, 30),
        'hard' : ({1 : 10, 2 : 10, 3 : 10, 4 : 9, 5 : 8, 6 : 8, 7 : 8, 8 : 8}, 8, 10, 30)
    }

    # max_inputs, max_subcircuit_size, time_limit = predefined_parameters[speed]
    dict_inps_to_number_of_gates, max_inputs, max_subcircuit_size, time_limit = predefined_params[speed]
    was_improved = True
    while was_improved:
        time_remaining = int(global_time_limit - (datetime.now() - start_time).total_seconds())
        if time_remaining < 0:
            print(f'...shutting down iterative improvement since {global_time_limit} seconds have passed')
            break

        # print("START CALCULATING TRUTH TABLES")
        # start = time.time()
        was_improved = False
        circuit_graph, circuit_truth_tables = circuit.construct_graph(), circuit.get_truth_tables()
        # print("STOP CALCULATION TRUTH TABLES", time.time() - start)

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
            # winsound.MessageBeep()
            circuit = better_circuit

            if save_circuits:
                circuit.save_to_file(f'_{file_name.replace(".bench", "")}-{basis}-size{str(better_circuit.get_nof_true_binary_gates())}.bench')

    print(f'  Done! time={datetime.now()}')
    return circuit


def improve_single_circuit(input_path: str, output_path: str, speed: str = 'easy', global_time_limit: int = 60):
    assert input_path.endswith('.bench') and output_path.endswith('.bench')
    circuit = Circuit()
    circuit.load_from_file(path=input_path)
    circuit = improve_circuit_iteratively(circuit=circuit, basis='aig', file_name=input_path, save_circuits=False, speed=speed, global_time_limit=global_time_limit)
    circuit.save_to_file(path=output_path)


# if __name__ == "__main__":
#     # cProfile.run("improve_circuit_iteratively(Circuit(file_name=\"ex129\"), \"ex129\", \'aig\', save_circuits=True, speed=8)")
#     # for name in ["ex121", "ex122", "ex123", "ex124"]:
#     #     improve_circuit_iteratively(Circuit(file_name=name), name, 'aig', save_circuits=True, speed=8)
#     # improve_circuit_iteratively(Circuit(file_name="ex155"), "ex155", 'aig', save_circuits=True, speed='medium')
#     improve_circuit_iteratively(Circuit(file_name="ex128"), "ex128", 'aig', save_circuits=True, speed='easy', global_time_limit=60 * 60 * 40)
#     # for name in range(151, 160):
#     #     improve_circuit_iteratively(Circuit(file_name=f'ex{name}'), f'ex{name}', 'aig', save_circuits=True, speed=8)
