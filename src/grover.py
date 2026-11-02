from qiskit import QuantumCircuit


# ============================================================
# GROVER 2 QUBITS
# ============================================================

def oracle_2q(qc, target="11"):
    """
    Oracle de Grover pour 2 qubits.

    target peut être :
        "00", "01", "10" ou "11"
    """

    if target == "00":
        qc.x(0)
        qc.x(1)
        qc.cz(0, 1)
        qc.x(0)
        qc.x(1)

    elif target == "01":
        qc.x(1)
        qc.cz(0, 1)
        qc.x(1)

    elif target == "10":
        qc.x(0)
        qc.cz(0, 1)
        qc.x(0)

    elif target == "11":
        qc.cz(0, 1)

    else:
        raise ValueError(
            "target doit être '00', '01', '10' ou '11'"
        )


def diffusion_2q(qc):
    """Opérateur de diffusion de Grover pour 2 qubits."""

    qc.h(0)
    qc.h(1)

    qc.x(0)
    qc.x(1)

    qc.cz(0, 1)

    qc.x(0)
    qc.x(1)

    qc.h(0)
    qc.h(1)


def grover_2q(nb_iterations=1, target="11"):
    """
    Construit un circuit de Grover à 2 qubits
    recherchant l'état target.
    """

    qc = QuantumCircuit(2)

    qc.h(0)
    qc.h(1)

    for _ in range(nb_iterations):
        oracle_2q(qc, target)
        diffusion_2q(qc)

    qc.measure_all()

    return qc


# ============================================================
# GROVER 3 QUBITS
# ============================================================

def ccz(qc):
    """
    Réalise une porte CCZ à partir d'une CCX.

    CCZ = H - CCX - H
    sur le troisième qubit.
    """

    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)


def oracle_3q(qc):
    """
    Oracle marquant l'état |111>.
    """

    ccz(qc)


def diffusion_3q(qc):
    """
    Opérateur de diffusion de Grover pour 3 qubits.
    """

    # H sur les trois qubits
    for q in range(3):
        qc.h(q)

    # X sur les trois qubits
    for q in range(3):
        qc.x(q)

    # Réflexion de phase
    ccz(qc)

    # Retour
    for q in range(3):
        qc.x(q)

    for q in range(3):
        qc.h(q)


def grover_3q(nb_iterations=2):
    """
    Construit un circuit de Grover à 3 qubits
    recherchant l'état |111>.
    """

    qc = QuantumCircuit(3)

    # Superposition uniforme
    for q in range(3):
        qc.h(q)

    # Itérations de Grover
    for _ in range(nb_iterations):
        oracle_3q(qc)
        diffusion_3q(qc)

    qc.measure_all()

    return qc