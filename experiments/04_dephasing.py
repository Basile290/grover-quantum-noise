from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

import numpy as np
import matplotlib.pyplot as plt

from src.grover import grover_2q
from src.noise_models import dephasing_noise_model


# ============================================================
# PARAMÈTRES
# ============================================================

shots = 2000
seeds = range(10)

tau_values = np.linspace(0, 4, 30)

basis_gates = ["h", "x", "t", "tdg", "cx"]


# ============================================================
# 1. VALIDATION DU DÉPHASAGE SUR |+>
# ============================================================

qc_test = QuantumCircuit(1)

# |0> -> |+>
qc_test.h(0)

# Permet de convertir la cohérence en population mesurable
qc_test.h(0)

qc_test.measure_all()

compiled_test = transpile(
    qc_test,
    basis_gates=basis_gates,
    optimization_level=0
)


probabilities_test = []
std_test = []


for tau_phi in tau_values:

    noise_model = dephasing_noise_model(tau_phi)

    simulator = AerSimulator(
        noise_model=noise_model
    )

    results = []

    for seed in seeds:

        result = simulator.run(
            compiled_test,
            shots=shots,
            seed_simulator=seed
        ).result()

        counts = result.get_counts()

        results.append(
            counts.get("0", 0) / shots
        )

    probabilities_test.append(
        np.mean(results)
    )

    std_test.append(
        np.std(results)
    )


probabilities_test = np.array(probabilities_test)
std_test = np.array(std_test)


# Théorie
#
# gamma_phi = 1 - exp(-2 tau_phi)
#
# donc :
# sqrt(1 - gamma_phi) = exp(-tau_phi)
#
# et :
# P(0) = (1 + exp(-tau_phi))/2

theory_test = (
    1 + np.exp(-tau_values)
) / 2


# ============================================================
# FIGURE 1 : VALIDATION
# ============================================================

plt.plot(
    tau_values,
    theory_test,
    linestyle="--",
    label=r"Théorie : $(1+e^{-\tau_\phi})/2$"
)

plt.errorbar(
    tau_values,
    probabilities_test,
    yerr=std_test,
    marker="o",
    markersize=3,
    capsize=2,
    linestyle="none",
    label="Simulation"
)

plt.xlabel(
    r"$\tau_\phi = t_{\mathrm{gate}}/T_\phi$"
)

plt.ylabel(
    r"Probabilité $P(0)$"
)

plt.title(
    "Validation du modèle de déphasage"
)

plt.ylim(0, 1.05)

plt.grid(alpha=0.4)
plt.legend()
plt.tight_layout()

plt.savefig(
    "figures/dephasing_validation.png",
    dpi=300
)

plt.show()


# ============================================================
# 2. DÉPHASAGE SUR GROVER
# ============================================================

targets = ["00", "01", "10", "11"]

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


probabilities = {
    target: []
    for target in targets
}

standard_deviations = {
    target: []
    for target in targets
}


for tau_phi in tau_values:

    noise_model = dephasing_noise_model(
        tau_phi
    )

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

            results.append(
                counts.get(target, 0) / shots
            )

        probabilities[target].append(
            np.mean(results)
        )

        standard_deviations[target].append(
            np.std(results)
        )


# ============================================================
# FIGURE 2 : GROVER
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


plt.axhline(
    0.25,
    linestyle="--",
    label=r"Limite $1/4$"
)

plt.xlabel(
    r"$\tau_\phi = t_{\mathrm{gate}}/T_\phi$"
)

plt.ylabel(
    "Probabilité de succès"
)

plt.title(
    "Grover 2 qubits sous déphasage pur"
)

plt.ylim(0, 1.05)

plt.grid(alpha=0.4)
plt.legend()
plt.tight_layout()

plt.savefig(
    "figures/dephasing_grover.png",
    dpi=300
)

plt.show()