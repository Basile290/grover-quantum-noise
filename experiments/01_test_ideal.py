from qiskit import transpile
from qiskit_aer import AerSimulator

from src.grover import grover_2q, grover_3q


shots = 10000
simulator = AerSimulator()


# ============================================================
# GROVER 2 QUBITS
# ============================================================

qc_2q = grover_2q()

compiled_2q = transpile(
    qc_2q,
    simulator
)

result_2q = simulator.run(
    compiled_2q,
    shots=shots,
    seed_simulator=42
).result()

counts_2q = result_2q.get_counts()

p_2q = counts_2q.get("11", 0) / shots


# ============================================================
# GROVER 3 QUBITS
# ============================================================

qc_3q = grover_3q()

compiled_3q = transpile(
    qc_3q,
    simulator
)

result_3q = simulator.run(
    compiled_3q,
    shots=shots,
    seed_simulator=42
).result()

counts_3q = result_3q.get_counts()

p_3q = counts_3q.get("111", 0) / shots


# ============================================================
# RÉSULTATS
# ============================================================

print("Grover 2 qubits")
print(counts_2q)
print("P(|11>) =", p_2q)

print()

print("Grover 3 qubits")
print(counts_3q)
print("P(|111>) =", p_3q)