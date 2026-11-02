from src.noise_models import (
    depolarizing_noise_model,
    amplitude_damping_noise_model,
    dephasing_noise_model,
    combined_noise_model
)


noise_depolarizing = depolarizing_noise_model(
    p1=0.01,
    p2=0.03
)

noise_T1 = amplitude_damping_noise_model(
    tau=0.01
)

noise_Tphi = dephasing_noise_model(
    tau_phi=0.01
)

noise_combined = combined_noise_model(
    tau=0.01
)


print("Dépolarisation : OK")
print(noise_depolarizing)

print("\nT1 : OK")
print(noise_T1)

print("\nTphi : OK")
print(noise_Tphi)

print("\nT1 + Tphi : OK")
print(noise_combined)