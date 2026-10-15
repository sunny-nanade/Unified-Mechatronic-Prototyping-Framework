# Unified First-Principles and Numerical Simulation Framework for Rapid Mechatronic System Prototyping

Code, numerical verification gates, dynamic benchmark toolchains, and embedded hardware assets accompanying the manuscript:  
**"A Unified First-Principles and Numerical Simulation Framework for Rapid Mechatronic System Prototyping: Dynamic Modeling and Validation Across Heterogeneous Architectures"**  
(*Designs*, MDPI, Manuscript ID: `designs-4596903`, CiteScore 5.7, Scopus Q1).  
**Authors:** Dr. Sunny Nanade & Dr. Koteswararao Anne (SVKM's NMIMS MPSTME, Mumbai, India).

---

## Overview

Modern mechatronic development requires bridging the sim-to-real gap between idealized kinematic designs and multi-physics execution. This repository provides the open-source reference implementation of the unified Model-Based Systems Engineering (MBSE) prototyping framework:

1. **Canonical Multi-Body Dynamics:** Second-order Lagrangian and Bond Graph formalizations with skew-symmetry and Hamiltonian passivity invariants mapped to continuous state-space architectures across 17 heterogeneous systems spanning 5 engineering domains:
   - *Domain 1:* Bio-Inspired & Legged Locomotion (Systems 01–03)
   - *Domain 2:* Parallel Manipulators & Precision Positioning (Systems 04–06)
   - *Domain 3:* Underactuated & Balancing Systems (Systems 07–09)
   - *Domain 4:* Aerospace & Marine Dynamics (Systems 10–12)
   - *Domain 5:* Industrial Automation & Electromechanics (Systems 13–17)

2. **Four Deterministic Pre-Fabrication Verification Gates:**
   - **Gate 1 (Mechanical Energy & Power Consistency):** Normalized mechanical energy drift ($\varepsilon_E < 10^{-4}$) for conservative orbits; normalized power-balance dissipation residual ($\varepsilon_P < 2.0 \times 10^{-2}$) for forced, dissipative, and non-holonomic systems.
   - **Gate 2 (Dynamic Actuator Torque Headroom):** Actuator dynamic headroom margin ($S_i \ge 20\%$) to safeguard against transient saturation, friction, and thermal derating.
   - **Gate 3 (Kinematic Feasibility & Static Stability):** Kinematic singularity clearance ($\sigma_{\min}(\mathbf{J}_e) \ge 0.0105$), full controllability rank ($\operatorname{rank}(\mathcal{C}) = n$), Zero-Moment Point (ZMP) margins ($d_{\text{ZMP}} \ge 32\text{ mm}$), Static Stability Margin ($\text{SSM} \ge 60\text{ mm}$), and metacentric righting stability ($\overline{BG}_z \ge +50\text{ mm}$).
   - **Gate 4 (Spectral Asymptotic Stability):** Hurwitz spectral stability of designated trim equilibria ($\max \operatorname{Re}(\lambda_i) < 0$) and closed-loop Riccati (CARE) LQR pole placement.

3. **Empirical Prototyping Demonstration:**
   - Physical implementation of the 3-DOF Parallel Tilting Platform (System 04) running deterministic inverse kinematics and dual-axis PID loops on an Espressif ESP32 microcontroller at 500 Hz ($T_s = 2.0\text{ ms}$, WCET $< 45\,\mu\text{s}$) with 30 Hz overhead computer vision tracking.

---

## Repository Structure

```
Unified-Mechatronic-Prototyping-Framework/
├── catalogs/
│   ├── MASTER_NOMENCLATURE_DICTIONARY.md   # Unified IEEE/ASME variable taxonomy
│   └── UNIFIED_17_SYSTEM_MATHEMATICAL_CATALOG.md # Closed-form equations for all 17 systems
├── verification/
│   ├── gates.py                            # Deterministic verification gate execution engine
│   ├── make_framework_figs.py              # Framework pipeline diagram generator
│   ├── requirements.txt                    # Python dependencies
│   ├── figures/                            # High-order phase portraits & trajectory benchmarks
│   └── results/
│       └── gate_results.json               # Quantitative gate metrics and solve times
├── hardware/
│   └── sys04_parallel_platform/            # Physical testbed demonstration
│       ├── README.md                       # Hardware documentation and BOM
│       ├── firmware/
│       │   └── esp32_platform_control.ino  # ESP32 500 Hz discrete execution loop
│       ├── vision/
│       │   └── ball_tracker_opencv.py      # 30 Hz OpenCV ball centroid tracker
│       └── simulation/
│           └── pybullet_parallel_sim.py    # PyBullet multi-body dynamic simulator
├── LICENSE                                 # MIT License
├── README.md                               # Project documentation
└── requirements.txt                        # Master environment dependencies
```

---

## Getting Started

### Prerequisites
Python 3.10+ with standard scientific computing libraries:
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
```

### Reproducing Verification Gates
To execute the four deterministic verification gates and generate benchmark outputs:
```bash
cd verification
python gates.py
```
This script evaluates the closed-form multi-body dynamics, performs numerical integration via SciPy (adaptive RK45, stiff Radau-IIA, and high-order DOP853 baselines), and logs quantitative gate pass/fail criteria into `verification/results/gate_results.json`.

---

## Citation

If you use this framework, dynamic models, or verification gates in your research, please cite:
```bibtex
@article{nanade2026unified,
  title={A Unified First-Principles and Numerical Simulation Framework for Rapid Mechatronic System Prototyping: Dynamic Modeling and Validation Across Heterogeneous Architectures},
  author={Nanade, Sunny and Anne, Koteswararao},
  journal={Designs},
  volume={10},
  number={5},
  pages={1--46},
  year={2026},
  publisher={MDPI},
  doi={10.3390/designsXXXXXXXX}
}
```

---

## License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
