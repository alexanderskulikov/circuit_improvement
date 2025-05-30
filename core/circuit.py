import os
from itertools import product
from typing import List, Any, Union

import networkx as nx
import random
from string import ascii_lowercase
from .zhegalkin_polynomial import ZhegalkinPolynomial, ZhegalkinTree



class Circuit:
    gate_types = {
        # constants
        '0000': '0',
        '1111': '1',
        # degenerate
        '0011': 'x',
        '1100': 'not',
        '0101': 'y',
        '1010': 'not',
        # xor-type
        '0110': '+',
        '1001': '=',
        # and-type
        '0001': '∧',
        '1110': '⊼',
        '0111': 'v',
        '1000': '⊽',
        '0010': '>',
        '0100': '<',
        '1011': '≥',
        '1101': '≤',
    }

    gate_bench_types = {
        'XOR': '0110',
        'OR': '0111',
        'AND': '0001',
        'NOT': '1100',
        'BUFF': '0011',
        'NAND': '1110',
        'NOR': '1000',
        'NXOR': '1001',
        'XNOR': '1001',

        '1001': '=',
        '0010': '>',
        '0100': '<',
        '1011': '>=',
        '1101': '<=',
    }

    def __init__(self, input_labels=None, gates=None, outputs=None, file_name=None, graph=None):
        self.input_labels = input_labels or []
        self.gates = gates or {}
        self.outputs = outputs or []
        self.outputs_negations = [False] * len(self.outputs)
        if graph is not None and input_labels is not None and outputs is not None:
            self.__get_from_graph(graph)
        if file_name is not None:
            self.load_from_file(file_name)
        self._new_node_counter = 0

    def __str__(self):
        s = 'Inputs: ' + ' '.join(map(str, self.input_labels)) + '\n'

        for gate in self.gates:
            s += f'{gate}: ({self.gates[gate][0]} {self.gate_types[self.gates[gate][2]]} {self.gates[gate][1]})\n'

        s += 'Outputs: '
        self.outputs_negations = self.outputs_negations or [False] * len(self.outputs)
        for output, is_negated in zip(self.outputs, self.outputs_negations):
            if is_negated:
                s += '-'
            s += f'{output} '

        return s

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
        self.outputs_negations = [False] * number_of_outputs

    def __load_from_string_bench(self, string):
        def ch(ss: str):
            return "ch" + ss if ss.isnumeric() else ss

        lines = string.splitlines()

        self.input_labels = []
        self.outputs = []
        self.outputs_negations = []
        self.gates = {}

        for line in lines:
            line = line.strip()
            if len(line) == 0 or line.startswith('#'):
                continue
            elif line.startswith('INPUT'):
                self.input_labels.append(ch(line[6:-1]))
            elif line.startswith('OUTPUT'):
                self.outputs.append(ch(line[7:-1]))
                self.outputs_negations.append(False)
            else:
                nls = line.replace(" ", "").replace("=", ",").replace("(", ",").replace(")", "").split(",")
                if len(nls) == 4:
                    self.gates[ch(nls[0])] = (ch(nls[2]), ch(nls[3]), self.gate_bench_types[nls[1]])
                elif len(nls) == 3:
                    self.gates[ch(nls[0])] = (ch(nls[2]), ch(nls[2]), self.gate_bench_types[nls[1]])
                else:
                    gatename = ch(nls[0])
                    opername = nls[1]
                    nls = nls[2:]
                    prev = nls[0] + "plus" + gatename
                    self.gates[prev] = (ch(nls[0]), ch(nls[1]), self.gate_bench_types[opername])
                    for i in range(2, len(nls)):
                        neww = nls[i] + "plus" + gatename
                        if i == len(nls) - 1:
                            neww = gatename
                        self.gates[neww] = (prev, ch(nls[i]), self.gate_bench_types[opername])
                        prev = neww

    def load_from_file(self, path: str):
        with open(path) as circuit_file:
            if path.endswith('.ckt'):
                self.__load_from_string_ckt(circuit_file.read())
            elif path.endswith('.bench'):
                self.__load_from_string_bench(circuit_file.read())
            else:
                assert 'Unrecognized circuit format'

    def __save_to_ckt(self):
        file_data = f'{len(self.input_labels)} {len(self.gates)} {len(self.outputs)}\n'
        file_data += ' '.join(map(str, self.input_labels))

        for gate in self.gates:
            first, second, gate_type = self.gates[gate]
            file_data += f'\n{gate} {first} {second} {gate_type}'

        file_data += '\n'
        self.outputs_negations = self.outputs_negations or [False] * len(self.outputs)
        for output, is_negated in zip(self.outputs, self.outputs_negations):
            if is_negated:
                file_data += '-'
            file_data += f'{output} '

        return file_data

    def __save_to_bench(self):
        file_data = '\n'.join(f'INPUT({l})' for l in self.input_labels) + '\n'

        neg_prefix, neg_counter = 'tmpneg', 1

        for gat in list(nx.topological_sort(self.construct_graph())):
            gate = gat[::1]
            if gate in self.input_labels:
                continue

            first, second, gate_type = self.gates[gate]

            if neg_prefix in gate and gate_type not in ['0010', '0100', '1011', '1101']:
                for i in range(len(self.outputs)):
                    if self.outputs[i] == gate:
                        self.outputs[i] = f'{neg_prefix}{neg_counter}'
                gate = f'{neg_prefix}{neg_counter}'
                neg_counter += 1

            if gate_type == '0110':
                file_data += f'\n{gate}=XOR({first}, {second})'
            elif gate_type == '1001':
                file_data += f'\n{gate}=NXOR({first}, {second})'
            elif gate_type == '0001':
                file_data += f'\n{gate}=AND({first}, {second})'
            elif gate_type == '0111':
                file_data += f'\n{gate}=OR({first}, {second})'
            elif gate_type == '0010':
                new_var = f'{neg_prefix}{neg_counter}'
                neg_counter += 1
                file_data += f'\n{new_var}=NOT({second})'
                file_data += f'\n{gate}=AND({first}, {new_var})'
            elif gate_type == '0100':
                new_var = f'{neg_prefix}{neg_counter}'
                neg_counter += 1
                file_data += f'\n{new_var}=NOT({first})'
                file_data += f'\n{gate}=AND({new_var}, {second})'
            elif gate_type == '1011':
                new_var = f'{neg_prefix}{neg_counter}'
                neg_counter += 1
                file_data += f'\n{new_var}=NOT({second})'
                file_data += f'\n{gate}=OR({first}, {new_var})'
            elif gate_type == '1101':
                new_var = f'{neg_prefix}{neg_counter}'
                neg_counter += 1
                file_data += f'\n{new_var}=NOT({first})'
                file_data += f'\n{gate}=OR({new_var}, {second})'
            elif gate_type == '1000':
                file_data += f'\n{gate}=NOR({first}, {second})'
            elif gate_type == '1110':
                file_data += f'\n{gate}=NAND({first}, {second})'
            elif gate_type == '1100':
                assert first == second
                file_data += f'\n{gate}=NOT({first})'
            elif gate_type == '0011':
                assert first == second
                file_data += f'\n{gate}=BUFF({first})'
            else:
                assert False, f'Gate type not yet supported: {gate_type}'

        file_data += '\n\n'

        self.outputs_negations = self.outputs_negations or [False] * len(self.outputs)
        for output, is_negated in zip(self.outputs, self.outputs_negations):
            if is_negated:
                new_var = f'{neg_prefix}{neg_counter}'
                neg_counter += 1
                file_data += f'\n{new_var}=NOT({output})'
                file_data += f'\nOUTPUT({new_var})'
            else:
                file_data += f'\nOUTPUT({output})'

        return file_data

    def save_to_file(self, path: str):
        with open(path, 'w') as circuit_file:
            if path.endswith('.ckt'):
                circuit_file.write(self.__save_to_ckt())
            elif path.endswith('.bench'):
                circuit_file.write(self.__save_to_bench())
            else:
                assert 'Unrecognized circuit format'

        print(f'Circuit saved to: {path}')

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
            self.gates[gate] = (
                (graph.nodes[gate]['label']).split()[1], (graph.nodes[gate]['label']).split()[3], bit_operation)

    def draw(self, file_name='circuit', detailed_labels=False, experimental=False, highlight_gates=None):
        highlight_gates = highlight_gates or []
        circuit_graph = self.construct_graph(detailed_labels)
        a = nx.nx_agraph.to_agraph(circuit_graph)

        for gate in self.input_labels:
            a.get_node(gate).attr['shape'] = 'invtriangle'

        for gate in self.gates:
            if detailed_labels:
                a.get_node(gate).attr['shape'] = 'rectangle'
            else:
                a.get_node(gate).attr['shape'] = 'circle'

        for gate in highlight_gates:
            a.get_node(gate).attr['style'] = 'filled'
            a.get_node(gate).attr['fillcolor'] = 'green3'

        if isinstance(self.outputs, str):
            self.outputs = [self.outputs]

        self.outputs_negations = self.outputs_negations or [False] * len(self.outputs)
        for output_id, (output, is_negated) in enumerate(zip(self.outputs, self.outputs_negations)):
            output_label = f'tout{output_id}'
            a.add_node(output_label)
            a.get_node(output_label).attr['shape'] = 'invtriangle'
            a.add_edge(output, output_label)
            if is_negated:
                a.get_edge(output, output_label).attr['style'] = 'dashed'

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
        a.draw(file_name)
        print(f'Circuit image saved to: {file_name}')

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
                assert gate in self.gates, f'unknown gate: {gate}'
                f, s = self.gates[gate][0], self.gates[gate][1]
                assert len(truth_tables[f]) > len(truth_tables[gate]) and len(truth_tables[s]) > len(truth_tables[gate])
                fv, sv = truth_tables[f][-1], truth_tables[s][-1]
                truth_tables[gate].append(int(self.gates[gate][2][sv + 2 * fv]))

        return truth_tables

    def get_zhegalkin_polynomials(self):
        polynomials = {}
        topological_ordering = list(nx.topological_sort(self.construct_graph()))
        for gate in topological_ordering:
            if gate in self.input_labels:
                polynomials[gate] = ZhegalkinPolynomial(self.input_labels, [[self.input_labels.index(gate)]])
                continue
            assert gate in self.gates, f'unknown gate: {gate}'
            f, s = self.gates[gate][0], self.gates[gate][1]
            op = self.gates[gate][2]
            f_polynom = polynomials[f]
            s_polynom = polynomials[s]
            polynomials[gate] = ZhegalkinPolynomial.merge_polynomials(f_polynom, s_polynom, op)

        return polynomials

    def add_zhegalkin_polynomials(self, polynomials: List[ZhegalkinPolynomial], add_outputs: bool = False) -> List:
        assert all(self.input_labels == p.input_labels for p in polynomials), "Input_labels should be aligned"
        assert len(polynomials) > 0, "At least one polynomial should be provided"

        def add_gate(label, first, second, op):
            if label in self.gates.keys():
                return
            self.add_gate(first, second, op, label)

        monom_pref = "m"
        xor_pref = "x"
        not_pref = "not"

        def monom_to_gate(monom):
            assert monom != 0
            if monom.bit_count() == 1:
                idx = bin(monom)[::-1].index('1')
                return self.input_labels[idx]
            else:
                return f"{monom_pref}_{monom}"

        def add_monom(monom):
            assert monom != 0
            monom_inputs = [i for i in range(len(self.input_labels)) if monom >> i & 1]
            prev = 2 ** monom_inputs[0]
            for i, elem in enumerate(monom_inputs):
                if i == 0:
                    continue
                nxt = prev | 2 ** monom_inputs[i]
                add_gate(monom_to_gate(nxt), monom_to_gate(prev), self.input_labels[elem], "0001")
                prev = nxt

        def add_not(gate):
            assert gate is not None
            new_gate = f"{not_pref}_{gate}"
            add_gate(new_gate, gate, gate, "1100")
            return new_gate

        def add_xor(gate, monom):
            assert monom != 0
            new_gate = f"{gate}_{xor_pref}_{monom_to_gate(monom)}"
            add_gate(new_gate, gate, monom_to_gate(monom), op="0110")
            return new_gate

        outputs = []
        for polynomial in polynomials:
            should_not = False
            gate = None

            if len(polynomial.monomials) == 0 or polynomial.monomials == {0}:
                gate = f"const_0"
                add_gate(gate, self.input_labels[0], self.input_labels[0], '0000')
            for m in polynomial.monomials:
                if m == 0:
                    should_not = True
                else:
                    add_monom(m)
                    if gate is None:
                        gate = monom_to_gate(m)
                    else:
                        gate = add_xor(gate, m)
            if should_not:
                gate = add_not(gate)
            outputs.append(gate)
            if add_outputs:
                self.outputs.append(gate)
                self.outputs_negations.append(False)
        return outputs

    def add_zhegalkin_trees(self, trees: List[ZhegalkinTree], add_outputs: bool = False) -> List:

        def add_subtree(node: Union[ZhegalkinTree.Node, ZhegalkinTree, ZhegalkinPolynomial]) -> Any:
            if isinstance(node, ZhegalkinPolynomial):
                return self.add_zhegalkin_polynomials([node])[0]
            elif isinstance(node, ZhegalkinTree):
                return add_subtree(node.root)
            else:
                assert isinstance(node, ZhegalkinTree.Node)
                left_gate = add_subtree(node.left)
                right_gate = add_subtree(node.right)
                root_label = f"_tree_op_{self._new_node_counter}"
                self._new_node_counter += 1
                self.add_gate(left_gate, right_gate, node.op, gate_label=root_label)
                return root_label

        roots = []
        for t in trees:
            root = add_subtree(t)
            roots.append(root)
        if add_outputs:
            self.outputs.extend(roots)
            self.outputs_negations.extend([False] * len(roots))
        return roots

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
            new_gates[list_after[list_before.index(gate)] if gate in list_before else gate] = (
                list_after[list_before.index(value[0])] if value[0] in list_before else value[0],
                list_after[list_before.index(value[1])] if value[1] in list_before else value[1], value[2])
        self.gates = new_gates

    def get_nof_true_binary_gates(self):
        nof_gates = 0
        for gate in self.gates:
            _, _, gate_type = self.gates[gate]
            if gate_type not in ('0000', '1111', '0011', '1100', '0101', '1010'):
                nof_gates += 1
        return nof_gates

    # propagate NOT gates into successors
    def contract_unary_gates(self):
        new_gate_contracted = True
        while new_gate_contracted:
            new_gate_contracted = False

            for gate in self.gates:
                x, y, gate_type = self.gates[gate]
                assert gate_type != '1010' and gate_type != '0101', 'y and NOT(y) are not supported yet'
                if gate_type == '1100':  # NOT gates
                    assert x == y

                    for i in range(len(self.outputs)):
                        if self.outputs[i] == gate:
                            self.outputs[i] = x
                            assert 0 <= i < len(
                                self.outputs_negations), f"{type(i)}: {i} \\notin [0, {len(self.outputs_negations)})"
                            self.outputs_negations[i] = not self.outputs_negations[i]

                    for successor in self.gates:
                        sx, sy, stype = self.gates[successor]
                        if sx == sy and sx == gate:
                            assert stype == '1100'
                            self.gates[successor] = (x, x, '0011')
                        elif sx == gate:
                            self.gates[successor] = (x, sy, stype[2:] + stype[:2])
                        elif sy == gate:
                            self.gates[successor] = (sx, x, stype[1] + stype[0] + stype[3] + stype[2])

                    self.gates.pop(gate)
                    new_gate_contracted = True
                    break
                # elif gate_type == '0011':  # BUFF gates
                #     assert x == y
                #
                #     if gate in self.outputs:
                #         gate_index = self.outputs.index(gate)
                #         self.outputs[gate_index] = x
                #     else:
                #         for successor in self.gates:
                #             sx, sy, stype = self.gates[successor]
                #             if sx == sy and sx == gate:
                #                 self.gates[successor] = (x, x, stype)
                #             elif sx == gate:
                #                 self.gates[successor] = (x, sy, stype)
                #             elif sy == gate:
                #                 self.gates[successor] = (sx, x, stype)
                #
                #     self.gates.pop(gate)
                #     new_gate_contracted = True
                #     break

    # if a gate g is fed by a and b such that both
    # a and b are fed by с and d, then g is replaced by a function of c and d
    def contract_gates(self, basis):
        assert basis in ('xaig', 'aig')

        new_gate_contracted = True
        while new_gate_contracted:
            new_gate_contracted = False

            for gate in self.gates:
                a, b, gate_type = self.gates[gate]

                if gate_type in ('0000', '1111', '0011', '1100', '0101', '1010'):
                    continue

                if a in self.input_labels or b in self.input_labels or a == b:
                    continue

                a1, a2, a_type = self.gates[a]
                b1, b2, b_type = self.gates[b]

                if a1 == a2 or b1 == b2:
                    continue

                if a1 == b1 and a2 == b2:
                    new_type = ''.join([gate_type[2 * int(a_type[2 * c1 + c2]) + int(b_type[2 * c1 + c2])] for c1, c2 in
                                        product((0, 1), repeat=2)])
                    if basis != 'aig' or new_type not in ['0110', '1001']:
                        self.gates[gate] = a1, a2, new_type
                        new_gate_contracted = True
                        break
                elif a1 == b2 and a2 == b1:
                    new_type = ''.join([gate_type[2 * int(a_type[2 * c1 + c2]) + int(b_type[2 * c2 + c1])] for c1, c2 in
                                        product((0, 1), repeat=2)])
                    if basis != 'aig' or new_type not in ['0110', '1001']:
                        self.gates[gate] = a1, a2, new_type
                        new_gate_contracted = True
                        break

    def remove_dangling_gates(self):
        dangling_gate_removed = True
        while dangling_gate_removed:
            dangling_gate_removed = False

            graph = self.construct_graph()

            for gate in graph.nodes:
                if gate not in self.outputs and gate not in self.input_labels and graph.out_degree(gate) == 0:
                    self.gates.pop(gate)
                    dangling_gate_removed = True

    def normalize(self, basis):
        assert basis in ('aig', 'xaig')
        self.contract_unary_gates()
        self.contract_gates(basis=basis)
        self.remove_dangling_gates()

    # prepends all internal gate (i.e., gates that are not inputs and outputs) names with the string prefix
    # to avoid names clashes with other circuits
    def rename_internal_gates(self, prefix=''):
        if not prefix:
            prefix = ''.join(random.choice(ascii_lowercase) for _ in range(5))

        def new_name(old_name):
            return prefix + str(
                old_name) if old_name not in self.input_labels and old_name not in self.outputs else str(old_name)

        new_gates = dict()
        for gate in self.gates:
            first, second, gate_type = self.gates[gate]
            new_gates[new_name(gate)] = new_name(first), new_name(second), gate_type

        self.gates = new_gates

    def rename_output_gates(self, output_gate_labels):
        assert len(self.outputs) == len(output_gate_labels)
        for name in output_gate_labels:
            assert name not in self.input_labels and name not in self.outputs and name not in self.gates

        def new_name(old_name):
            return output_gate_labels[self.outputs.index(old_name)] if old_name in self.outputs else old_name

        new_gates = dict()
        for gate in self.gates:
            first, second, gate_type = self.gates[gate]
            new_gates[new_name(gate)] = new_name(first), new_name(second), gate_type

        self.gates = new_gates
        self.outputs = output_gate_labels

    def merge_gates(self, first_gate, second_gate):
        assert first_gate in self.gates and second_gate in self.gates

        order = list(nx.topological_sort(self.construct_graph()))
        (to_be_replaced_gate, by_gate) = (first_gate, second_gate) if order.index(first_gate) > order.index(
            second_gate) else (second_gate, first_gate)

        self.gates.pop(to_be_replaced_gate)

        for gate in self.gates:
            if self.gates[gate][0] == to_be_replaced_gate:
                self.gates[gate] = by_gate, self.gates[gate][1], self.gates[gate][2]
            if self.gates[gate][1] == to_be_replaced_gate:
                self.gates[gate] = self.gates[gate][0], by_gate, self.gates[gate][2]

        for idx in range(len(self.outputs)):
            if self.outputs[idx] == to_be_replaced_gate:
                self.outputs[idx] = by_gate