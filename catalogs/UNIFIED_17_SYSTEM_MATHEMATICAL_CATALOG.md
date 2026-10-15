# UNIFIED 17-SYSTEM MATHEMATICAL & DYNAMICAL FORMULATION CATALOG
## Special Issue: Mechatronic System Design — MDPI Designs (CiteScore 5.7, Scopus Q1)
### Authors: Sunny Nanade, Koteswararao Anne (SVKM's NMIMS MPSTME, Mumbai, India)

---

## EXECUTIVE SUMMARY & NOMENCLATURE HARMONIZATION

> **System Architecture Catalog.** This catalog provides the unified first-principles kinematic and dynamic formulations across all 17 heterogeneous mechatronic architectures analyzed in this study. Numerical benchmarks, gate verification metrics, and stability margins are generated via the unified verification pipeline.
This catalog provides the complete, mathematically unified benchmark formulations across all 17 heterogeneous mechatronic architectures analyzed in this study. All systems adhere strictly to the **Unified IEEE/ASME Multi-Body Robotics Formulation**:
$$\mathbf{M}(\mathbf{q})\ddot{\mathbf{q}} + \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})\dot{\mathbf{q}} + \mathbf{G}(\mathbf{q}) + \mathbf{F}_f(\dot{\mathbf{q}}) + \mathbf{K}_s(\mathbf{q}) = \mathbf{B}_u(\mathbf{q})\mathbf{u} + \mathbf{J}_e^T(\mathbf{q})\mathbf{F}_{ext} + \mathbf{A}^T(\mathbf{q})\boldsymbol{\lambda}$$

---

# DOMAIN 1: BIO-INSPIRED & LEGGED LOCOMOTION

### [SYS-01] 2-DOF Quadruped Pantograph Robotic Leg
- **Domain:** Bio-Inspired & Legged Locomotion
- **Generalized Coordinates:** $\mathbf{q} = [\theta_1, \theta_2]^T \in \mathbb{R}^2$ (Hip pitch $\theta_1$, Knee pitch $\theta_2$).
- **Kinematic Loop:** Foot position $\mathbf{r}_f = [l_1 \sin\theta_1 + l_2 \sin(\theta_1 + \theta_2), -l_1 \cos\theta_1 - l_2 \cos(\theta_1 + \theta_2)]^T$.
- **Inertia Matrix $\mathbf{M}(\mathbf{q})$:**
  $$m_{11} = m_1 c_1^2 + I_1 + m_2(l_1^2 + c_2^2 + 2 l_1 c_2 \cos\theta_2) + I_2, \quad m_{12} = m_{21} = m_2(c_2^2 + l_1 c_2 \cos\theta_2) + I_2, \quad m_{22} = m_2 c_2^2 + I_2$$
- **Coriolis Matrix $\mathbf{C}(\mathbf{q}, \dot{\mathbf{q}})$:**
  $$h = m_2 l_1 c_2 \sin\theta_2; \quad \mathbf{C}(\mathbf{q}, \dot{\mathbf{q}}) = \begin{bmatrix} -h\dot{\theta}_2 & -h(\dot{\theta}_1 + \dot{\theta}_2) \ h\dot{\theta}_1 & 0 \end{bmatrix}$$
- **Gravity Vector $\mathbf{G}(\mathbf{q})$:**
  $$g_1 = (m_1 c_1 + m_2 l_1) g \cos\theta_1 + m_2 c_2 g \cos(\theta_1 + \theta_2), \quad g_2 = m_2 c_2 g \cos(\theta_1 + \theta_2)$$
- **Physical Parameters (SI Units):** $l_1 = l_2 = 0.20\text{ m}, c_1 = c_2 = 0.10\text{ m}, m_1 = 0.85\text{ kg}, m_2 = 0.65\text{ kg}, I_1 = 0.005\text{ kg}\cdot\text{m}^2, I_2 = 0.003\text{ kg}\cdot\text{m}^2, b_1 = b_2 = 0.02\text{ N}\cdot\text{s/rad}, \tau_{max} = 80.0\text{ N}\cdot\text{m}$.
- **Seminal Literature:** Raibert, M.H. *Legged Robots That Balance*, MIT Press, 1986; Wensing, P.M. et al., *IEEE Trans. Robot.*, 2017.

### [SYS-02] 3-DOF Tripod Locomotion Hexapod Robot
- **Domain:** Bio-Inspired & Legged Locomotion
- **Generalized Coordinates:** $\mathbf{q}_i = [\alpha_i, \beta_i, \gamma_i]^T$ per leg ($i=1..6$) across 6 radial kinematic chains.
- **Kinematic Formulation:** Spatial D-H convention ($a_1=l_1, a_2=l_2, a_3=l_3; \alpha_1=+\pi/2, \alpha_2=0, \alpha_3=0$).
- **Dynamics & Gait:** Symmetrical alternating tripod wave gait (duty factor $\beta_{gait}=0.50$, stroke $L=80\text{ mm}$, clearance $H=40\text{ mm}$) with unilateral Kelvin-Voigt viscoelastic ground reaction forces.
- **Physical Parameters (SI Units):** $l_1 = 0.05\text{ m}, l_2 = 0.10\text{ m}, l_3 = 0.15\text{ m}, m_{leg} = 0.35\text{ kg}, m_{body} = 0.80\text{ kg}, m_{tot} = 2.90\text{ kg}, \tau_{max} = 1.8\text{ N}\cdot\text{m}$.
- **Seminal Literature:** Siciliano, B. et al. *Robotics: Modelling, Planning and Control*, Springer, 2009; Arena, P. et al., *IEEE Control Syst. Mag.*, 2004.

### [SYS-03] 12-DOF 3D Bipedal Humanoid Robot
- **Domain:** Bio-Inspired & Legged Locomotion
- **Generalized Coordinates:** $\mathbf{q} = [\mathbf{q}_R^T, \mathbf{q}_L^T]^T \in \mathbb{R}^{12}$ ($6\text{ DOF}$ per leg: Hip Yaw/Roll/Pitch, Knee Pitch, Ankle Pitch/Roll).
- **Dynamics & Balance:** Multi-body Euler-Lagrange kinetic chain coupled to Linear Inverted Pendulum Model (LIPM) for Zero-Moment Point (ZMP) trajectory preview control.
- **Physical Parameters (SI Units):** $m_{torso} = 4.546\text{ kg}, m_{leg} = 0.705\text{ kg}, m_{tot} = 5.956\text{ kg}, l_{thigh} = l_{shin} = 0.18\text{ m}, \tau_{max} = 20.0\text{ N}\cdot\text{m}$.
- **Seminal Literature:** Vukobratović, M.; Borovac, B., *Int. J. Humanoid Robot.*, 2004; Kajita, S. et al., *Proc. IEEE ICRA*, 2003.

---

# DOMAIN 2: PARALLEL MANIPULATORS & PRECISION POSITIONING

### [SYS-04] 6-DOF Stewart-Gough Parallel Platform
- **Domain:** Parallel Manipulators
- **Generalized Coordinates:** $\mathbf{x}_p = [x, y, z, \phi, \theta, \psi]^T \in \mathbb{R}^6$ (Platform pose) + $[x_b, y_b]^T$ (Ball position).
- **Kinematics:** 3-RSS closed spatial loop with analytical crank inverse kinematics $\theta_i = \text{atan2}(B_i, A_i) - \arccos(C_i / \sqrt{A_i^2+B_i^2})$.
- **Ball-Plate Dynamic Coupling:** Non-holonomic rolling without slipping $\ddot{x}_b = \frac{5}{7} g \beta, \quad \ddot{y}_b = -\frac{5}{7} g \alpha$.
- **Physical Parameters (SI Units):** $r_{base} = 0.15\text{ m}, r_{plat} = 0.10\text{ m}, L_{horn} = 0.04\text{ m}, L_{rod} = 0.23\text{ m}, m_b = 0.045\text{ kg}, r_b = 0.02\text{ m}, \tau_{servo, max} = 2.5\text{ N}\cdot\text{m}$.
- **Seminal Literature:** Merlet, J.-P. *Parallel Robots*, 2nd ed., Springer, 2006; Dasgupta, B.; Mruthyunjaya, T.S., *Mech. Mach. Theory*, 2000.

### [SYS-05] Underactuated Compliant Robotic Gripper
- **Domain:** Parallel Manipulators
- **Generalized Coordinates:** $\mathbf{q} = [x, \dot{x}, i]^T$ (Jaw displacement, velocity, armature current).
- **Dynamics:** Electromechanical lead-screw drive coupled to flexure compliance:
  $$M_{eff}\ddot{x} + B_{eff}\dot{x} + K_{eff}x = \Gamma_{em} i - F_{contact}, \quad L_m \frac{di}{dt} + R_m i + K_{e,eff}\dot{x} = V_{in}(t)$$
- **Physical Parameters (SI Units):** $M_{eff} = 0.550\text{ kg}, B_{eff} = 6.00\text{ N}\cdot\text{s/m}, K_{eff} = 200.0\text{ N/m}, \Gamma_{em} = 13.60\text{ N/A}, R_m = 0.25\ \Omega, L_m = 1.2\text{ mH}, p = 0.005\text{ m/rad}$.
- **Seminal Literature:** Dollar, A.M.; Howe, R.D., *Int. J. Robot. Res.*, 2010; Birglen, L. et al., *Underactuated Robotic Hands*, Springer, 2008.

### [SYS-06] Autonomous Mobile Pick-and-Place Manipulator
- **Domain:** Parallel Manipulators
- **Generalized Coordinates:** $\mathbf{q} = [x_b, y_b, \theta_b, \theta_1, \theta_2, \theta_3]^T \in \mathbb{R}^6$ (Husky base pose + 3-DOF articulated arm).
- **Inertia Cross-Coupling:** Evaluated non-zero off-diagonal sub-matrix $\mathbf{M}_{ba}(\mathbf{q}) = \mathbf{M}_{ab}^T(\mathbf{q})$ transferring reaction dynamic torques.
- **Physical Parameters (SI Units):** $m_b = 38.0\text{ kg}, I_b = 2.45\text{ kg}\cdot\text{m}^2, m_{arm} = 3.60\text{ kg}, m_{load} = 0.16\text{ kg}, F_{wheel, max} = 950\text{ N}, \tau_{arm, max} = 160\text{ N}\cdot\text{m}$.
- **Seminal Literature:** Khatib, O., *Int. J. Robot. Res.*, 1995; Yamamoto, Y.; Yun, X., *IEEE Trans. Autom. Control*, 1994.

---

# DOMAIN 3: UNDERACTUATED & NON-LINEAR STABILIZERS

### [SYS-07] Two-Wheeled Inverted Pendulum Self-Balancing Robot
- **Domain:** Underactuated Stabilizers
- **Generalized Coordinates:** $\mathbf{q} = [x, \theta]^T \in \mathbb{R}^2$ (Cart linear displacement, chassis pitch angle).
- **Canonical Mass Matrix $\mathbf{M}(\mathbf{q})$:**
  $$\mathbf{M}(\mathbf{q}) = \begin{bmatrix} M + 2m_w + \frac{2 J_w}{r^2} & M l \cos\theta \ M l \cos\theta & I_p + M l^2 \end{bmatrix} > 0$$
- **Coupled Non-linear EOM:**
  $$(M + 2m_w + 2J_w/r^2)\ddot{x} + M l \cos\theta \ddot{\theta} - M l \sin\theta \dot{\theta}^2 = \frac{2u}{r}, \quad M l \cos\theta \ddot{x} + (I_p + M l^2)\ddot{\theta} - M g l \sin\theta = -2u$$
- **Optimal State-Feedback (LQR):** $\mathbf{K}_{lqr} = [-20.000, -82.415, -19.782, -19.865]$ guaranteeing simultaneous balance & station keeping.
- **Physical Parameters (SI Units):** $M = 0.50\text{ kg}, m_w = 0.10\text{ kg}, l = 0.30\text{ m}, r = 0.05\text{ m}, I_p = 0.006\text{ kg}\cdot\text{m}^2, J_w = 0.0005\text{ kg}\cdot\text{m}^2, \tau_{max} = 2.5\text{ N}\cdot\text{m}$.
- **Seminal Literature:** Spong, M.W., *IEEE Control Syst. Mag.*, 1995; Pathak, K. et al., *IEEE Trans. Robot.*, 2005.

### [SYS-08] Critical Skid Velocity Vehicle Dynamic Platform
- **Domain:** Underactuated Stabilizers
- **Generalized Coordinates:** $\mathbf{q} = [X, Y, \psi]^T \in \mathbb{R}^3$, body quasi-velocities $\boldsymbol{\nu} = [u, v, r]^T$.
- **Nonlinear Tire Mechanics:** Pacejka Magic Formula $F_y(\alpha) = D \sin(C \arctan(B\alpha - E(B\alpha - \arctan(B\alpha))))$.
- **Static Stability Factor:** $\text{SSF} = T / (2 h_{CG}) = 1.778 > \mu_{max} = 0.78$ (pure planar skidding bifurcation failure).
- **Physical Parameters (SI Units):** $m = 0.850\text{ kg}, I_z = 0.0125\text{ kg}\cdot\text{m}^2, a = 0.110\text{ m}, b = 0.130\text{ m}, C_{\alpha f} = 48.5\text{ N/rad}, C_{\alpha r} = 54.2\text{ N/rad}, \mu = 0.78$.
- **Seminal Literature:** Pacejka, H.B. *Tire and Vehicle Dynamics*, 3rd ed., Elsevier, 2012; Rajamani, R. *Vehicle Dynamics and Control*, Springer, 2012.

### [SYS-09] Multi-Terrain Autonomous Rover
- **Domain:** Underactuated Stabilizers
- **Generalized Coordinates:** $\mathbf{q} = [v_y, r]^T \in \mathbb{R}^2$ (Lateral side-slip velocity, yaw rate).
- **Dynamics:** 4-bar active suspension compliance coupled to 4WD skid-steer tire slip kinematics.
- **Physical Parameters (SI Units):** $m = 12.5\text{ kg}, I_z = 0.45\text{ kg}\cdot\text{m}^2, L = 0.44\text{ m}, 2w = 0.36\text{ m}, C_f = C_r = 450.0\text{ N/rad}, U = 1.2\text{ m/s}$.
- **Seminal Literature:** Wong, J.Y. *Theory of Ground Vehicles*, 4th ed., Wiley, 2008; Iagnemma, K.; Dubowsky, S. *Mobile Robots in Rough Terrain*, Springer, 2004.

---

# DOMAIN 4: AERIAL POWERTRAINS & AEROSPACE DYNAMICS

### [SYS-10] Thrust-Vectored Rocket Lander & Docking Mechanism
- **Domain:** Aerospace Dynamics
- **Generalized Coordinates:** $\mathbf{q} = [x, z, \theta]^T \in \mathbb{R}^3$, instantaneous mass $m(t) \in \mathbb{R}^+$.
- **Dynamics:** Meshchersky variable-mass Lagrangian $\dot{m}(t) = -T(t)/(I_{sp} g_0)$ with gimbaled thrust vector $\mathbf{T}(\delta) = [T\sin(\theta+\delta), T\cos(\theta+\delta)]^T$.
- **Physical Parameters (SI Units):** $m_0 = 1.00\text{ kg}, m_{dry} = 0.80\text{ kg}, m_{prop} = 0.20\text{ kg}, I_{yy} = 0.0312\text{ kg}\cdot\text{m}^2, l_{cg} = 0.30\text{ m}, T_{max} = 50.0\text{ N}, \delta_{max} = \pm 20^\circ$.
- **Seminal Literature:** Acikmese, B.; Ploen, S.R., *J. Guid. Control Dyn.*, 2007; Blackmore, L., *Natl. Acad. Eng. Bridge*, 2016.

### [SYS-11] Hybrid Hydrogen Fuel-Cell UAV Aerial Powertrain
- **Domain:** Aerospace Dynamics
- **Generalized Coordinates:** Coupled 22-state vector $\mathbf{x} \in \mathbb{R}^{22}$ (6-DOF rigid flight pose + 4 motor currents + 4 rotor RPMs + FC stack RC dynamics + Battery SOC).
- **Multi-Physics Coupling:** Electrochemical PEM fuel cell polarization ($V_{FC} = V_{oc} - R_{int} I_{FC}$) buffering high-rate motor current surges via Li-ion hybrid bus.
- **Physical Parameters (SI Units):** $m = 1.50\text{ kg}, I_{xx} = I_{yy} = 0.0225\text{ kg}\cdot\text{m}^2, I_{zz} = 0.0450\text{ kg}\cdot\text{m}^2, K_t = 0.025\text{ N}\cdot\text{m/A}, V_{FC,oc} = 28.0\text{ V}, Q_{bat} = 2.20\text{ Ah}$.
- **Seminal Literature:** Bizon, N., *Appl. Energy*, 2019; Gong, A.; Verstraete, D., *Prog. Aerosp. Sci.*, 2017.

### [SYS-12] 6-DOF Underwater Oceanic ROV
- **Domain:** Aerospace Dynamics
- **Generalized Coordinates:** Velocity $\boldsymbol{\nu} = [u, v, w, p, q, r]^T$, Position $\boldsymbol{\eta} = [x, y, z, \phi, \theta, \psi]^T$.
- **Fossen's Marine Dynamics:** $(\mathbf{M}_{RB} + \mathbf{M}_A)\dot{\boldsymbol{\nu}} + (\mathbf{C}_{RB}(\boldsymbol{\nu}) + \mathbf{C}_A(\boldsymbol{\nu}))\boldsymbol{\nu} + \mathbf{D}(\boldsymbol{\nu})\boldsymbol{\nu} + \mathbf{g}(\boldsymbol{\eta}) = \mathbf{B}_t \mathbf{u}$.
- **Physical Parameters (SI Units):** $m_{dry} = 73.89\text{ kg}, I_{xx} = 1.478\text{ kg}\cdot\text{m}^2, I_{yy} = I_{zz} = 2.956\text{ kg}\cdot\text{m}^2, m_{A,surge} = 7.54\text{ kg}, m_{A,heave} = 75.40\text{ kg}, \overline{BG}_z = +0.050\text{ m}, F_{thruster} = 56.0\text{ N}$.
- **Seminal Literature:** Fossen, T.I. *Handbook of Marine Craft Hydrodynamics and Motion Control*, 2nd ed., Wiley, 2021; Prestero, T., MIT M.S. Thesis, 2001.

---

# DOMAIN 5: INDUSTRIAL HANDLING & ELECTRO-MECHANICAL ACTUATORS

### [SYS-13] Automated EoT Gantry Crane with Anti-Sway Hoisting
- **Domain:** Industrial Handling
- **Generalized Coordinates:** $\mathbf{q} = [x_t, l_c, \theta_s]^T \in \mathbb{R}^3$ (Trolley position, cable hoisting length, sway angle).
- **Lagrangian Mass Matrix $\mathbf{M}(\mathbf{q})$:**
  $$\mathbf{M}(\mathbf{q}) = \begin{bmatrix} M_t + m_p & m_p \sin\theta_s & m_p l_c \cos\theta_s \ m_p \sin\theta_s & m_p & 0 \ m_p l_c \cos\theta_s & 0 & m_p l_c^2 \end{bmatrix}, \quad \det\mathbf{M} = M_t m_p^2 l_c^2 > 0$$
- **Coupled Natural Frequency:** $\omega_n = \sqrt{\frac{g(M_t + m_p)}{M_t l_0}} = 1.0388\text{ rad/s}$ ($T_n = 6.05\text{ s}$).
- **Physical Parameters (SI Units):** $M_t = 500.0\text{ kg}, m_p = 50.0\text{ kg}, l_0 = 10.0\text{ m}, b_x = 12.5\text{ N}\cdot\text{s/m}, b_l = 8.0\text{ N}\cdot\text{s/m}, b_\theta = 1.2\text{ N}\cdot\text{m}\cdot\text{s/rad}, F_{x,max} = 1500.0\text{ N}$.
- **Seminal Literature:** Abdel-Rahman, E.M. et al., *J. Vib. Control*, 2003; Singhose, W., *Int. J. Precis. Eng. Manuf.*, 2009.

### [SYS-14] Quarter-Car Active Suspension System
- **Domain:** Industrial Handling
- **Generalized Coordinates:** $\mathbf{q} = [z_s, z_u]^T \in \mathbb{R}^2$ (Sprung body displacement, unsprung wheel displacement).
- **Canonical Second-Order Form:**
  $$\begin{bmatrix} m_s & 0 \ 0 & m_u \end{bmatrix}\ddot{\mathbf{q}} + \begin{bmatrix} c_s & -c_s \ -c_s & c_s+c_t \end{bmatrix}\dot{\mathbf{q}} + \begin{bmatrix} k_s & -k_s \ -k_s & k_s+k_t \end{bmatrix}\mathbf{q} = \begin{bmatrix} 1 \ -1 \end{bmatrix} u_{act} + \begin{bmatrix} 0 \ k_t \end{bmatrix} z_r + \begin{bmatrix} 0 \ c_t \end{bmatrix} \dot{z}_r$$
- **Modal Frequencies:** Body bounce $\omega_{n1} = 8.50\text{ rad/s}$ ($1.35\text{ Hz}$), Wheel hop $\omega_{n2} = 68.37\text{ rad/s}$ ($10.88\text{ Hz}$).
- **Physical Parameters (SI Units):** $m_s = 250.0\text{ kg}, m_u = 45.0\text{ kg}, k_s = 16000.0\text{ N/m}, c_s = 1200.0\text{ N}\cdot\text{s/m}, k_t = 190000.0\text{ N/m}, c_t = 50.0\text{ N}\cdot\text{s/m}$.
- **Seminal Literature:** Hrovat, D., *Automatica*, 1997; Karnopp, D., *ASME J. Vib. Acoust.*, 1995.

### [SYS-15] Dynamic Industrial Conveyor with Transient Loading Effects
- **Domain:** Industrial Handling
- **Generalized Coordinates:** Pulley angle $\theta_d(t)$, belt speed $v_b(t) = R\omega_d(t)$, material payload position $x_L(t)$ under load $m_L(t)$.
- **Thermodynamic Law Proof:** In dry-friction sliding from rest, exactly $50\%$ of drive work is kinetic ($1.125\text{ J}$) and $50\%$ is thermal friction dissipation ($1.125\text{ J}$).
- **Physical Parameters (SI Units):** $R = 0.10\text{ m}, J_0 = 0.05\text{ kg}\cdot\text{m}^2, m_b = 8.0\text{ kg}, m_L = 20.0\text{ kg}, k_{belt} = 45000.0\text{ N/m}, c_{belt} = 120.0\text{ N}\cdot\text{s/m}, \mu = 0.35$.
- **Seminal Literature:** Harrison, A., *Trans. Inst. Eng. Aust. Mech. Eng.*, 1984; Lodewijks, G., *Bulk Solids Handl.*, 2011.

### [SYS-16] Multi-Actuator Electro-Mechanical Dynamics (DC, Servo, Stepper)
- **Domain:** Industrial Handling
- **Generalized Dynamic States:** PMDC $[i_a, \omega, \theta]^T$, Servo $[\theta_{out}, \omega_{out}, i_a]^T$, Hybrid Stepper $[\theta, \omega, i_A, i_B]^T$.
- **Physical Parameters (SI Units):** $R_a = 1.2\ \Omega, L_a = 2.5\text{ mH}, K_t = K_e = 0.055\text{ SI}, J_m = 0.00045\text{ kg}\cdot\text{m}^2, B_m = 0.00012\text{ N}\cdot\text{m}\cdot\text{s/rad}, N_{gear} = 30$.
- **Seminal Literature:** Krause, P.C. et al. *Analysis of Electric Machinery & Drive Systems*, IEEE/Wiley, 2013; Mohan, N. *Electric Machines & Drives*, Wiley, 2012.

### [SYS-17] Motor Thermal-Mechanical Digital Twin & Parameter Estimation
- **Domain:** Industrial Handling
- **Generalized Dynamic States:** $[i(t), \omega(t), \theta(t), T_s(t), T_r(t)]^T \in \mathbb{R}^5$.
- **Coupled Electro-Thermal Network:** Joule heating $P_{loss} = i^2 R(T_s)$ driving 2-node lumped thermal state estimator with dynamic self-healing current derating $\gamma(T_s)$.
- **Physical Parameters (SI Units):** $R_0 = 0.45\ \Omega, \alpha_{Cu} = 0.00393\text{ K}^{-1}, C_{th,s} = 145.0\text{ J/K}, C_{th,r} = 85.0\text{ J/K}, R_{th,sa} = 1.85\text{ K/W}, T_{warn} = 75^\circ\text{C}, T_{crit} = 105^\circ\text{C}$.
- **Seminal Literature:** Boglietti, A. et al., *IEEE Trans. Ind. Electron.*, 2009; Tao, F. et al., *IEEE Trans. Ind. Inform.*, 2019.
