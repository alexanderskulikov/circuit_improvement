import time
from os import walk

import pycosat
from pysat.card import *
from pysat.solvers import Solver

from clique_sat_representations import clique_n2
from clique_sat_representations import clique_n2_th20n
from clique_sat_representations import clique_n2_th18n
from clique_sat_representations import clique_kn


def load_from_file(file_name):
    edges = {}
    with open('benchmarks/' + file_name) as matrix_file:
        lines = matrix_file.read().splitlines()
        n, k, clique_size = list(map(int, lines[0].strip().split()))
        for i in range(k):
            a, b = lines[i + 1].strip().split()
            a = int(a)
            b = int(b)
            edges[(min(a, b), max(a, b))] = 1
    return n, clique_size, edges


def run_solver(clauses, solver_name):
    timing = time.time()
    sat_result = 'SAT'
    if solver_name == 'pycosat':
        result = pycosat.solve(clauses)
        if result == 'UNSAT':
            sat_result = 'UNSAT'
    else:
        f1 = CNF(from_file='clique.cnf')
        s = Solver(name=solver_name)
        s.append_formula(f1.clauses)
        s.solve()
        result = s.get_model()
        if result is None:
            sat_result = 'UNSAT'
    return sat_result, round(time.time() - timing, 2)


def run(solver_name, benchmark_name, clique_repres, isUNSAT):
    n, k, edges = load_from_file(benchmark_name)
    if isUNSAT:
        k = k + 1
    clauses, method_info = clique_repres(n, k, edges)
    result, current_time = run_solver(clauses, solver_name)
    print(f'{method_info},{benchmark_name},{solver_name},{len(clauses)},{current_time},{result}')


if __name__ == '__main__':
    # solver_name = 'mcb'
    solver_name = 'pycosat'
    _, _, benchmarks = next(walk('benchmarks'))
    benchmarks.sort()
    for benchmark in benchmarks:
        if benchmark == 'hamming6-4.mtx':
        #run(solver_name, benchmark, clique_repres=clique_n2, isUNSAT=False)
        #run(solver_name, benchmark, clique_repres=clique_n2_th20n, isUNSAT=True)
        #run(solver_name, benchmark, clique_repres=clique_n2_th18n, isUNSAT=True)
            run(solver_name, benchmark, clique_repres=clique_kn, isUNSAT=False)
