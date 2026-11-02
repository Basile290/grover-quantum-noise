from qiskit import transpile
from qiskit_aer import AerSimulator

import numpy as np
import matplotlib.pyplot as plt

from src.grover import grover_3q


# ============================================================
# PARAMÈTRES
# ============================================================

shots = 8000
iterations = np.arange(9)

simulator = AerSimulator()

probabilities = []


# ============================================================
# SIMULATION
# ============================================================

for k in iterations:

    qc = grover_3q(nb_iterations=k)

    compiled = transpile(
        qc,
        simulator
    )

    result = simulator.run(
        compiled,
        shots=shots,
        seed_simulator=42
    ).result()

    counts = result.get_counts()

    p_success = counts.get("111", 0) / shots

    probabilities.append(p_success)


probabilities = np.array(probabilities)


# ============================================================
# THÉORIE
# ============================================================

theta = np.arcsin(1 / np.sqrt(8))

# Valeurs théoriques aux itérations entières
theoretical_probabilities = np.sin(
    (2 * iterations + 1) * theta
) ** 2

# Axe continu uniquement pour visualiser la fonction théorique
k_continu = np.linspace(0, 8, 500)

P_continu = np.sin(
    (2 * k_continu + 1) * theta
) ** 2


# ============================================================
# RÉSULTATS
# ============================================================

print("k   Simulation   Théorie")

for k, p_sim, p_theory in zip(
    iterations,
    probabilities,
    theoretical_probabilities
):
    print(
        f"{k:<3} {p_sim:.4f}       {p_theory:.4f}"
    )


plt.plot(
    k_continu,
    P_continu,
    linestyle="--",
    label=r"Théorie : $\sin^2((2k+1)\theta)$"
)

plt.scatter(
    iterations,
    probabilities,
    label="Simulation"
)

plt.xlabel("Nombre d'itérations de Grover")
plt.ylabel(r"Probabilité de mesurer $|111\rangle$")

plt.title("Grover idéal à 3 qubits")

plt.xticks(iterations)
plt.ylim(0, 1.05)

plt.grid(alpha=0.4)
plt.legend()
plt.tight_layout()

plt.savefig(
    "figures/grover_3q_iterations.png",
    dpi=300
)

plt.show()