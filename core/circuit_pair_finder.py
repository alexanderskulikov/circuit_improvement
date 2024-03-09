from circuit import Circuit
from circuit_search import find_circuit
from itertools import combinations
import networkx as nx
from scipy.special import comb
from timeit import default_timer as timer

circuit = None
circuit_graph = None
subcircuit_enumeration_list = None
gates_already = None
subcircuit_size = 3
count1 = None
count2 = None
gates_in = None
gates_und = None


def get_circuit_object(subcircuit):
    subcircuit_inputs, subcircuit_outputs = set(), set()
    new_gates = {}

    for gate in subcircuit:
        g = circuit.gates[gate]
        if g[0] in subcircuit and g[1] in subcircuit:
            new_gates[gate] = g
        if g[0] in subcircuit and g[1] not in subcircuit:
            new_gates[gate] = (g[0], g[1], g[2])
            subcircuit_inputs.add(g[1])
        if g[0] not in subcircuit and g[1] in subcircuit:
            new_gates[gate] = (g[0], g[1], g[2])
            subcircuit_inputs.add(g[0])
        if g[0] not in subcircuit and g[1] not in subcircuit:
            new_gates[gate] = (g[0], g[1], g[2])
            subcircuit_inputs.add(g[0])
            subcircuit_inputs.add(g[1])

        f = False
        for p in circuit_graph.successors(gate):
            if p not in subcircuit:
                f = True
        if f:
            subcircuit_outputs.add(gate)
            continue

        if gate in circuit.outputs:
            subcircuit_outputs.add(gate)

    subcircuit_inputs = list(subcircuit_inputs)
    subcircuit_outputs = list(subcircuit_outputs)

    new_circuit = Circuit(input_labels=subcircuit_inputs, gates=new_gates, outputs=subcircuit_outputs)

    return new_circuit


def gate_adj(gates, current):
    if len(gates) == 0:
        return True

    for gate in gates:
        if current in circuit_graph.predecessors(gate) or current in circuit_graph.successors(gate):
        # if current in circuit_graph.successors(gate):
            return True

    return False


def f():
    global subcircuit_enumeration_list
    global gates_already
    global gates_in
    global gates_und
    global count1
    global count2

    if len(gates_in) == subcircuit_size:
        if gates_in not in subcircuit_enumeration_list:
            subcircuit_enumeration_list.append(gates_in.copy())
            yield gates_in.copy()
        return

    for gate in gates_und.copy():
        if gate_adj(gates_in, gate):
            gates_in.add(gate)
            gates_und.remove(gate)
            if hash(str(gates_in)) not in gates_already:
                gates_already.add(hash(str(gates_in)))
                yield from f()
            gates_in.remove(gate)
            gates_und.add(gate)
    return


def circuit_pair_finder(crt, filename):
    global circuit
    global circuit_graph
    global subcircuit_enumeration_list
    global gates_already
    global count1
    global count2
    global gates_in
    global gates_und
    global subcircuit_size
    reviewed_subcircuits = []
    variable_iterator = 0
    circuit = crt
    subcircuit_enumeration_list = []

    while True:
        circuit_graph = circuit.construct_graph()
        is_improved = False

        gates_already = set()
        forbiden_gates = set()
        start1 = timer()
        count1 = 0
        count2 = 0
        gates_in = set()
        gates_und = set(list(circuit.gates.keys()))
        # f()
        # a = f()
        # for subcircuit in f():
        #     print(subcircuit)
        # return
        # print(count1)
        # print(count2)
        diff1 = timer() - start1
        # print("subcircuit_enumeration_list length:", len(subcircuit_enumeration_list))
        # print("time spent:", diff1)
        # print("reviewed_subcircuits length:", len(reviewed_subcircuits))
        if len(reviewed_subcircuits) > 500:
            reviewed_subcircuits = []
        print("current circuit size:", len(circuit.gates))

        start2 = timer()
        is_improved = False
        for subcircuit in f():

            boolValue = False
            for item in subcircuit:
                # print("item", item)
                if item in forbiden_gates:
                    boolValue = True
                    break
            if boolValue:
                continue
            if subcircuit in reviewed_subcircuits:
                continue
            subcircuit = list(subcircuit)


            subcircuit_new = get_circuit_object(subcircuit)
            tt = subcircuit_new.get_truth_tables()
            subcircuit_inputs = subcircuit_new.input_labels
            subcircuit_outputs = subcircuit_new.outputs

            improved_circuit = find_circuit(
                dimension=len(subcircuit_inputs),
                input_labels=subcircuit_inputs,
                input_truth_tables=[''.join(map(str, tt[g])) for g in subcircuit_inputs],
                number_of_gates=subcircuit_size - 1,
                output_truth_tables=[''.join(map(str, tt[g])) for g in subcircuit_outputs],
                forbidden_operations=['0000', '0010', '0011', '0100', '0101', '1011', '1101', '1111']
            )

            if not isinstance(improved_circuit, Circuit):
                reviewed_subcircuits.append(set(subcircuit))
                continue

            # print("subcircuit", subcircuit)
            # print('Before:', subcircuit_new)
            # print()
            # print('After:', improved_circuit)
            # print()
            # print("subcircuit_enumeration_list length:", len(subcircuit_enumeration_list))
            list_before = list(range(len(subcircuit_inputs), len(subcircuit_inputs) + subcircuit_size - 1))
            list_after = [("imp" + str(g)) for g in range(variable_iterator, variable_iterator + subcircuit_size - 1)]
            variable_iterator += subcircuit_size - 1
            improved_circuit.change_gates(list_before, list_after)

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



            if not nx.is_directed_acyclic_graph(circuit_graph_copy):
                continue

            is_improved = True

            for gate in subcircuit:
                del circuit.gates[gate]
                forbiden_gates.add(gate)
            for gate in improved_circuit.gates:
                circuit.gates[gate] = improved_circuit.gates[gate]
            circuit.change_gates(subcircuit_outputs, improved_circuit.outputs)
            circuit.save_to_file(filename)
            print("circuit.gates", len(circuit.gates))
            if len(improved_circuit.input_labels) == 2:
                print(improved_circuit)
            # print()
            # for item in subcircuit:
            #     forbiden_gates.add(item)
            # print("forbiden_gates", forbiden_gates)
            # break
        diff2 = timer() - start2
        # print("time spent:", diff2)
        # print()
        if not is_improved:
            # if subcircuit_size == 3:
            #     subcircuit_size = 4
            # else:
            break
    return circuit

def run(filename):
    start = timer()
    print(f'Run {filename}...')
    circuit = Circuit()
    circuit.load_from_file(filename, extension='bench')
    circuit_pair_finder(circuit, filename)
    print(timer() - start)
    print()


if __name__ == '__main__':
    # run("b19_Cg")
    run("fact_58767398799349")





