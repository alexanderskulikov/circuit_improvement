from circuit import Circuit
from circuit_search import find_circuit, CircuitFinder
from itertools import product
from math import ceil, log2
from circuit_improvement import *
from functions.sum import check_sum_circuit
from pysat.solvers import Glucose3
from pysat.card import ITotalizer
import pycosat
import time
from os import walk
from pysat.formula import CNF
from pysat.solvers import Solver
from functions.th import add_thn
from pysat.card import *

def save_cnf_formula_to_file(file_name, clauses, var_count):
    with open(file_name, 'w') as file:
        file.write(f'p cnf {var_count} {len(clauses)}\n')
        for clause in clauses:
            file.write(f'{" ".join(map(str, clause))} 0\n')
        for v in range(1, var_count + 1):
            file.write(f'c x{v} {v}\n')

def clique_n2(n, k, edges):
    clauses = []

    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if (i, j) not in edges:
                clauses += [[-i, -j]]

    true = n * (k + 1) + 1
    var_count = false = true + 1
    clauses += [[true]]
    clauses += [[-false]]

    def get_s(i, j):
        if j == 0:
            return true
        if i == 0:
            return false
        return n + (i - 1) * k + j

    for i in range(1, n + 1):
        for j in range(1, k + 1):
            clauses += [[-get_s(i - 1, j), get_s(i, j)]]
            clauses += [[-i, -get_s(i - 1, j - 1), get_s(i, j)]]
            clauses += [[-get_s(i, j), get_s(i - 1, j), i]]
            clauses += [[-get_s(i, j), get_s(i - 1, j), get_s(i - 1, j - 1)]]

    clauses += [[get_s(n, k)]]

    save_cnf_formula_to_file('clique.cnf', clauses, var_count)
    return clauses, 'n^2'


def clique_n2_th20n(n, k, edges):
    clauses = []

    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if (i, j) not in edges:
                clauses += [[-i, -j]]

    c = Circuit(input_labels=[f'x{i}' for i in range(1, n + 1)], gates={})
    c.outputs = add_thn(c, c.input_labels, k)

    def makesatvar(s):
        if s[0] == 'x':
            return int(s[1:])
        else:
            return int(s[1:]) + n + 1

    for gate in c.gates.keys():
        var = makesatvar(gate)
        pr1 = makesatvar(c.gates[gate][0])
        pr2 = makesatvar(c.gates[gate][1])
        op = c.gates[gate][2]
        clauses += [[pr1, pr2, var if op[0] == '1' else -var]]
        clauses += [[pr1, -pr2, var if op[1] == '1' else -var]]
        clauses += [[-pr1, pr2, var if op[2] == '1' else -var]]
        clauses += [[-pr1, -pr2, var if op[3] == '1' else -var]]

    clauses += [[makesatvar(c.outputs)]]

    save_cnf_formula_to_file('clique.cnf', clauses, n + len(c.gates))
    return clauses, '20n'

def clique_n2_th18n(n, k, edges):
    clauses = []

    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if (i, j) not in edges:
                clauses += [[-i, -j]]

    c = Circuit(input_labels=[f'x{i}' for i in range(1, n + 1)], gates={})
    c.outputs = add_thn(c, c.input_labels, k, is5n=False)

    def makesatvar(s):
        if s[0] == 'x':
            return int(s[1:])
        else:
            return int(s[1:]) + n + 1

    for gate in c.gates.keys():
        var = makesatvar(gate)
        pr1 = makesatvar(c.gates[gate][0])
        pr2 = makesatvar(c.gates[gate][1])
        op = c.gates[gate][2]
        clauses += [[pr1, pr2, var if op[0] == '1' else -var]]
        clauses += [[pr1, -pr2, var if op[1] == '1' else -var]]
        clauses += [[-pr1, pr2, var if op[2] == '1' else -var]]
        clauses += [[-pr1, -pr2, var if op[3] == '1' else -var]]

    clauses += [[makesatvar(c.outputs)]]

    save_cnf_formula_to_file('clique.cnf', clauses, n + len(c.gates))
    return clauses, '18n'


def clique_kn(n, k, edges):
    clauses = []

    def get_s(i, j):
        return (i - 1) * n + j

    for j1 in range(1, n + 1):
        for j2 in range(j1 + 1, n + 1):
            for i1 in range(1, k + 1):
                for i2 in range(i1 + 1, k + 1):
                    if (j1, j2) not in edges:
                        clauses += [[-get_s(i1, j1), -get_s(i2, j2)]]
                        clauses += [[-get_s(i1, j2), -get_s(i2, j1)]]

    for j in range(1, n + 1):
        for i1 in range(1, k + 1):
            for i2 in range(i1 + 1, k + 1):
                clauses += [[-get_s(i1, j), -get_s(i2, j)]]

    for i in range(1, k + 1):
        for j1 in range(1, n + 1):
            for j2 in range(j1 + 1, n + 1):
                clauses += [[-get_s(i, j1), -get_s(i, j2)]]

    for i in range(1, k + 1):
        lol = []
        for j in range(1, n + 1):
            lol += [get_s(i, j)]
        clauses += [lol]

    return clauses, 'kn'
