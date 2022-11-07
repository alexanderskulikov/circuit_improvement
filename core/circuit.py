from itertools import product
import networkx as nx
import os

project_directory = os.path.dirname(os.path.abspath("path"))


class Circuit:
    gate_types = {
        # constants
        '0000': '0',
        '1111': '1',
        # degenerate
        '0011': 'x',
        '1100': 'not(x)',
        '0101': 'y',
        '1010': 'not(y)',
        # xor-type
        '0110': '+',
        '1001': '=',
        # and-type
        '0001': 'and',
        '1110': 'nand',
        '0111': 'or',
        '1000': 'nor',
        '0010': '>',
        '0100': '<',
        '1011': '>=',
        '1101': '<=',
    }

    gate_bench_types = {
        'XOR': '0110',
        'OR': '0111',
        'AND': '0001',
        'NOT': '1100',
        'NAND': '1110',
        'NOR': '1000',


        '1001': '=',
        '0010': '>',
        '0100': '<',
        '1011': '>=',
        '1101': '<=',
    }

    def __init__(self, input_labels=None, gates=None, outputs=None, fn=None, graph=None):
        self.input_labels = input_labels or []
        self.gates = gates or {}
        self.outputs = outputs or []
        if graph is not None and input_labels is not None and outputs is not None:
            self.__get_from_graph(graph)
        if fn is not None:
            self.load_from_file(fn)

    def __str__(self):
        s = ''
        s += 'Inputs: ' + ' '.join(map(str, self.input_labels)) + '\n'
        for gate in self.gates:
            s += f'{gate}: ({self.gates[gate][0]} {self.gate_types[self.gates[gate][2]]} {self.gates[gate][1]})\n'
        s += 'Outputs: ' + ' '.join(map(str, self.outputs))
        return s

    @staticmethod
    def find_file(filename):
        fname = []
        for root, d_names, f_names in os.walk(project_directory):
            for f in f_names:
                if f == filename:
                    fname.append(os.path.join(root, f))

        assert len(fname) == 1
        return fname[0]

    def __load_from_string_ckt(self, string):
        lines = string.splitlines()
        number_of_inputs, number_of_gates, number_of_outputs = \
            list(map(int, lines[0].strip().split()))
        self.input_labels = lines[1].strip().split()
        assert len(self.input_labels) == number_of_inputs

        self.gates = {}
        for i in range(number_of_gates):
            gate, first, second, gate_type = lines[i + 2].strip().split()
            self.gates[gate] = (first, second, gate_type)

        self.outputs = lines[number_of_gates + 2].strip().split()
        assert len(self.outputs) == number_of_outputs

    # TODO: handle multiply gates
    def __load_from_string_bench(self, string):
        lines = string.splitlines()

        self.input_labels = []
        self.outputs = []
        self.gates = {}

        for line in lines:
            if len(line) == 0 or line.startswith('#'):
                continue
            elif line.startswith('INPUT'):
                self.input_labels.append(line[6:-1])
            elif line.startswith('OUTPUT'):
                self.outputs.append(line[7:-1])
            else:
                nls = line.replace(" ", "").replace("=", ",").replace("(", ",").replace(")", "").split(",")
                if len(nls) == 4:
                    self.gates[nls[0]] = (nls[2], nls[3], self.gate_bench_types[nls[1]])
                else:
                    self.gates[nls[0]] = (nls[2], nls[2], self.gate_bench_types[nls[1]])

    def load_from_file(self, file_name, extension='ckt'):
        with open(Circuit.find_file(file_name + '.' + extension)) as circuit_file:
            if extension == 'ckt':
                self.__load_from_string_ckt(circuit_file.read())

            if extension == 'bench':
                self.__load_from_string_bench(circuit_file.read())

    def __save_to_ckt(self):
        file_data = ''
        file_data += f'{len(self.input_labels)} {len(self.gates)} {len(self.outputs)}\n'
        file_data += ' '.join(self.input_labels)

        for gate in self.gates:
            first, second, gate_type = self.gates[gate]
            file_data += f'\n{gate} {first} {second} {gate_type}'
        file_data += '\n' + ' '.join([str(i) for i in self.outputs])
        return file_data

    # TODO: write this method
    def __save_to_bench(self):
        return 'lol'

    def save_to_file(self, file_name, extension='ckt'):
        file_data = ''
        if extension == 'ckt':
            file_data = self.__save_to_ckt()

        if extension == 'bench':
            file_data = self.__save_to_bench()

        with open(project_directory + '/circuits/' + file_name + '.' + extension, 'w') as circuit_file:
            circuit_file.write(file_data)

    def construct_graph(self, detailed_labels=True):
        circuit_graph = nx.DiGraph()
        for input_label in self.input_labels:
            circuit_graph.add_node(input_label)

        for gate in self.gates:
            label = self.gate_types[self.gates[gate][2]]
            if detailed_labels:
                label = f'{gate}: {self.gates[gate][0]} {self.gate_types[self.gates[gate][2]]} {self.gates[gate][1]}'
            circuit_graph.add_node(gate, label=label)
            circuit_graph.add_edge(self.gates[gate][0], gate)
            circuit_graph.add_edge(self.gates[gate][1], gate)

        return circuit_graph

    def __get_from_graph(self, graph):
        for gate in graph.pred:
            if gate in self.input_labels:
                continue
            operation = (graph.nodes[gate]['label']).split()[2]
            bit_operation = list(self.gate_types.keys())[list(self.gate_types.values()).index(operation)]
            self.gates[gate] = ((graph.nodes[gate]['label']).split()[1], (graph.nodes[gate]['label']).split()[3], bit_operation)

    # TODO: check this method
    def replace_subgraph(self, improved_circuit, subcircuit, subcircuit_outputs):
        circuit_graph = self.construct_graph()
        replaced_graph = self.construct_graph()
        subcircuit_inputs = improved_circuit.input_labels
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
                replaced_graph.remove_node(gate)
        for gate in improved_circuit.gates:
            assert gate not in subcircuit_inputs
            labels = []
            for p in improved_circuit_graph.predecessors(gate):
                labels.append(str(p))
            replaced_graph.add_node(gate,
                                    label=f'{gate}: {labels[0]} {improved_circuit.gate_types[improved_circuit.gates[gate][2]]} {labels[1]}')
            for p in improved_circuit_graph.predecessors(gate):
                replaced_graph.add_edge(p, gate)

        for i in range(len(subcircuit_outputs)):
            for s in circuit_graph.successors(subcircuit_outputs[i]):
                if s in replaced_graph.nodes:
                    replaced_graph.add_edge(improved_circuit.outputs[i], s)
                    replaced_graph.nodes[s]['label'] = make_label(replaced_graph.nodes[s]['label'],
                                                                  subcircuit_outputs[i],
                                                                  improved_circuit.outputs[i])
        return replaced_graph

    # TODO: check this method
    def draw(self, file_name='circuit', detailed_labels=True, experimental=False):
        circuit_graph = self.construct_graph(detailed_labels)
        a = nx.nx_agraph.to_agraph(circuit_graph)
        for gate in self.input_labels:
            a.get_node(gate).attr['shape'] = 'box'
        if isinstance(self.outputs, str):
            self.outputs = [self.outputs]
        for output in self.outputs:
            a.get_node(output).attr['shape'] = 'box'

        if experimental:
            for g in self.gates:
                distance_to_inputs = float('inf')
                for i in self.input_labels:
                    if nx.has_path(circuit_graph, i, g):
                        distance_to_inputs = min(distance_to_inputs, nx.shortest_path_length(circuit_graph, i, g))

                if distance_to_inputs <= 2:
                    a.get_node(g).attr['style'] = 'filled'
                    if distance_to_inputs == 1:
                        a.get_node(g).attr['fillcolor'] = 'green3'
                    else:
                        a.get_node(g).attr['fillcolor'] = 'green4'

                if self.gates[g][2] != '0110' and self.gates[g][2] != '1001':
                    a.get_node(g).attr['style'] = 'filled'
                    a.get_node(g).attr['fillcolor'] = 'coral'

        a.layout(prog='dot')

        file_name = project_directory + '/circuits/.images/' + file_name + '.png'
        a.draw(file_name)
        print(f'Circuit image: {file_name}')

    def get_truth_tables(self):
        truth_tables = {}

        for gate in self.input_labels:
            truth_tables[gate] = []
        for gate in self.gates:
            truth_tables[gate] = []

        topological_ordering = list(nx.topological_sort(self.construct_graph()))

        for assignment in product(range(2), repeat=len(self.input_labels)):
            for i in range(len(self.input_labels)):
                truth_tables[self.input_labels[i]].append(assignment[i])

            for gate in topological_ordering:
                if gate in self.input_labels:
                    continue
                assert gate in self.gates
                f, s = self.gates[gate][0], self.gates[gate][1]
                assert len(truth_tables[f]) > len(truth_tables[gate]) and len(truth_tables[s]) > len(truth_tables[gate])
                fv, sv = truth_tables[f][-1], truth_tables[s][-1]
                truth_tables[gate].append(int(self.gates[gate][2][sv + 2 * fv]))

        return truth_tables

    def add_gate(self, first_predecessor, second_predecessor, operation, gate_label=None):
        if not gate_label:
            gate_label = f'z{len(self.gates)}'
        assert gate_label not in self.gates and gate_label not in self.input_labels
        self.gates[gate_label] = (first_predecessor, second_predecessor, operation)
        return gate_label

    def change_gates(self, list_before, list_after):
        new_input_labels = []
        for gate in self.input_labels:
            new_input_labels.append(list_after[list_before.index(gate)] if gate in list_before else gate)
        self.input_labels = new_input_labels

        new_output_labels = []
        for gate in self.outputs:
            new_output_labels.append(list_after[list_before.index(gate)] if gate in list_before else gate)
        self.outputs = new_output_labels

        new_gates = {}
        for gate in self.gates:
            value = self.gates[gate]
            new_gates[list_after[list_before.index(gate)] if gate in list_before else gate] = (list_after[list_before.index(value[0])] if value[0] in list_before else value[0], list_after[list_before.index(value[1])] if value[1] in list_before else value[1], value[2])
        self.gates = new_gates