from core.circuit_improvement import improve_single_circuit

improve_single_circuit(
    input_path='maj15_size114_aig.bench',
    output_file_name='maj15_size114_aig_improved.bench',
    speed=15,
    global_time_limit=60
)

