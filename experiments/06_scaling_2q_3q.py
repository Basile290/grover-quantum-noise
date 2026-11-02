from qiskit import transpile
from qiskit_aer import AerSimulator

import numpy as np
import matplotlib.pyplot as plt

from src.grover import grover_2q, grover_3q
from src.noise_models import (
    amplitude_damping_noise_model,
    combined_noise_model
)


# ============================================================
# PARAMÈTRES
# ============================================================

shots = 2000
seeds = range(10)

# On se concentre ici sur la zone de faible bruit,
# où la dégradation du circuit 3q est particulièrement visible.
tau_values = np.linspace(0, 0.1, 25)

basis_gates = ["h", "x", "t", "tdg", "cx"]

P_IDEAL_2Q = 1.0
P_IDEAL_3Q = 121 / 128

# ============================================================
# CIRCUITS
# ============================================================

qc_2q = grover_2q(
    nb_iterations=1,
    target="11"
)

qc_3q = grover_3q(
    nb_iterations=2
)


compiled_2q = transpile(
    qc_2q,
    basis_gates=basis_gates,
    optimization_level=0
)

compiled_3q = transpile(
    qc_3q,
    basis_gates=basis_gates,
    optimization_level=0
)


print("=== CIRCUIT 2 QUBITS ===")
print("Portes :", compiled_2q.count_ops())
print("Profondeur :", compiled_2q.depth())

print()

print("=== CIRCUIT 3 QUBITS ===")
print("Portes :", compiled_3q.count_ops())
print("Profondeur :", compiled_3q.depth())

# ============================================================
# FONCTION DE SIMULATION
# ============================================================

def run_noise_experiment(noise_function):

    probabilities_2q = []
    probabilities_3q = []

    std_2q = []
    std_3q = []

    for tau in tau_values:

        noise_model = noise_function(tau)

        simulator = AerSimulator(
            noise_model=noise_model
        )

        results_2q = []
        results_3q = []

        for seed in seeds:

            # --------------------------
            # 2 qubits
            # --------------------------

            result_2q = simulator.run(
                compiled_2q,
                shots=shots,
                seed_simulator=seed
            ).result()

            counts_2q = result_2q.get_counts()

            results_2q.append(
                counts_2q.get("11", 0) / shots
            )


            # --------------------------
            # 3 qubits
            # --------------------------

            result_3q = simulator.run(
                compiled_3q,
                shots=shots,
                seed_simulator=seed
            ).result()

            counts_3q = result_3q.get_counts()

            results_3q.append(
                counts_3q.get("111", 0) / shots
            )


        probabilities_2q.append(
            np.mean(results_2q)
        )

        probabilities_3q.append(
            np.mean(results_3q)
        )

        std_2q.append(
            np.std(results_2q)
        )

        std_3q.append(
            np.std(results_3q)
        )


    return (
        np.array(probabilities_2q),
        np.array(probabilities_3q),
        np.array(std_2q),
        np.array(std_3q)
    )
    
    
# ============================================================
# EXPÉRIENCE 1 : RELAXATION T1
# ============================================================

p2_T1, p3_T1, std2_T1, std3_T1 = (
    run_noise_experiment(
        amplitude_damping_noise_model
    )
)


relative_2q_T1 = p2_T1 / P_IDEAL_2Q
relative_3q_T1 = p3_T1 / P_IDEAL_3Q

relative_std2_T1 = std2_T1 / P_IDEAL_2Q
relative_std3_T1 = std3_T1 / P_IDEAL_3Q


plt.errorbar(
    tau_values,
    relative_2q_T1,
    yerr=relative_std2_T1,
    marker="o",
    markersize=3,
    capsize=2,
    label="Grover 2 qubits"
)

plt.errorbar(
    tau_values,
    relative_3q_T1,
    yerr=relative_std3_T1,
    marker="s",
    markersize=3,
    capsize=2,
    label="Grover 3 qubits"
)

plt.xlabel(
    r"$\tau=t_{\mathrm{gate}}/T_1$"
)

plt.ylabel(
    r"Performance relative $P/P_{\mathrm{ideal}}$"
)

plt.title(
    r"Passage de 2 à 3 qubits sous relaxation $T_1$"
)

plt.ylim(0, 1.05)

plt.grid(alpha=0.4)
plt.legend()
plt.tight_layout()

plt.savefig(
    "figures/scaling_T1.png",
    dpi=300
)

plt.show()

# ============================================================
# EXPÉRIENCE 2 : T1 + T_phi
# ============================================================

p2_combined, p3_combined, std2_combined, std3_combined = (
    run_noise_experiment(
        combined_noise_model
    )
)


relative_2q_combined = (
    p2_combined / P_IDEAL_2Q
)

relative_3q_combined = (
    p3_combined / P_IDEAL_3Q
)

relative_std2_combined = (
    std2_combined / P_IDEAL_2Q
)

relative_std3_combined = (
    std3_combined / P_IDEAL_3Q
)


plt.errorbar(
    tau_values,
    relative_2q_combined,
    yerr=relative_std2_combined,
    marker="o",
    markersize=3,
    capsize=2,
    label="Grover 2 qubits", color = "navy"
)

plt.errorbar(
    tau_values,
    relative_3q_combined,
    yerr=relative_std3_combined,
    marker="s",
    markersize=3,
    capsize=2,
    label="Grover 3 qubits", color = "red"
)

plt.xlabel(
    r"$\tau=t_{\mathrm{gate}}/T_1$"
)

plt.ylabel(
    r"Performance relative $P/P_{\mathrm{ideal}}$"
)

plt.title(
    r"Passage de 2 à 3 qubits sous bruit $T_1 + T_\phi$"
)

plt.ylim(0, 1.05)

plt.grid(alpha=0.4)
plt.legend()
plt.tight_layout()

plt.savefig(
    "figures/scaling_T1_Tphi.png",
    dpi=300
)

plt.show()