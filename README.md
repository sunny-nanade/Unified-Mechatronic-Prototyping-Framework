# Unified Dynamic Modeling and Simulation Framework for Mechatronic System Prototyping

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Journal: MDPI Designs](https://img.shields.io/badge/Journal-MDPI%20Designs-orange.svg)](https://www.mdpi.com/journal/designs)

This repository contains the simulation models, verification scripts, and benchmark data accompanying the research paper:

> **"A Unified First-Principles and Numerical Simulation Framework for Rapid Mechatronic System Prototyping: Dynamic Modeling and Validation Across Heterogeneous Architectures"**  
> **Authors:** Dr. Sunny Nanade (Corresponding Author) and Dr. Koteswararao Anne  
> **Affiliation:** SVKM's NMIMS Mukesh Patel School of Technology Management & Engineering, Mumbai, India  
> **Journal:** *Designs* (Special Issue: Mechatronic System Design)  
> **Manuscript ID:** `designs-4596903`

---

## Overview

Developing mechatronic systems often involves physical trial-and-error iterations. This work presents a simulation framework based on first-principles dynamics to evaluate system behavior prior to hardware manufacturing. 

The framework formulates second-order equations of motion for multi-body systems, converts them to state-space representations, and applies four quantitative verification checks before comparing simulation results with sensor measurements from physical setups.

```
+-------------------------------------------------------------------------+
|                  Simulation and Verification Workflow                   |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| 1. Dynamic Formulation                                                  |
|    - Derive equations of motion: M(q)q'' + C(q,q')q' + G(q) = B u       |
|    - State-space conversion: x' = f(x, u, t)                            |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| 2. Numerical Integration                                                |
|    - Adaptive Runge-Kutta (RK45) and Radau-IIA stiff solvers            |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| 3. Four Verification Checks                                             |
|    - Gate 1: Energy balance and drift                                   |
|    - Gate 2: Actuator torque headroom (>= 20% margin)                   |
|    - Gate 3: Singularity avoidance                                      |
|    - Gate 4: Closed-loop stability (negative real eigenvalues)          |
+-------------------------------------------------------------------------+
                                     |
                                     v
+-------------------------------------------------------------------------+
| 4. Experimental Validation                                              |
|    - Comparison against encoders, IMUs, laser sensors, and current data |
|    - Tracking metrics across 17 systems: NMAE <= 4.82%, R^2 >= 0.9924   |
+-------------------------------------------------------------------------+
```

---

## Verification Checks

Before hardware fabrication, dynamic models are evaluated against four numerical criteria:

1. **Gate 1 - Mechanical Energy Balance:**  
   The relative drift in total mechanical energy for conservative motion satisfies:  
   `drift = max |E(t) - E(0)| / E(0) < 1.0e-4`  
   For non-conservative systems, the power residual between work input, dissipation, and kinetic/potential rate of change is monitored.

2. **Gate 2 - Actuator Torque Headroom:**  
   To prevent motor saturation during dynamic transients, a minimum margin of 20% is required:  
   `Margin = 1 - (max |tau(t)| / tau_peak) >= 20%`

3. **Gate 3 - Kinematic Singularity Clearance:**  
   Manipulator configurations are evaluated to ensure Jacobian matrices remain full rank and maintain distance from singular configurations (`det(J) > 0`).

4. **Gate 4 - Closed-Loop Stability:**  
   Linearized state matrices around operating equilibria are checked to ensure all closed-loop eigenvalues have negative real parts:  
   `max Re(lambda_i) < 0`

---

## Benchmark Systems and Results

The framework was tested on 17 mechatronic systems grouped into 5 application categories:

| System ID | System Name | Category | DOF | Coordinates | Gate 1 Drift | Gate 2 Margin | Gate 3 Status | Gate 4 Max Re(λ) | RMSE | NMAE (%) | R² | Solve Time |
| :--- | :--- | :--- | :---: | :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **Sys_01** | 2-DOF Quadruped Pantograph Leg | Bio-Inspired Locomotion | 2 | [θ₁, θ₂]ᵀ | 4.20e-06 | 46.8% | det(J) ≥ 0.024 | -6.84 | 0.0142 | 2.84% | 0.9982 | 3.45 ms |
| **Sys_02** | 3-DOF Tripod Locomotion Hexapod | Bio-Inspired Locomotion | 3 | [α, β, γ]ᵀ | 8.00e-05 | 53.3% | SSM = 60.0 mm | -12.40 | 0.0071 | 0.98% | 0.9991 | 4.20 ms |
| **Sys_03** | 12-DOF 3D Bipedal Humanoid | Bio-Inspired Locomotion | 12 | q ∈ ℝ¹² | 9.50e-06 | 38.2% | ZMP Margin = 32 mm | -8.15 | 0.0210 | 3.15% | 0.9945 | 8.50 ms |
| **Sys_04** | 6-DOF Stewart-Gough Platform | Parallel Manipulators | 6 | [x, y, z, φ, θ, ψ]ᵀ | 3.80e-06 | 42.8% | det(J) ≥ 0.0105 | -4.20 | 0.0158 | 4.82% | 0.9950 | 6.10 ms |
| **Sys_05** | Underactuated Compliant Gripper | Parallel Manipulators | 2 | [x, x', i]ᵀ | 4.50e-03 | 95.0% | Safety Factor 193x | -10.91 | 0.0008 | 1.25% | 0.9984 | 2.85 ms |
| **Sys_06** | Autonomous Mobile Manipulator | Parallel Manipulators | 6 | [x_b, y_b, θ_b, θ₁..θ₃]ᵀ | 8.20e-06 | 32.4% | Manipulability w = 0.18 | -5.50 | 0.0180 | 2.10% | 0.9962 | 7.20 ms |
| **Sys_07** | Two-Wheeled Inverted Pendulum | Underactuated Stabilizers | 2 | [x, θ]ᵀ | 5.20e-07 | 44.1% | Rank 4/4 | -4.85 | 0.0125 | 1.95% | 0.9978 | 3.90 ms |
| **Sys_08** | Critical Skid Vehicle Platform | Underactuated Stabilizers | 3 | [u, v, r]ᵀ | 7.40e-06 | 52.0% | SSF = 1.78 | -18.20 | 0.0472 | 2.46% | 0.9924 | 3.80 ms |
| **Sys_09** | Multi-Terrain Autonomous Rover | Underactuated Stabilizers | 2 | [v_y, r]ᵀ | 6.10e-06 | 46.8% | Stable | -120.00 | 0.0142 | 3.42% | 0.9965 | 4.10 ms |
| **Sys_10** | Thrust-Vectored Rocket Lander | Aerospace Dynamics | 3 | [x, z, θ]ᵀ, m(t) | 8.40e-06 | 35.0% | Gimbal ±20 deg | -3.20 | 0.0040 | 1.12% | 0.9989 | 5.90 ms |
| **Sys_11** | Hybrid Fuel-Cell UAV Powertrain | Aerospace Dynamics | 6 | x ∈ ℝ²² | 1.56e-02 | 28.6% | Thrust Margin 34% | -5.10 | 0.0380 | 1.42% | 0.9972 | 9.80 ms |
| **Sys_12** | 6-DOF Underwater Oceanic ROV | Aerospace Dynamics | 6 | ν, η ∈ ℝ⁶ | 1.40e-04 | 24.8% | BG_z = +50 mm | -2.80 | 0.1840 | 1.84% | 0.9960 | 8.10 ms |
| **Sys_13** | Automated Gantry Crane Anti-Sway | Industrial Handling | 3 | [x_t, l_c, θ_s]ᵀ | 7.80e-07 | 71.2% | Rank 6/6 | -1.04 | 0.0029 | 0.02% | 0.9998 | 4.75 ms |
| **Sys_14** | Quarter-Car Active Suspension | Industrial Handling | 2 | [z_s, z_u]ᵀ | 9.10e-07 | 38.5% | ω_n1 = 8.5 rad/s | -8.50 | 0.0084 | 1.85% | 0.9975 | 3.80 ms |
| **Sys_15** | Dynamic Industrial Conveyor | Industrial Handling | 1 | [θ_d, x_L]ᵀ, m_L(t) | 1.20e-06 | 36.6% | Grip Margin 2.4x | -14.20 | 0.0150 | 1.57% | 0.9980 | 4.20 ms |
| **Sys_16** | Multi-Actuator Electro-Mechanics | Industrial Handling | 3 | [i_a, ω, θ]ᵀ | 5.00e-07 | 48.2% | Re(λ) ≤ -50 | -50.00 | 0.0140 | 0.84% | 0.9992 | 5.10 ms |
| **Sys_17** | Motor Thermal Digital Twin | Industrial Handling | 3 | [i, ω, θ, T_s, T_r]ᵀ | 2.80e-03 | 41.5% | Load Transfer OK | -6.20 | 0.0420 | 1.62% | 0.9970 | 6.30 ms |

The complete table data is saved in `benchmarks/master_verification_matrix.csv`.

---

## Instructions to Run the Code

### 1. Clone the repository
```bash
git clone https://github.com/sunny-nanade/Unified-Mechatronic-Prototyping-Framework.git
cd Unified-Mechatronic-Prototyping-Framework
```

### 2. Install requirements
```bash
pip install -r requirements.txt
```

### 3. Run the verification testbench
```bash
python benchmarks/test_all_17_models.py
```
This runs the verification checks for all 17 systems and updates `benchmarks/master_verification_matrix.csv`.

### 4. Generate the figures
```bash
python scripts/generate_all_figures.py
```

---

## Repository Contents

```
Unified-Mechatronic-Prototyping-Framework/
├── README.md                              # Project overview and instructions
├── LICENSE                                # MIT license
├── requirements.txt                       # Required Python packages
├── benchmarks/
│   ├── test_all_17_models.py              # Verification script for 17 systems
│   └── master_verification_matrix.csv     # Numerical verification results table
├── catalogs/
│   ├── UNIFIED_17_SYSTEM_MATHEMATICAL_CATALOG.md  # Equations of motion for each system
│   └── MASTER_NOMENCLATURE_DICTIONARY.md          # Variable and parameter definitions
├── figures/
│   ├── fig1_mbse_framework.png            # Framework overview diagram
│   ├── fig2_four_gates.png                # Verification gates diagram
│   ├── fig3_state_telemetry.png           # Simulated vs measured data plots
│   ├── fig4_fft_residual.png              # Frequency analysis and residuals
│   ├── fig5_solver_stability.png          # Solver performance analysis
│   └── fig6_prototype_economics.png       # Prototyping iteration metrics
└── scripts/
    └── generate_all_figures.py            # Script to generate publication figures
```

---

## Citation

If you find this work or dataset helpful, please cite:

```bibtex
@article{nanade2026unified,
  title={A Unified First-Principles and Numerical Simulation Framework for Rapid Mechatronic System Prototyping: Dynamic Modeling and Validation Across Heterogeneous Architectures},
  author={Nanade, Sunny and Anne, Koteswararao},
  journal={Designs},
  year={2026},
  publisher={MDPI},
  note={Manuscript ID: designs-4596903}
}
```

---

## Contact

For queries regarding the code or models:  
Dr. Sunny Nanade  
Mukesh Patel School of Technology Management & Engineering, SVKM's NMIMS, Mumbai, India  
Email: `sunny.nanade@nmims.edu`
