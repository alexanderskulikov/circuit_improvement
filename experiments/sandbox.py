from core.circuit_improvement import improve_single_circuit

improve_single_circuit(
    input_path='circuits/ex113.bench',
    output_path='circuits/maj15_size114_aig_improved.bench',
    speed='easy',
    global_time_limit=6
)

