from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

import numpy as np
import matplotlib.pyplot as plt

from src.grover import grover_2q


# ============================================================
# PARAMÈTRES
# ============================================================

shots = 4000
seeds = range(10)

p_values = np.linspace(0, 0.15, 15)

probabilities_1q = []
probabilities_2q = []

std_1q = []
std_2q = []


# ============================================================
# CIRCUIT
# ============================================================

qc = grover_2q(nb_iterations=1)

basis_gates = ["h", "x", "cz"]

compiled = transpile(
    qc,
    basis_gates=basis_gates,
    optimization_level=0
)


# ============================================================
# SIMULATION
# ============================================================

for p in p_values:

    results_1q = []
    results_2q = []

    # --------------------------
    # Bruit uniquement sur 1q
    # --------------------------

    noise_1q = NoiseModel()

    noise_1q.add_all_qubit_quantum_error(
        depolarizing_error(p, 1),
        ["h", "x"]
    )

    simulator_1q = AerSimulator(
        noise_model=noise_1q
    )

    # --------------------------
    # Bruit uniquement sur 2q
    # --------------------------

    noise_2q = NoiseModel()

    noise_2q.add_all_qubit_quantum_error(
        depolarizing_error(p, 2),
        ["cz"]
    )

    simulator_2q = AerSimulator(
        noise_model=noise_2q
    )

    # --------------------------
    # Plusieurs seeds
    # --------------------------

    for seed in seeds:

        result_1q = simulator_1q.run(
            compiled,
            shots=shots,
            seed_simulator=seed
        ).result()

        counts_1q = result_1q.get_counts()

        results_1q.append(
            counts_1q.get("11", 0) / shots
        )


        result_2q = simulator_2q.run(
            compiled,
            shots=shots,
            seed_simulator=seed
        ).result()

        counts_2q = result_2q.get_counts()

        results_2q.append(
            counts_2q.get("11", 0) / shots
        )


    probabilities_1q.append(
        np.mean(results_1q)
    )

    probabilities_2q.append(
        np.mean(results_2q)
    )

    std_1q.append(
        np.std(results_1q)
    )

    std_2q.append(
        np.std(results_2q)
    )


# ============================================================
# CONVERSION EN ARRAYS
# ============================================================

probabilities_1q = np.array(probabilities_1q)
probabilities_2q = np.array(probabilities_2q)

std_1q = np.array(std_1q)
std_2q = np.array(std_2q)


# ============================================================
# GRAPHIQUE
# ============================================================

plt.errorbar(
    p_values,
    probabilities_1q,
    yerr=std_1q,
    marker="o",
    markersize=4,
    capsize=3,
    label="Bruit sur les portes 1 qubit"
)

plt.errorbar(
    p_values,
    probabilities_2q,
    yerr=std_2q,
    marker="s",
    markersize=4,
    capsize=3,
    label="Bruit sur les portes 2 qubits"
)

plt.xlabel("Probabilité de dépolarisation par porte")
plt.ylabel(r"Probabilité de succès $P(|11\rangle)$")

plt.title("Grover 2 qubits sous bruit dépolarisant")

plt.ylim(0, 1.05)

plt.grid(alpha=0.4)
plt.legend()
plt.tight_layout()

plt.savefig(
    "figures/depolarizing_noise.png",
    dpi=300
)

plt.show()