# UNIFIED MECHATRONICS NOMENCLATURE & VARIABLE ATTRIBUTION DICTIONARY
## Standardized Multi-Body Dynamics Lexicon for MDPI Designs Manuscript
### Standard: IEEE / ASME / ISO Multi-Body Robotics & Mechatronics Formulation

---

### 1. GENERALIZED COORDINATES & STATE VECTORS
- q = [q_1, q_2, ..., q_n]^T in R^n: Generalized coordinate vector.
- q_dot = [dq_1/dt, dq_2/dt, ..., dq_n/dt]^T in R^n: Generalized velocity vector.
- q_ddot = [d2q_1/dt2, ..., d2q_n/dt2]^T in R^n: Generalized acceleration vector.
- nu = [u, v, w, p, q, r]^T in R^6: Body-fixed linear and angular velocity quasi-coordinates (marine/aerospace/mobile).
- eta = [x, y, z, phi, theta, psi]^T in R^6: Earth-fixed inertial pose vector.
- x = [q^T, q_dot^T]^T in R^{2n}: Continuous first-order state-space vector (expanded with currents i_a or thermal states T_th where electromechanically coupled).

---

### 2. CANONICAL SECOND-ORDER ROBOTIC EQUATIONS OF MOTION
M(q)*q_ddot + C(q, q_dot)*q_dot + G(q) + F_f(q_dot) + K_s(q) = B_u(q)*u + J_e^T(q)*F_ext + A^T(q)*lambda

Where:
1. M(q) = M^T(q) > 0 in R^{n x n}: Generalized Symmetric Positive-Definite (SPD) Inertia Matrix.
2. C(q, q_dot) in R^{n x n}: Coriolis and Centripetal matrix computed via Christoffel symbols of the first kind:
   c_{kj}(q, q_dot) = sum_{i=1}^n 0.5 * (d m_{kj}/d q_i + d m_{ki}/d q_j - d m_{ij}/d q_k) * q_dot_i
   Passivity Skew-Symmetry Condition: z^T * (M_dot - 2*C) * z = 0 for all z in R^n.
3. G(q) = grad_q V_g(q) in R^n: Conservative Gravitational Torque/Force vector.
4. K_s(q) = grad_q V_e(q) in R^n: Elastic Restoring Force vector (springs, flexures).
5. F_f(q_dot) = B_v * q_dot + F_c * sgn(q_dot) in R^n: Dissipative viscous and Coulomb friction forces.
6. B_u(q) in R^{n x m}: Actuator allocation matrix mapping control inputs u in R^m into generalized coordinates (m <= n).
7. J_e(q) in R^{p x n}: Kinematic contact / end-effector Jacobian matrix.
8. A(q)*q_dot = 0: Non-holonomic / geometric kinematic constraint Pfaffian matrix with Lagrange multipliers lambda.

---

### 3. PHYSICAL PARAMETER SYMBOL STANDARDIZATION (STRICT SI UNITS)

| Physical Quantity | Standard Symbol | Standard SI Unit | Unified Definition across all 17 Systems |
| :--- | :--- | :--- | :--- |
| Total System Mass | m_tot or M | kg | Total combined lumped rigid-body mass |
| Link / Component Mass | m_i (i=1, 2, ...) | kg | Mass of link / phalanx / sprung / unsprung component i |
| Link / Segment Length | l_i (i=1, 2, ...) | m | Kinematic span between consecutive joint axes |
| Center of Mass (COM) Offset | l_{cg, i} or c_i | m | Distance from proximal joint axis to link i center of mass |
| Mass Moment of Inertia | I_xx, I_yy, I_zz | kg*m^2 | Principal centroidal mass moments of inertia |
| Rotor Polar Inertia | J_m | kg*m^2 | Motor armature/rotor rotational inertia |
| Gravitational Acceleration | g | m/s^2 | Standard earth gravity (9.81 m/s^2) |
| Joint / Viscous Damping | b_i or c_i | N*s/m or N*m*s/rad | Linear viscous friction / dissipation coefficient |
| Linear / Angular Spring Constant | k_i or K_s | N/m or N*m/rad | Elastic structural / suspension / flexure stiffness |
| Motor Torque Constant | K_t | N*m/A | Electromechanical torque constant (T_e = K_t * i_a) |
| Back-EMF Voltage Constant | K_e | V/(rad/s) | Faraday counter-electromotive force constant (e_b = K_e * omega) |
| Armature Resistance | R_a | Ohm | Motor winding electrical resistance |
| Armature Inductance | L_a | H or mH | Motor winding electrical inductance |
| Gearbox Reduction Ratio | N or r_g | Dimensionless | Angular velocity reduction ratio (N = omega_in / omega_out > 1) |
| Control Input Vector | u(t) | N*m, N, V | Actuation vector (motor torques, thruster forces, voltage) |
| Actuator Saturation Limit | tau_max or F_max | N*m or N | Maximum continuous/peak actuator output boundary |

---

### 4. SIMULATION VERIFICATION GATES STANDARDIZATION

- Gate 1: Total Mechanical Energy Conservation Drift (epsilon_E)
  epsilon_E(t) = |(E(t) - E(0)) / E(0)| < 1e-4 in unforced, un-damped regimes.
- Gate 2: Dynamic Actuator Torque Headroom Margin (S_i)
  S_i(t) = 1 - |tau_i(t)| / tau_{max, i} >= 20.0% for all t in [0, t_f].
- Gate 3: Kinematic Singularity Clearance Margin (sigma_{min}(J))
  sigma_{min}(J(q)) >= sigma_{threshold} > 0 iff |det(J * J^T)| > 0.
- Gate 4: Phase-Plane Asymptotic Stability & Spectral Pole Placement
  Re(lambda_i(A_{linear})) < 0 for all i=1, ..., 2n.

---

### 5. STANDARDIZED VALIDATION & ERROR METRICS

- Root Mean Square Error (RMSE):
  RMSE = sqrt( (1/N) * sum_{k=1}^N (x_{sim}(t_k) - x_{exp}(t_k))^2 )
- Normalized Mean Absolute Error (NMAE):
  NMAE = ( (1/N) * sum_{k=1}^N |x_{sim}(t_k) - x_{exp}(t_k)| ) / (x_max - x_min) * 100%
- Coefficient of Determination (R^2 Score):
  R^2 = 1 - sum( (x_exp - x_sim)^2 ) / sum( (x_exp - mean(x_exp))^2 )
