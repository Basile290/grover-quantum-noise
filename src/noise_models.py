import numpy as np

from qiskit_aer.noise import (
    NoiseModel,
    depolarizing_error,
    amplitude_damping_error,
    phase_damping_error
)


# ============================================================
# BRUIT DÉPOLARISANT
# ============================================================

def depolarizing_noise_model(p1, p2):
    """
    Construit un modèle de bruit dépolarisant.

    p1 : paramètre de dépolarisation des portes 1 qubit
    p2 : paramètre de dépolarisation des portes 2 qubits
    """

    noise_model = NoiseModel()

    error_1q = depolarizing_error(p1, 1)
    error_2q = depolarizing_error(p2, 2)

    noise_model.add_all_qubit_quantum_error(
        error_1q,
        ["h", "x", "t", "tdg"]
    )

    noise_model.add_all_qubit_quantum_error(
        error_2q,
        ["cx"]
    )

    return noise_model


# ============================================================
# RELAXATION ÉNERGÉTIQUE T1
# ============================================================

def amplitude_damping_noise_model(tau):
    """
    Modèle simplifié de relaxation énergétique.

    tau = t_gate / T1

    On suppose ici que toutes les portes ont la même
    durée effective.
    """

    gamma_1 = 1 - np.exp(-tau)

    error_1q = amplitude_damping_error(gamma_1)
    error_2q = error_1q.tensor(error_1q)

    noise_model = NoiseModel()

    noise_model.add_all_qubit_quantum_error(
        error_1q,
        ["h", "x", "t", "tdg"]
    )

    noise_model.add_all_qubit_quantum_error(
        error_2q,
        ["cx"]
    )

    return noise_model


# ============================================================
# DÉPHASAGE PUR T_phi
# ============================================================

def dephasing_noise_model(tau_phi):
    """
    Modèle de déphasage pur.

    tau_phi = t_gate / T_phi

    Pour phase_damping_error :
        gamma_phi = 1 - exp(-2 tau_phi)
    """

    gamma_phi = 1 - np.exp(-2 * tau_phi)

    error_1q = phase_damping_error(gamma_phi)
    error_2q = error_1q.tensor(error_1q)

    noise_model = NoiseModel()

    noise_model.add_all_qubit_quantum_error(
        error_1q,
        ["h", "x", "t", "tdg"]
    )

    noise_model.add_all_qubit_quantum_error(
        error_2q,
        ["cx"]
    )

    return noise_model


# ============================================================
# RELAXATION + DÉPHASAGE
# ============================================================

def combined_noise_model(tau, ratio_Tphi_T1=1.0):
    """
    Combine relaxation énergétique et déphasage pur.

    tau = t_gate / T1

    ratio_Tphi_T1 = T_phi / T1

    Par défaut :
        T_phi = T1

    donc :
        gamma_1   = 1 - exp(-tau)
        gamma_phi = 1 - exp(-2 tau)
    """

    gamma_1 = 1 - np.exp(-tau)

    tau_phi = tau / ratio_Tphi_T1
    gamma_phi = 1 - np.exp(-2 * tau_phi)

    relaxation = amplitude_damping_error(gamma_1)
    dephasing = phase_damping_error(gamma_phi)

    error_1q = relaxation.compose(dephasing)
    error_2q = error_1q.tensor(error_1q)

    noise_model = NoiseModel()

    noise_model.add_all_qubit_quantum_error(
        error_1q,
        ["h", "x", "t", "tdg"]
    )

    noise_model.add_all_qubit_quantum_error(
        error_2q,
        ["cx"]
    )

    return noise_model