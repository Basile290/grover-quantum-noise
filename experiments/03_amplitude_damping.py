from qiskit import transpile
from qiskit_aer import AerSimulator

import numpy as np
import matplotlib.pyplot as plt

from src.grover import grover_2q
from src.noise_models import amplitude_damping_noise_model


# ============================================================
# PARAMÈTRES
# ============================================================

shots = 2000
seeds = range(10)

tau_values = np.linspace(0, 4, 30)

targets = ["00", "01", "10", "11"]

basis_gates = ["h", "x", "t", "tdg", "cx"]


# ============================================================
# CIRCUITS
# ============================================================

compiled_circuits = {}

for target in targets:

    qc = grover_2q(
        nb_iterations=1,
        target=target
    )

    compiled_circuits[target] = transpile(
        qc,
        basis_gates=basis_gates,
        optimization_level=0
    )


# ============================================================
# SIMULATION
# ============================================================

probabilities = {
    target: []
    for target in targets
}

standard_deviations = {
    target: []
    for target in targets
}


for tau in tau_values:

    noise_model = amplitude_damping_noise_model(tau)

    simulator = AerSimulator(
        noise_model=noise_model
    )

    for target in targets:

        results = []

        for seed in seeds:

            result = simulator.run(
                compiled_circuits[target],
                shots=shots,
                seed_simulator=seed
            ).result()

            counts = result.get_counts()

            p_success = (
                counts.get(target, 0) / shots
            )

            results.append(p_success)

        probabilities[target].append(
            np.mean(results)
        )

        standard_deviations[target].append(
            np.std(results)
        )


# ============================================================
# GRAPHIQUE
# ============================================================

for target in targets:

    plt.errorbar(
        tau_values,
        probabilities[target],
        yerr=standard_deviations[target],
        marker="o",
        markersize=3,
        capsize=2,
        label=rf"Cible $|{target}\rangle$"
    )


plt.xlabel(r"$\tau = t_{\mathrm{gate}}/T_1$")
plt.ylabel("Probabilité de succès")

plt.title(
    r"Grover 2 qubits sous relaxation énergétique $T_1$"
)

plt.ylim(0, 1.05)

plt.grid(alpha=0.4)
plt.legend()
plt.tight_layout()

plt.savefig(
    "figures/amplitude_damping_targets.png",
    dpi=300
)

plt.show()