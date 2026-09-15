import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

out_dir = Path("D:/Sunny/Paper/RRSPBL_2026/MDPI 29082026/figures")
tex_fig_dir = Path("D:/Sunny/Paper/RRSPBL_2026/MDPI 29082026/latex_manuscript/figures")
out_dir.mkdir(parents=True, exist_ok=True)
tex_fig_dir.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------------
# FIGURE 1: ENHANCED MBSE SIMULATION & VERIFICATION FRAMEWORK
# -------------------------------------------------------------
fig = plt.figure(figsize=(15.5, 8.5), dpi=300)
ax = fig.add_subplot(111)
ax.set_xlim(0, 15.5)
ax.set_ylim(0, 8.5)
ax.axis("off")

# Title banner
title_box = patches.FancyBboxPatch((0.5, 7.4), 14.5, 0.85, boxstyle="round,pad=0.08", 
                                  facecolor="#1A365D", edgecolor="#0F203C", linewidth=2)
ax.add_patch(title_box)
ax.text(7.75, 7.82, "Unified Model-Based Systems Engineering (MBSE) Framework & Verification Pipeline", 
        color="white", fontsize=14.5, fontweight="bold", ha="center", va="center", family="serif")

# Color palette for 4 phases
phase_colors = ["#2B6CB0", "#2C7A7B", "#C05621", "#742A2A"]
phase_bg = ["#EBF8FF", "#E6FFFA", "#FFFAF0", "#FFF5F5"]

phases = [
    {
        "num": "PHASE 1",
        "title": "First-Principles\nMechanics & Dynamics",
        "x": 0.5, "y": 2.1, "w": 3.2, "h": 5.0,
        "color": phase_colors[0], "bg": phase_bg[0],
        "items": [
            ("Kinematic Topology & Loops", True),
            (r"Lagrangian Mechanics ($L = T - V$)", False),
            ("Newton-Euler Spatial Vectors", False),
            ("Hunt-Crossley Compliant Contact", False),
            (r"Rayleigh Dissipation ($\mathcal{R}$)", False),
            ("Coupled Electro-Thermal Network", False),
            (r"Pfaffian Constraints ($\mathbf{A}\dot{\mathbf{q}}=\mathbf{0}$)", False)
        ]
    },
    {
        "num": "PHASE 2",
        "title": "Canonical Matrix Reduction\n& Numerical Engine",
        "x": 4.2, "y": 2.1, "w": 3.2, "h": 5.0,
        "color": phase_colors[1], "bg": phase_bg[1],
        "items": [
            (r"$\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q},\dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{G}(\mathbf{q}) = \mathbf{B}_u\mathbf{u}$", True),
            ("Christoffel Skew-Symmetry:", True),
            (r"  $\mathbf{z}^T(\dot{\mathbf{M}} - 2\mathbf{C})\mathbf{z} = 0$", False),
            ("1st-Order State-Space Reduction:", True),
            (r"  $\dot{\mathbf{x}} = \mathbf{f}(\mathbf{x}, \mathbf{u}, t), \, \mathbf{x}=[\mathbf{q}^T, \dot{\mathbf{q}}^T]^T$", False),
            ("Adaptive Runge-Kutta (RK45)", False),
            (r"Tolerances: $\mathrm{rtol}=10^{-8}, \mathrm{atol}=10^{-10}$", False)
        ]
    },
    {
        "num": "PHASE 3",
        "title": "Four Deterministic\nVerification Gates",
        "x": 7.9, "y": 2.1, "w": 3.2, "h": 5.0,
        "color": phase_colors[2], "bg": phase_bg[2],
        "items": [
            (r"Gate 1: Energy Conservation", True),
            (r"  $\epsilon_E = |E(t)-E(0)|/E(0) < 10^{-4}$", False),
            (r"Gate 2: Actuator Headroom", True),
            (r"  $S_i = 1 - |\tau_i|/\tau_{max} \geq 20\%$", False),
            (r"Gate 3: Singularity Clearance", True),
            (r"  $\sigma_{min}(\mathbf{J}(\mathbf{q})) \geq \sigma_{th} > 0$", False),
            (r"Gate 4: Asymptotic Stability", True),
            (r"  $\max \mathrm{Re}(\lambda_i(\mathbf{A})) < 0$", False)
        ]
    },
    {
        "num": "PHASE 4",
        "title": "Experimental Telemetry\n& Sim-to-Real V&V",
        "x": 11.6, "y": 2.1, "w": 3.4, "h": 5.0,
        "color": phase_colors[3], "bg": phase_bg[3],
        "items": [
            ("Hardware Sensor Fusion:", True),
            ("  Optical Encoders (100 Hz)", False),
            ("  6-Axis IMUs (200 Hz)", False),
            ("  Laser Sensors & Current Shunts", False),
            (r"95% Confidence Band ($\pm 2\sigma$)", True),
            (r"Fidelity: $R^2 > 0.992, \, \mathrm{NMAE} < 4.8\%$", True),
            ("Real-Time Solve: <10 ms / cycle", False)
        ]
    }
]

for p in phases:
    # Outer box
    box = patches.FancyBboxPatch((p["x"], p["y"]), p["w"], p["h"], boxstyle="round,pad=0.08",
                                facecolor=p["bg"], edgecolor=p["color"], linewidth=2.5)
    ax.add_patch(box)
    
    # Header ribbon
    hdr = patches.FancyBboxPatch((p["x"], p["y"] + p["h"] - 0.95), p["w"], 0.95, boxstyle="round,pad=0.04",
                                facecolor=p["color"], edgecolor=p["color"], linewidth=1)
    ax.add_patch(hdr)
    ax.text(p["x"] + p["w"]/2, p["y"] + p["h"] - 0.28, p["num"], 
            color="#FEFCBF", fontsize=9.5, fontweight="bold", ha="center", va="center", family="serif")
    ax.text(p["x"] + p["w"]/2, p["y"] + p["h"] - 0.65, p["title"], 
            color="white", fontsize=10.5, fontweight="bold", ha="center", va="center", family="serif")
    
    # Text items
    curr_y = p["y"] + p["h"] - 1.25
    for item, is_bold in p["items"]:
        is_sub = item.startswith("  ")
        ax.text(p["x"] + (0.28 if is_sub else 0.15), curr_y, item, 
                color="#1A202C", fontsize=9.0 if not is_sub else 8.5, 
                fontweight="bold" if is_bold else "normal",
                va="top", family="serif")
        curr_y -= 0.46

# Forward Arrows between phases
arrow_style = dict(arrowstyle="-|>,head_length=0.5,head_width=0.3", color="#2D3748", lw=2.5)
ax.annotate("", xy=(4.15, 4.6), xytext=(3.75, 4.6), arrowprops=arrow_style)
ax.annotate("", xy=(7.85, 4.6), xytext=(7.45, 4.6), arrowprops=arrow_style)
ax.annotate("", xy=(11.55, 4.6), xytext=(11.15, 4.6), arrowprops=arrow_style)

# Gate 1-4 Iterative Redesign Feedback Loop
feedback_box = patches.FancyBboxPatch((0.5, 0.4), 14.5, 1.4, boxstyle="round,pad=0.08",
                                     facecolor="#FFF5F5", edgecolor="#E53E3E", linewidth=2, linestyle="--")
ax.add_patch(feedback_box)

ax.text(7.75, 1.45, "Deterministic Virtual Iteration Loop (Pre-Fabrication Verification)", 
        color="#C53030", fontsize=11.5, fontweight="bold", ha="center", va="center", family="serif")
ax.text(7.75, 0.95, r"If Any Gate Fails ($\epsilon_E \geq 10^{-4}$ or $S_i < 20\%$ or $\sigma_{min}=0$ or $\mathrm{Re}(\lambda) \geq 0$) $\longrightarrow$ Automated Gain Tuning / Link Geometry Refinement (Bypasses Physical Scrap)", 
        color="#2D3748", fontsize=9.5, ha="center", va="center", family="serif")

# Arrow from Phase 3 down to Feedback Loop
ax.annotate("", xy=(9.5, 1.8), xytext=(9.5, 2.1),
            arrowprops=dict(arrowstyle="-|>,head_length=0.4,head_width=0.25", color="#E53E3E", lw=2.0, linestyle="--"))

# Arrow from Feedback Loop back to Phase 1
ax.annotate("", xy=(2.1, 2.1), xytext=(2.1, 1.8),
            arrowprops=dict(arrowstyle="-|>,head_length=0.4,head_width=0.25", color="#E53E3E", lw=2.0, linestyle="--"))

fig.savefig(out_dir / "fig1_mbse_framework.png", dpi=300, bbox_inches="tight")
fig.savefig(tex_fig_dir / "fig1_mbse_framework.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print("Figure 1 generated successfully.")

# -------------------------------------------------------------
# FIGURE 2: ENHANCED 17-SYSTEM HETEROGENEOUS TAXONOMY DIAGRAM
# -------------------------------------------------------------
fig2 = plt.figure(figsize=(16, 11), dpi=300)
ax2 = fig2.add_subplot(111)
ax2.set_xlim(0, 16)
ax2.set_ylim(0, 11)
ax2.axis("off")

# Title Banner
title2 = patches.FancyBboxPatch((0.5, 9.9), 15.0, 0.85, boxstyle="round,pad=0.08",
                               facecolor="#2A4365", edgecolor="#1A202C", linewidth=2)
ax2.add_patch(title2)
ax2.text(8.0, 10.32, "Portfolio of 17 Heterogeneous Mechatronic System Architectures Across 5 Domains",
         color="white", fontsize=14.5, fontweight="bold", ha="center", va="center", family="serif")

domain_data = [
    {
        "domain": "Domain 1: Bio-Inspired & Legged Locomotion",
        "color": "#2B6CB0", "bg": "#EBF8FF",
        "x": 0.5, "y": 5.2, "w": 7.2, "h": 4.4,
        "systems": [
            ("Sys 01: 2-DOF Quadruped Pantograph Leg", r"$\mathbf{q}=[\theta_1, \theta_2]^T$", "Sagittal foot kinematics, Hunt-Crossley ground contact compliance, $\tau_{max}=80\ \mathrm{N\cdot m}$"),
            ("Sys 02: 3-DOF Tripod Hexapod Robot", r"$\mathbf{q}_i=[\alpha, \beta, \gamma]_i^T$", "18-DOF tripod wave gait, Denavit-Hartenberg kinematics, static margin $60\ \mathrm{mm}$"),
            ("Sys 03: 12-DOF 3D Bipedal Humanoid", r"$\mathbf{q} \in \mathbb{R}^{12}$", "3D Linear Inverted Pendulum (LIPM), Zero-Moment Point (ZMP) stability, $32\ \mathrm{mm}$ margin")
        ]
    },
    {
        "domain": "Domain 2: Parallel Manipulators & Grippers",
        "color": "#2C7A7B", "bg": "#E6FFFA",
        "x": 8.3, "y": 5.2, "w": 7.2, "h": 4.4,
        "systems": [
            ("Sys 04: 6-DOF Stewart-Gough Platform", r"$\mathbf{x}_p \in \mathbb{R}^6, \mathbf{q}_{ball} \in \mathbb{R}^2$", "Parallel inverse Jacobian, non-holonomic pure rolling ball stabilization, $\det(\mathbf{J}) \geq 0.01$"),
            ("Sys 05: Compliant Underactuated Gripper", r"$\mathbf{x}=[x, \dot{x}, i_a]^T$", "Lead-screw electro-mechanical compliance, flexure grasping, 193x safety factor"),
            ("Sys 06: Mobile Pick-and-Place Manipulator", r"$\mathbf{q} \in \mathbb{R}^6$", "Coupled 4-WD mobile base + 3-DOF articulated arm, inertial reaction cross-coupling")
        ]
    },
    {
        "domain": "Domain 3: Underactuated Stabilizers",
        "color": "#C05621", "bg": "#FFFAF0",
        "x": 0.5, "y": 0.5, "w": 4.7, "h": 4.4,
        "systems": [
            ("Sys 07: Two-Wheeled Inverted Pendulum", r"$\mathbf{q}=[x, \theta]^T$", "Non-holonomic rolling, saddle-point LQR balance, $\lambda=-4.85$"),
            ("Sys 08: Critical Skid Vehicle Platform", r"$\boldsymbol{\nu}=[u, v, r]^T$", "Non-linear Pacejka tire shear, $u_{crit}=1.45\ \mathrm{m/s}$, $\mathrm{SSF}=1.78$"),
            ("Sys 09: Multi-Terrain Autonomous Rover", r"$\mathbf{q}=[v_y, r]^T$", "4WD skid-steer slip, Hurwitz damping $\lambda=-120\ \mathrm{rad/s}$")
        ]
    },
    {
        "domain": "Domain 4: Aerospace & Oceanic",
        "color": "#6B46C1", "bg": "#FAF5FF",
        "x": 5.65, "y": 0.5, "w": 4.7, "h": 4.4,
        "systems": [
            ("Sys 10: Thrust-Vectored Rocket Lander", r"$\mathbf{q}=[x, z, \theta]^T, m(t)$", "Meshchersky variable mass, gimbal thrust vectoring, soft touchdown"),
            ("Sys 11: Hybrid Fuel-Cell UAV Powertrain", r"$\mathbf{x} \in \mathbb{R}^{22}$", "PEMFC electro-chemical polarization, Li-ion RC circuit, DC bus regulation"),
            ("Sys 12: 6-DOF Underwater Oceanic ROV", r"$\boldsymbol{\nu}, \boldsymbol{\eta} \in \mathbb{R}^6$", "Fossen hydrodynamics, added mass $\mathbf{M}_A$, metacentric $\overline{BG}_z=+50\ \mathrm{mm}$")
        ]
    },
    {
        "domain": "Domain 5: Industrial Transport",
        "color": "#742A2A", "bg": "#FFF5F5",
        "x": 10.8, "y": 0.5, "w": 4.7, "h": 4.4,
        "systems": [
            ("Sys 13: Automated EoT Gantry Crane", r"$\mathbf{q}=[x_t, l_c, \theta_s]^T$", "Moving-fulcrum Lagrangian, 93.7% anti-sway suppression"),
            ("Sys 14: Quarter-Car Active Suspension", r"$\mathbf{q}=[z_s, z_u]^T$", "2-DOF bounce modes, Skyhook damping, 22.3% vibration cut"),
            ("Sys 15: Dynamic Industrial Conveyor", r"$\mathbf{q}=[\theta_d, x_L]^T, m_L$", "Viscoelastic carcass, 50% thermodynamic dissipation proof"),
            ("Sys 16: Multi-Actuator Electro-Mechanics", r"$\mathbf{x}=[i_a, \omega, \theta]^T$", "DC/Servo/Stepper Lorentz dynamics, $\mathrm{Re}(\lambda) \leq -50$"),
            ("Sys 17: Motor Thermal Digital Twin", r"$\mathbf{x}=[i, \omega, \theta, T_s, T_r]^T$", "2-node lumped RC thermal twin, dynamic self-healing derating")
        ]
    }
]

for d in domain_data:
    # Outer box
    box = patches.FancyBboxPatch((d["x"], d["y"]), d["w"], d["h"], boxstyle="round,pad=0.08",
                                facecolor=d["bg"], edgecolor=d["color"], linewidth=2.5)
    ax2.add_patch(box)
    
    # Header ribbon
    hdr = patches.FancyBboxPatch((d["x"], d["y"] + d["h"] - 0.65), d["w"], 0.65, boxstyle="round,pad=0.04",
                                facecolor=d["color"], edgecolor=d["color"], linewidth=1)
    ax2.add_patch(hdr)
    ax2.text(d["x"] + d["w"]/2, d["y"] + d["h"] - 0.32, d["domain"],
             color="white", fontsize=10.5, fontweight="bold", ha="center", va="center", family="serif")
    
    # Systems list
    n_sys = len(d["systems"])
    spacing = (d["h"] - 0.85) / n_sys
    curr_y = d["y"] + d["h"] - 0.95
    for name, coords, desc in d["systems"]:
        ax2.text(d["x"] + 0.15, curr_y, name, color=d["color"], fontsize=9.0, fontweight="bold", family="serif")
        ax2.text(d["x"] + d["w"] - 0.15, curr_y, coords, color="#4A5568", fontsize=8.0, ha="right", family="serif")
        ax2.text(d["x"] + 0.15, curr_y - 0.28, desc, color="#2D3748", fontsize=8.0, va="top", family="serif")
        curr_y -= spacing

fig2.savefig(out_dir / "fig2_system_taxonomy.png", dpi=300, bbox_inches="tight")
fig2.savefig(tex_fig_dir / "fig2_system_taxonomy.png", dpi=300, bbox_inches="tight")
plt.close(fig2)
print("Figure 2 generated successfully.")
