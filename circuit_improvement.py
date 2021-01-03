from circuit_search_for_improvement import find_circuit
from circuit_shuffle import shuffle
from generate_circuit.generate_ex3_circuit import *
from generate_circuit.generate_ex2_circuit import *
from generate_circuit.generate_sum_circuit import *
from generate_circuit.generate_ib_circuit import *
from generate_circuit.generate_maj_circuit import *
from generate_circuit.generate_mod3_circuit import *
from generate_circuit.generate_th_circuit import *

from itertools import combinations
import networkx as nx
from timeit import default_timer as timer
import random


def is_connected(circuit_graph, subcircuit):
    q = [subcircuit[0]]
    i, count = 0, 1
    while True:
        lst = []
        for cg in circuit_graph.predecessors(q[i]):
            lst.append(cg)
        for cg in circuit_graph.successors(q[i]):
            lst.append(cg)
        for gt in lst:
            if gt in subcircuit and gt not in q:
                q.append(gt)
                count += 1
        if i + 1 < count:
            i = i + 1
        else:
            break

    return len(q) == len(subcircuit)


def correct_subcircuit_count(circuit, subcircuit_size=7, connected=True):
    circuit_graph, count = circuit.construct_graph(), 0
    for subcircuit in combinations(circuit.gates, subcircuit_size):
        if connected:
            if not is_connected(circuit_graph, subcircuit) and connected:
                continue

        subcircuit_outputs = set()
        for gate in subcircuit:
            if gate in circuit.outputs:
                subcircuit_outputs.add(gate)
            else:
                for s in circuit_graph.successors(gate):
                    if s not in subcircuit:
                        subcircuit_outputs.add(gate)
                        break

        if len(subcircuit_outputs) != subcircuit_size:
            count += 1
    return count


def make_truth_tables(circuit, truth_tables, subcircuit_inputs, subcircuit_outputs):
    sub_input_truth_table = {}
    sub_output_truth_table = {}
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


def improve_circuit(circuit, subcircuit_size=5, connected=True):
    print('Trying to improve a circuit of size', len(circuit.gates), flush=True)
    if isinstance(circuit.outputs, str):
        circuit.outputs = [circuit.outputs]
    truth_tables = circuit.get_truth_tables()
    circuit_graph = circuit.construct_graph()
    total, current, time = correct_subcircuit_count(circuit, subcircuit_size, connected=connected), 0, 0
    print(f'\nEnumerating subcircuits of size {subcircuit_size} (total={total})...')
    for subcircuit in combinations(circuit.gates, subcircuit_size):

        if connected:
            if not is_connected(circuit_graph, subcircuit):
                continue

        start = timer()

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

        if len(subcircuit_outputs) == subcircuit_size:
            continue

        current += 1
        print(f'\n{subcircuit_size}: {current}/{total} ({100 * current // total}%) ', end='', flush=True)

        subcircuit_inputs = list(subcircuit_inputs)
        subcircuit_outputs = list(subcircuit_outputs)

        random.shuffle(subcircuit_inputs)
        sub_in_tt, sub_out_tt = make_truth_tables(circuit, truth_tables, subcircuit_inputs, subcircuit_outputs)
        assert find_circuit(subcircuit_inputs, subcircuit_size, sub_in_tt, sub_out_tt)
        improved_circuit = find_circuit(subcircuit_inputs, subcircuit_size-1, sub_in_tt, sub_out_tt)

        if isinstance(improved_circuit, Circuit):
            print('✔', end='', flush=True)
            circuit_graph_copy = circuit.construct_graph()
            improved_circuit_graph = improved_circuit.construct_graph()

            def make_label(label_now, gate_before, gate_after):
                gate_before = str(gate_before)
                gate_after = str(gate_after)
                ss = label_now.split(' ')
                if ss[1] == gate_before:
                    ss[1] = gate_after
                if ss[3] == gate_before:
                    ss[3] = gate_after

                return ss[0] + ' ' + ss[1] + ' ' + ss[2] + ' ' + ss[3]

            for gate in subcircuit:
                if gate not in subcircuit_inputs:
                    circuit_graph_copy.remove_node(gate)
            for gate in improved_circuit.gates:
                assert gate not in subcircuit_inputs
                labels = []
                for p in improved_circuit_graph.predecessors(gate):
                    labels.append(str(p))
                circuit_graph_copy.add_node(gate,
                                            label=f'{gate}: {labels[0]} {improved_circuit.gate_types[improved_circuit.gates[gate][2]]} {labels[1]}')
                for p in improved_circuit_graph.predecessors(gate):
                    circuit_graph_copy.add_edge(p, gate)

            for i in range(len(subcircuit_outputs)):
                for s in circuit_graph.successors(subcircuit_outputs[i]):
                    if s in circuit_graph_copy.nodes:
                        circuit_graph_copy.add_edge(improved_circuit.outputs[i], s)
                        circuit_graph_copy.nodes[s]['label'] = make_label(circuit_graph_copy.nodes[s]['label'],
                                                                          subcircuit_outputs[i],
                                                                          improved_circuit.outputs[i])

            if nx.is_directed_acyclic_graph(circuit_graph_copy):
                print('\nCircuit Improved!\n', end='', flush=True)
                print(improved_circuit)
                improved_full_circuit = Circuit.make_circuit(circuit_graph_copy, circuit.input_labels,
                                                             make_improved_circuit_outputs(circuit.outputs,
                                                                                           subcircuit_outputs,
                                                                                           improved_circuit.outputs))
                improved_full_circuit.save_to_file('circuit_improved')
                exit()

        stop = timer()
        time += stop - start
        remaining = time / current * (total - current)
        print(f' | curr: {int(stop - start)} sec | rem: {int(remaining)} sec ({round(remaining / 60, 1)} min)', end='',
              flush=True)


def run_file(filename, subcircuit_size=5, connected=True):
    print(f'Run {filename}...')
    c = Circuit()
    c.load_from_file(filename)
    improve_circuit(c, subcircuit_size, connected)


def run_file_shuffle(filename, subcircuit_size=5, connected=True):
    print(f'Run {filename}...')
    c = Circuit()
    c.load_from_file(filename)
    shuffle(c, subcircuit_size, connected)


def run(fun, input_size, subcircuit_size=5, connected=True):
    print(f'Run {fun.__name__}...')
    c = Circuit(input_labels=[f'x{i}' for i in range(1, input_size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    improve_circuit(c, subcircuit_size, connected)


def run_shuffle(fun, input_size, subcircuit_size=5, connected=True):
    print(f'Run {fun.__name__}...')
    c = Circuit(input_labels=[f'x{i}' for i in range(1, input_size + 1)], gates={})
    c.outputs = fun(c, c.input_labels)
    shuffle(c, subcircuit_size, connected)
