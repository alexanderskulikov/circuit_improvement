from pathlib import Path

from core.circuit import Circuit

circuits_dir = Path('/home/vsevolod/sat/circuit_improvement/experiments/circuits')
out_dir = Path('/home/vsevolod/sat/circuit_improvement/experiments/zhegalkin_polynomials')


def analyse_circuit(circuit: Circuit, out_file):
    def print2(s):
        if len(s) > 300:
            s = f"{s[:300]}..."
        print(s, file=out_file)
        print(f"\t{s}")

    polynomials = circuit.get_zhegalkin_polynomials()
    for gate in circuit.outputs:
        polynomial = polynomials[gate]
        if polynomial.is_monom():
            print2(f"{gate}: monom: {polynomial}")
        elif polynomial.is_linear():
            print2(f"{gate}: linear: {polynomial}")
        elif polynomial.is_common_inputs_and_linear():
            print2(f"{gate}: common inputs and linear: {polynomial.common_inputs()}")
        elif len((common_inputs := polynomial.common_inputs())) != 0:
            print2(f"{gate}: common inputs: {common_inputs} {polynomial}")

    print(file=out_file)
    for gate in circuit.gates:
        print(f"{gate}: {polynomials[gate]}", file=out_file)


def main():
    for entry in sorted(circuits_dir.iterdir(), key=lambda x: int(x.stem[2:4])):
        if not entry.is_file():
            continue
        print(f"{entry.name}:")
        circuit = Circuit()
        circuit.load_from_file(entry.stem, 'bench')
        with (out_dir / entry.stem).open('w') as f:
            analyse_circuit(circuit, f)


if __name__ == "__main__":
    main()
