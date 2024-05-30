from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import List, Dict, Any
from tqdm import tqdm

from core.circuit import Circuit
from core.zhegalkin_polynomial import ZhegalkinTree, ZhegalkinPolynomial

circuits_dir = Path('/home/vsevolod/sat/circuit_improvement/experiments/circuits')
out_dir = Path('/home/vsevolod/sat/circuit_improvement/experiments/zhegalkin_polynomials')


def get_size(circuit: Circuit) -> int:
    circuit.normalize('xaig')
    size = len(list(filter(lambda x: x[-1] not in ('1100', '1010'), circuit.gates.values())))
    return size


def compare_circuits(ckt1: Circuit, ckt2: Circuit):
    all_tt_1 = ckt1.get_truth_tables()
    all_tt_2 = ckt2.get_truth_tables()
    tt_1 = [all_tt_1[i] for i in ckt1.outputs]
    tt_2 = [all_tt_2[i] for i in ckt2.outputs]
    assert len(tt_1) == len(tt_2)
    for i in range(len(tt_1)):
        assert tt_1[i] == tt_2[i], f"{i}:\n\t{tt_1[i]}\n\t{tt_2[i]}"


def analyze_polynomials(ckt: Circuit, poly: Dict[Any, ZhegalkinPolynomial], print2, out_file):
    print("Analyzing polynomials...")
    for gate in ckt.outputs:
        polynomial = poly[gate]
        if polynomial.is_monom():
            print2(f"{gate}: monom: {polynomial}")
        elif polynomial.is_linear():
            print2(f"{gate}: linear: {polynomial}")
        elif polynomial.is_common_inputs_and_linear():
            print2(f"{gate}: common inputs and linear: {polynomial.common_inputs()}")
        elif len((common_inputs := polynomial.common_inputs())) != 0:
            print2(f"{gate}: common inputs: {common_inputs} {polynomial}")

    print(file=out_file)
    for gate in ckt.gates:
        print(f"{gate}: {poly[gate]}", file=out_file)


def analyse_circuit(baseline_circuit: Circuit, out_file, circuit_name: str):
    def print2(s):
        if len(s) > 300:
            s = f"{s[:300]}..."
        print(s, file=out_file)
        print(f"\t{s}")

    baseline_size = get_size(baseline_circuit)
    print(f"Baseline size: {baseline_size}")

    # analyze polynomials
    polynomials = baseline_circuit.get_zhegalkin_polynomials()
    analyze_polynomials(baseline_circuit, polynomials, print2, out_file)
    out_polynomials = [polynomials[i] for i in baseline_circuit.outputs]
    if sum(len(x.monomials) for x in out_polynomials) > 1000:
        print("Skip because of the size")
        return
    # analyze trivial circuit
    trivial_circuit = Circuit(baseline_circuit.input_labels)
    trivial_circuit.add_zhegalkin_polynomials(out_polynomials, add_outputs=True)
    compare_circuits(baseline_circuit, trivial_circuit)
    trivial_size = get_size(trivial_circuit)
    print(f"Trivial size: {trivial_size}")
    trivial_circuit.save_to_file(file_name=f"zhegalkin_{circuit_name}", extension='bench')

    # analyze optimized circuit
    # print("")
    # zhegalkin_trees = [ZhegalkinTree.simplest_optimized_polynomial(p) for p in out_polynomials]
    # simplest_optimized_circuit = Circuit(baseline_circuit.input_labels)
    # simplest_optimized_circuit.add_zhegalkin_trees(zhegalkin_trees, add_outputs=True)
    # compare_circuits(baseline_circuit, simplest_optimized_circuit)
    # simplest_optimized_size = get_size(simplest_optimized_circuit)
    # print(f"Simplest optimized size: {simplest_optimized_size}")
    # simplest_optimized_circuit.save_to_file(file_name=f"zhegalkin_optimized_{circuit_name}", extension='bench')


def analyze_file(entry):
    print(f"{entry.name}:")
    circuit = Circuit()
    circuit.load_from_file(entry.stem, 'bench')
    with (out_dir / entry.stem).open('w') as f:
        analyse_circuit(circuit, f, entry.stem)
    return entry.stem

# "66" "14" "23_2" "19" "49" "60" "82" "59" "13" "66_2" "63" "94" "16" "03_2" "19" "03" "80" "55" "72" "23"
def main():
    files = list(sorted(filter(lambda x: x.stem[0] != 'z', circuits_dir.iterdir()), key=lambda x: int(x.stem[2:4])))
    with ProcessPoolExecutor(max_workers=4) as pool:
        tasks = []
        for entry in tqdm(files, desc="Task submission"):
            if not entry.is_file():
                continue
            future = pool.submit(analyze_file, entry)

            tasks.append(future)
        for future in tqdm(as_completed(tasks), total=len(tasks), desc="Waiting"):
            print(f"Analyzed: {future.result()}")


if __name__ == "__main__":
    main()
