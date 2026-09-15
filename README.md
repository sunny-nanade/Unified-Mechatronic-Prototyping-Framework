# Unified First-Principles & Numerical Simulation Framework for Rapid Mechatronic Prototyping

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Journal: MDPI Designs](https://img.shields.io/badge/Journal-MDPI%20Designs%20(Q1%2C%20CiteScore%205.7)-orange.svg)](https://www.mdpi.com/journal/designs)
[![Collection: Mechatronic System Design](https://img.shields.io/badge/Collection-Mechatronic%20System%20Design-purple.svg)](https://www.mdpi.com/journal/designs/topical_collections/Mechatronic_System_Design)

Official open-access replication codebase, dynamic models, mathematical catalogs, and benchmark datasets for:

> **"A Unified First-Principles and Numerical Simulation Framework for Rapid Mechatronic System Prototyping: Dynamic Modeling and Validation Across Heterogeneous Architectures"**  
> **Authors:** Dr. Sunny Nanade (Corresponding Author) and Dr. Koteswararao Anne  
> **Affiliation:** SVKM's NMIMS Mukesh Patel School of Technology Management & Engineering, Mumbai 400056, India  
> **Journal:** *Designs* (ISSN 2411-9660) — Special Issue / Topical Collection: *Mechatronic System Design*  
> **Manuscript ID:** `designs-4596903`

---

## 🔬 Framework Overview

Bridging the disconnect between conceptual kinematic design and high-fidelity multi-physics hardware execution remains a central challenge in mechatronic development, frequently necessitating costly, empirical trial-and-error prototyping iterations. 

This repository provides an open-source, reproducible Model-Based Systems Engineering (MBSE) framework that formalizes multi-body dynamics into a canonical second-order matrix representation, maps systems into continuous state space, enforces **four deterministic simulation verification gates**, and benchmarks simulations against physical sensor telemetry across **17 heterogeneous mechatronic architectures**.

```
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │                     UNIFIED MBSE VERIFICATION PIPELINE                      │
   └─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │ 1. KINEMATIC & DYNAMIC FORMULATION                                          │
   │    • Euler-Lagrange / Newton-Euler / Appell formulations                    │
   │    • Canonical 2nd-Order Dynamics: M(q)q̈ + C(q,q̇)q̇ + G(q) + F_f = B_u u     │
   │    • Christoffel skew-symmetry: z^T(Ṁ - 2C)z = 0                            │
   └─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │ 2. STATE-SPACE MAPPING & NUMERICAL INTEGRATION                              │
   │    • Explicit Dormand-Prince (RK45) / Implicit Stiff Radau-IIA              │
   │    • Adaptive step control with step size limiting                          │
   └─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │ 3. DETERMINISTIC FOUR-GATE VERIFICATION AUDIT                               │
   │    ├── Gate 1: Mechanical Energy Drift (ε_E < 10⁻⁴)                         │
   │    ├── Gate 2: Actuator Dynamic Torque Headroom (S_i ≥ 20%)                 │
   │    ├── Gate 3: Kinematic Singularity Clearance (σ_min(J) > 0)               │
   │    └── Gate 4: Spectral Hurwitz Asymptotic Stability (max Re(λ_i) < 0)      │
   └─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────────┐
   │ 4. THREE-TIER HARDWARE VALIDATION & SENSOR TELEMETRY                        │
   │    • Optical Encoders, 6-Axis IMUs, Laser Displacement, Hall Transducers    │
   │    • Metrics: NMAE ≤ 4.82%, R² ≥ 0.9924, Sub-10 ms real-time solve times   │
   │    • Prototyping Lifecycle: 76.19% cycle reduction, >68% CapEx reduction    │
   └─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ The Four Deterministic Verification Gates

Before committing physical capital to machining, additive manufacturing, or printed circuit fabrication, each mechatronic system must pass four quantitative simulation gates:

1. **Gate 1 — Conservation of Mechanical Energy:**
   $$\varepsilon_E = \max_{t \in [0, T]} \frac{|E(t) - E(0)|}{E(0)} < 10^{-4}$$
   For non-conservative (dissipative/actuated) systems, the instantaneous power residual $\varepsilon_P(t) = |\dot{E}(t) - P_{\text{in}}(t) + P_{\text{diss}}(t)| \le 2.0 \times 10^{-2}\text{ W}$.

2. **Gate 2 — Actuator Torque Headroom & Saturation Avoidance:**
   $$S_i = 1 - \frac{\max_{t \in [0, T]} |\tau_{m,i}(t)|}{\tau_{\text{peak},i}} \ge 20\% \quad \forall i \in \{1, \dots, m\}$$

3. **Gate 3 — Kinematic Singularity & Operational Margin:**
   $$\sigma_{\min}(J(q)) \ge \sigma_{\text{threshold}} > 0, \quad w(q) = \sqrt{\det(J J^T)} > 0$$

4. **Gate 4 — Spectral Hurwitz Asymptotic Stability:**
   $$\max_{i} \operatorname{Re}(\lambda_i(A_{\text{cl}})) < 0$$

---

## 📊 Master Benchmark Matrix: 17 Heterogeneous Systems

The framework is validated across 17 diverse systems spanning 5 engineering domains:

| System ID | Mechatronic Architecture | Domain | DOF | Generalized Coordinates | Gate 1 Drift | Gate 2 Margin | Gate 3 Status | Gate 4 $\max\operatorname{Re}(\lambda)$ | RMSE | NMAE (%) | $R^2$ Score | Solve Time |
| :--- | :--- | :--- | :---: | :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **Sys_01** | 2-DOF Quadruped Pantograph Leg | Bio-Inspired Locomotion | 2 | $[\theta_1, \theta_2]^T$ | $4.20 \times 10^{-6}$ | 46.8% | $\det(J) \ge 0.024$ | -6.84 | 0.0142 | 2.84% | 0.9982 | 3.45 ms |
| **Sys_02** | 3-DOF Tripod Locomotion Hexapod | Bio-Inspired Locomotion | 3 | $[\alpha, \beta, \gamma]^T$ | $8.00 \times 10^{-5}$ | 53.3% | $\text{SSM} = 60.0\text{ mm}$ | -12.40 | 0.0071 | 0.98% | 0.9991 | 4.20 ms |
| **Sys_03** | 12-DOF 3D Bipedal Humanoid | Bio-Inspired Locomotion | 12 | $q \in \mathbb{R}^{12}$ | $9.50 \times 10^{-6}$ | 38.2% | $\text{ZMP Margin} = 32\text{ mm}$ | -8.15 | 0.0210 | 3.15% | 0.9945 | 8.50 ms |
| **Sys_04** | 6-DOF Stewart-Gough Platform | Parallel Manipulators | 6 | $[x, y, z, \phi, \theta, \psi]^T$ | $3.80 \times 10^{-6}$ | 42.8% | $\det(J) \ge 0.0105$ | -4.20 | 0.0158 | 4.82% | 0.9950 | 6.10 ms |
| **Sys_05** | Underactuated Compliant Gripper | Parallel Manipulators | 2 | $[x, \dot{x}, i]^T$ | $4.50 \times 10^{-3}$ | 95.0% | Safety Factor 193x | -10.91 | 0.0008 | 1.25% | 0.9984 | 2.85 ms |
| **Sys_06** | Autonomous Mobile Manipulator | Parallel Manipulators | 6 | $[x_b, y_b, \theta_b, \theta_1..\theta_3]^T$ | $8.20 \times 10^{-6}$ | 32.4% | Manipulability $w=0.18$ | -5.50 | 0.0180 | 2.10% | 0.9962 | 7.20 ms |
| **Sys_07** | Two-Wheeled Inverted Pendulum | Underactuated Stabilizers | 2 | $[x, \theta]^T$ | $5.20 \times 10^{-7}$ | 44.1% | Controllability Rank 4/4 | -4.85 | 0.0125 | 1.95% | 0.9978 | 3.90 ms |
| **Sys_08** | Critical Skid Vehicle Platform | Underactuated Stabilizers | 3 | $[u, v, r]^T$ | $7.40 \times 10^{-6}$ | 52.0% | $\text{SSF} = 1.78$ | -18.20 | 0.0472 | 2.46% | 0.9924 | 3.80 ms |
| **Sys_09** | Multi-Terrain Autonomous Rover | Underactuated Stabilizers | 2 | $[v_y, r]^T$ | $6.10 \times 10^{-6}$ | 46.8% | Hurwitz Stable | -120.00 | 0.0142 | 3.42% | 0.9965 | 4.10 ms |
| **Sys_10** | Thrust-Vectored Rocket Lander | Aerospace Dynamics | 3 | $[x, z, \theta]^T, m(t)$ | $8.40 \times 10^{-6}$ | 35.0% | Gimbal Limit $\pm 20^\circ$ | -3.20 | 0.0040 | 1.12% | 0.9989 | 5.90 ms |
| **Sys_11** | Hybrid Fuel-Cell UAV Powertrain | Aerospace Dynamics | 6 | $x \in \mathbb{R}^{22}$ | $1.56 \times 10^{-2}$ | 28.6% | Thrust Margin 34% | -5.10 | 0.0380 | 1.42% | 0.9972 | 9.80 ms |
| **Sys_12** | 6-DOF Underwater Oceanic ROV | Aerospace Dynamics | 6 | $\nu, \eta \in \mathbb{R}^6$ | $1.40 \times 10^{-4}$ | 24.8% | Metacentric $BG_z = +50\text{ mm}$ | -2.80 | 0.1840 | 1.84% | 0.9960 | 8.10 ms |
| **Sys_13** | Automated Gantry Crane Anti-Sway | Industrial Handling | 3 | $[x_t, l_c, \theta_s]^T$ | $7.80 \times 10^{-7}$ | 71.2% | Controllability Rank 6/6 | -1.04 | 0.0029 | 0.02% | 0.9998 | 4.75 ms |
| **Sys_14** | Quarter-Car Active Suspension | Industrial Handling | 2 | $[z_s, z_u]^T$ | $9.10 \times 10^{-7}$ | 38.5% | Bounce $\omega_{n1} = 8.5\text{ rad/s}$ | -8.50 | 0.0084 | 1.85% | 0.9975 | 3.80 ms |
| **Sys_15** | Dynamic Industrial Conveyor | Industrial Handling | 1 | $[\theta_d, x_L]^T, m_L(t)$ | $1.20 \times 10^{-6}$ | 36.6% | Capstan Grip Margin 2.4x | -14.20 | 0.0150 | 1.57% | 0.9980 | 4.20 ms |
| **Sys_16** | Multi-Actuator Electro-Mechanics | Industrial Handling | 3 | $[i_a, \omega, \theta]^T$ | $5.00 \times 10^{-7}$ | 48.2% | $\operatorname{Re}(\lambda) \le -50$ | -50.00 | 0.0140 | 0.84% | 0.9992 | 5.10 ms |
| **Sys_17** | Motor Thermal Digital Twin | Industrial Handling | 3 | $[i, \omega, \theta, T_s, T_r]^T$ | $2.80 \times 10^{-3}$ | 41.5% | Self-Healing Load Transfer | -6.20 | 0.0420 | 1.62% | 0.9970 | 6.30 ms |

---

## 🚀 Quickstart & Replication

### 1. Clone the Repository
```bash
git clone https://github.com/sunny-nanade/Unified-Mechatronic-Prototyping-Framework.git
cd Unified-Mechatronic-Prototyping-Framework
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Master Verification Testbench
To execute the multi-body dynamic solvers and reproduce the deterministic gate evaluation matrix:
```bash
python benchmarks/test_all_17_models.py
```
This generates the full `master_verification_matrix.csv` with 17 verified rows matching Table 3 of the manuscript.

### 4. Regenerate Publication Figures
```bash
python scripts/generate_all_figures.py
```

---

## 📁 Repository Structure

```
Unified-Mechatronic-Prototyping-Framework/
├── README.md                              # Main documentation and benchmark overview
├── LICENSE                                # Open-access MIT license
├── requirements.txt                       # Python dependencies
├── benchmarks/
│   ├── test_all_17_models.py              # Master multi-body verification engine
│   └── master_verification_matrix.csv     # Quantitative gate audit and telemetry metrics
├── catalogs/
│   ├── UNIFIED_17_SYSTEM_MATHEMATICAL_CATALOG.md  # Closed-form kinematic & dynamic equations
│   └── MASTER_NOMENCLATURE_DICTIONARY.md          # Unified parameter & state variable dictionary
├── figures/
│   ├── fig1_mbse_framework.png            # Model-Based Systems Engineering pipeline
│   ├── fig2_four_gates.png                # Four quantitative simulation verification gates
│   ├── fig3_state_telemetry.png           # Simulated vs. physical hardware telemetry tracking
│   ├── fig4_fft_residual.png              # Frequency spectrum and error residuals
│   ├── fig5_solver_stability.png          # Numerical convergence and solver step-size sweeps
│   └── fig6_prototype_economics.png       # Prototyping lifecycle iterations and cost reduction
└── scripts/
    └── generate_all_figures.py            # High-resolution (300 DPI) publication figure generator
```

---

## 📖 Citation

If you use this framework or benchmark dataset in your research, please cite:

```bibtex
@article{nanade2026unified,
  title={A Unified First-Principles and Numerical Simulation Framework for Rapid Mechatronic System Prototyping: Dynamic Modeling and Validation Across Heterogeneous Architectures},
  author={Nanade, Sunny and Anne, Koteswararao},
  journal={Designs},
  volume={--},
  number={--},
  pages={--},
  year={2026},
  publisher={MDPI},
  note={Manuscript ID: designs-4596903}
}
```

---

## ✉️ Correspondence
For questions or collaborations:  
**Dr. Sunny Nanade**  
Mukesh Patel School of Technology Management & Engineering, SVKM's NMIMS, Mumbai, India  
Email: `sunny.nanade@nmims.edu`
