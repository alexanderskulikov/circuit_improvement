from core.circuit_improvement import improve_single_circuit

improve_single_circuit(
    input_path='circuits/saved/maj15_size114_aig.bench',
    output_path='circuits/maj15_size114_aig_improved.bench',
    speed=15,
    global_time_limit=6
)

