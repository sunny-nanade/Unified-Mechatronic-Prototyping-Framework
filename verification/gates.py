"""Reference implementation of the four verification gates for six mechatronic models.

Run:  python gates.py     (writes results/gate_results.json, results/gate_results.csv, figures/*.png)
Every number reported in the manuscript comes from this file's output.
"""
import json, time, platform, pathlib, sys
import numpy as np
import scipy
import scipy.linalg as sla
from scipy.integrate import solve_ivp
import sympy as sp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).parent
RES = HERE / "results"; RES.mkdir(exist_ok=True)
FIG = HERE / "figures"; FIG.mkdir(exist_ok=True)
G = 9.81
RTOL, ATOL = 1e-8, 1e-10
EPS_E, EPS_P, S_MARGIN = 1e-4, 2e-2, 0.20
plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.35, "figure.dpi": 150})
R = {}  # results store


# ----------------------------------------------------------------- generic helpers
def lagrange(T, V, q, qd):
    """Return numeric functions M(q), h(q,qd) for M qdd + h = tau from symbolic T, V."""
    n = len(q)
    M = sp.Matrix(n, n, lambda i, j: sp.diff(T, qd[i], qd[j]))
    Mdot_qd = sp.Matrix(n, 1, lambda i, _: sum(sp.diff(sum(M[i, j] * qd[j] for j in range(n)), q[k]) * qd[k] for k in range(n)))
    dTdq = sp.Matrix([sp.diff(T, qk) for qk in q])
    dVdq = sp.Matrix([sp.diff(V, qk) for qk in q])
    h = sp.simplify(Mdot_qd - dTdq + dVdq)
    args = list(q) + list(qd)
    Mf = sp.lambdify(args, M, "numpy"); hf = sp.lambdify(args, h, "numpy")
    Ef = sp.lambdify(args, T + V, "numpy")
    return Mf, hf, Ef


def num_jac(f, x0, eps=1e-6):
    n = len(x0); J = np.zeros((n, n))
    for k in range(n):
        d = np.zeros(n); d[k] = eps
        J[:, k] = (f(x0 + d) - f(x0 - d)) / (2 * eps)
    return J


def hurwitz(A):
    ev = np.linalg.eigvals(A)
    return float(np.max(ev.real)), ev


def ctrb_rank(A, B):
    n = A.shape[0]; C = B
    for k in range(1, n): C = np.hstack([C, np.linalg.matrix_power(A, k) @ B])
    return int(np.linalg.matrix_rank(C)), n


def solve(rhs, x0, t1, method="RK45", rtol=RTOL, atol=ATOL, **kw):
    return solve_ivp(rhs, (0, t1), x0, method=method, rtol=rtol, atol=atol, **kw)


def time_per_step(rhs, x0, t1, method="RK45", reps=5):
    ts = []; ns = 0
    for _ in range(reps):
        t0 = time.perf_counter(); s = solve(rhs, x0, t1, method); ts.append(time.perf_counter() - t0); ns = len(s.t) - 1
    return 1e3 * float(np.median(ts)) / ns, ns


def drift(sol, Efun):
    E = np.array([Efun(sol.y[:, k]) for k in range(sol.y.shape[1])])
    return float(np.max(np.abs(E - E[0]) / abs(E[0]))), E


def convergence(rhs, x0, t1, probe):
    """Global error of RK45 versus a tight DOP853 reference for decreasing rtol."""
    ref = solve_ivp(rhs, (0, t1), x0, method="DOP853", rtol=1e-13, atol=1e-14)
    xr = ref.y[:, -1]; out = []
    for rt in (1e-4, 1e-6, 1e-8, 1e-10):
        s = solve_ivp(rhs, (0, t1), x0, method="RK45", rtol=rt, atol=rt * 1e-2)
        out.append((rt, float(np.linalg.norm(s.y[:, -1] - xr) / max(np.linalg.norm(xr), 1e-12)), s.nfev))
    return out


def verdict(ok): return "PASS" if ok else "FAIL"


# ================================================================== Sys 01: 2-DOF leg
def sys01():
    l1 = l2 = 0.20; m1, m2 = 0.85, 0.65; I1, I2 = 0.005, 0.003; c1 = c2 = 0.10; tmax = 80.0
    t1_, t2_, d1, d2 = sp.symbols("t1 t2 d1 d2")
    # link COM kinematics (hip pitch from downward vertical, knee relative)
    p1 = sp.Matrix([c1 * sp.sin(t1_), -c1 * sp.cos(t1_)])
    p2 = sp.Matrix([l1 * sp.sin(t1_) + c2 * sp.sin(t1_ + t2_), -l1 * sp.cos(t1_) - c2 * sp.cos(t1_ + t2_)])
    q = [t1_, t2_]; qd = [d1, d2]
    v1 = p1.jacobian(q) * sp.Matrix(qd); v2 = p2.jacobian(q) * sp.Matrix(qd)
    T = sp.Rational(1, 2) * m1 * (v1.T * v1)[0] + sp.Rational(1, 2) * m2 * (v2.T * v2)[0] + sp.Rational(1, 2) * I1 * d1 ** 2 + sp.Rational(1, 2) * I2 * (d1 + d2) ** 2
    V = G * (m1 * p1[1] + m2 * p2[1])
    Mf, hf, Ef = lagrange(T, V, q, qd)
    Gf = sp.lambdify(q, sp.Matrix([sp.diff(V, qk) for qk in q]), "numpy")
    foot = lambda a, b: np.array([l1 * np.sin(a) + l2 * np.sin(a + b), -l1 * np.cos(a) - l2 * np.cos(a + b)])
    Jf = lambda a, b: np.array([[l1 * np.cos(a) + l2 * np.cos(a + b), l2 * np.cos(a + b)], [l1 * np.sin(a) + l2 * np.sin(a + b), l2 * np.sin(a + b)]])

    def free(t, x):
        a, b, da, db = x
        M = np.array(Mf(a, b, da, db), float); h = np.array(hf(a, b, da, db), float).ravel()
        qdd = np.linalg.solve(M, -h); return [da, db, qdd[0], qdd[1]]
    xf0 = np.array([0.6, 1.0, 0.0, 0.0]); En = lambda x: float(Ef(*x))
    g1 = {}
    for m in ("RK45", "Radau"):
        s = solve(free, xf0, 10.0, m); g1[m] = drift(s, En)[0]
    # driven: gravity-compensated PD to a swing trajectory (no feed-forward, so tracking error is real)
    Kp, Kd = 150.0, 12.0
    xd = lambda t: np.array([0.55 + 0.25 * np.sin(2 * np.pi * t), 1.10 + 0.35 * np.sin(2 * np.pi * t + np.pi / 3)])
    vd = lambda t: np.array([0.25 * 2 * np.pi * np.cos(2 * np.pi * t), 0.35 * 2 * np.pi * np.cos(2 * np.pi * t + np.pi / 3)])

    def tau_of(t, x):
        e = xd(t) - x[:2]; ed = vd(t) - x[2:]
        tau = np.array(Gf(x[0], x[1]), float).ravel() + Kp * e + Kd * ed
        return np.clip(tau, -tmax, tmax), tau

    def driven(t, x):
        tau, _ = tau_of(t, x)
        M = np.array(Mf(*x), float); h = np.array(hf(*x), float).ravel()
        qdd = np.linalg.solve(M, tau - h); return [x[2], x[3], qdd[0], qdd[1]]
    x0 = np.r_[xd(0), vd(0)]
    s = solve(driven, x0, 4.0, "RK45", dense_output=True)
    tt = np.linspace(0, 4, 800); Y = s.sol(tt)
    taus = np.array([tau_of(t, Y[:, k])[1] for k, t in enumerate(tt)])
    head = 1 - np.max(np.abs(taus)) / tmax
    err = np.array([xd(t) - Y[:2, k] for k, t in enumerate(tt)])
    sig = [np.linalg.svd(Jf(*Y[:2, k]), compute_uv=False)[-1] / l1 for k in range(len(tt))]
    sigmin = float(np.min(sig))
    # Gate 4: closed-loop linearisation about the set-point posture (PD + gravity compensation)
    qe = np.array([0.55, 1.10])
    def cl(x):
        Mx = np.array(Mf(x[0], x[1], 0, 0), float)
        tau = np.array(Gf(x[0], x[1]), float).ravel() + Kp * (qe - x[:2]) + Kd * (0 - x[2:]) - np.array(Gf(x[0], x[1]), float).ravel()
        hh = np.array(hf(x[0], x[1], x[2], x[3]), float).ravel()
        qdd = np.linalg.solve(np.array(Mf(*x), float), np.array(Gf(x[0], x[1]), float).ravel() + Kp * (qe - x[:2]) + Kd * (0 - x[2:]) - hh)
        return np.r_[x[2:], qdd]
    A = num_jac(cl, np.r_[qe, 0, 0]); a4, ev = hurwitz(A)
    tm, ns = time_per_step(free, xf0, 10.0)
    # compliant ground-contact test for step-size history (Radau)
    kc, cc, mu, y_g = 1.0e5, 300.0, 0.8, -0.36
    def contact(t, x):
        a, b, da, db = x
        f = foot(a, b); J = Jf(a, b); vf = J @ np.array([da, db])
        dl = y_g - f[1]  # penetration depth (>0 when foot below ground plane)
        Fn = max(0.0, kc * dl ** 1.5 + cc * dl ** 1.5 * (-vf[1])) if dl > 0 else 0.0
        Ft = -mu * Fn * np.tanh(vf[0] / 0.01)
        tc = J.T @ np.array([Ft, Fn])
        s_ = np.clip((t - 0.10) / 0.10, 0, 1); s_ = s_ * s_ * (3 - 2 * s_)  # smooth set-point change pushes the foot into the ground
        qset = np.array([0.30, 0.55 + s_ * (0.10 - 0.55)])
        tau = np.clip(np.array(Gf(a, b), float).ravel() + 200.0 * (qset - x[:2]) + 8.0 * (0 - x[2:]), -tmax, tmax)
        M = np.array(Mf(*x), float); h = np.array(hf(*x), float).ravel()
        qdd = np.linalg.solve(M, tau + tc - h); return [da, db, qdd[0], qdd[1]]
    cs = solve_ivp(contact, (0, 0.6), [0.30, 0.55, 0, 0], method="Radau", rtol=1e-6, atol=1e-8, dense_output=False)
    hh = np.diff(cs.t); fz = np.array([max(0.0, kc * max(y_g - foot(cs.y[0, k], cs.y[1, k])[1], 0) ** 1.5) for k in range(len(cs.t))])
    tcs = cs.t[1:]; t_c = float(cs.t[np.argmax(fz > 0.05)]); pre = (tcs > t_c - 0.04) & (tcs < t_c); imp = (tcs >= t_c - 0.005) & (tcs < t_c + 0.10)
    h_pre = float(np.median(hh[pre])); h_imp = float(hh[imp].min()); t_imp = float(tcs[imp][np.argmin(hh[imp])])
    t_rec = float(tcs[(tcs > t_imp) & (hh >= 0.5 * h_pre)][0] - t_imp)
    R["sys01"] = dict(t_contact=t_c, h_pre=h_pre, h_impact=h_imp, t_h_impact=t_imp, t_recover=t_rec, name="2-DOF leg", gate1_rk45=g1["RK45"], gate1_radau=g1["Radau"], gate2=head, gate3_sigma=sigmin,
                      gate4=a4, ms_step=tm, steps=ns, rmse_rad=float(np.sqrt(np.mean(err ** 2))), peak_tau=float(np.max(np.abs(taus))),
                      contact_hmin=float(hh[1:].min()), contact_h_first=float(hh[0]), contact_hmax=float(hh.max()), contact_nfev=int(cs.nfev), contact_njev=int(cs.njev), contact_nlu=int(cs.nlu), contact_t_hmin=float(cs.t[1:][np.argmin(hh[1:])]), contact_nsteps=int(len(hh)), contact_peakF=float(fz.max()),
                      conv=convergence(driven, x0, 2.0, None))
    return dict(tt=tt, Y=Y, xd=np.array([xd(t) for t in tt]), taus=taus, cs=cs, hh=hh, fz=fz, tmax=tmax)


# ================================================================== Sys 07: two-wheeled inverted pendulum
def sys07():
    M, mw, l, r, Ip, Jw, tmax = 0.50, 0.10, 0.30, 0.05, 0.006, 0.0005, 2.5
    a = M + 2 * mw + 2 * Jw / r ** 2
    def acc(x, u):
        th, dth = x[1], x[3]
        Mm = np.array([[a, M * l * np.cos(th)], [M * l * np.cos(th), Ip + M * l ** 2]])
        rhs = np.array([2 * u / r + M * l * np.sin(th) * dth ** 2, M * G * l * np.sin(th) - 2 * u])
        return np.linalg.solve(Mm, rhs)
    def f(x, u): ac = acc(x, u); return np.array([x[2], x[3], ac[0], ac[1]])
    A = num_jac(lambda x: f(x, 0.0), np.zeros(4)); B = ((f(np.zeros(4), 1e-6) - f(np.zeros(4), -1e-6)) / 2e-6).reshape(4, 1)
    a_open, ev_open = hurwitz(A); rk, n = ctrb_rank(A, B)
    Q = np.diag([10.0, 100.0, 1.0, 1.0]); Rr = np.array([[10.0]])
    P = sla.solve_continuous_are(A, B, Q, Rr); K = (np.linalg.inv(Rr) @ B.T @ P).ravel()
    a_cl, ev_cl = hurwitz(A - B @ K.reshape(1, 4))
    # Gate 1: conservative free fall (u=0, no friction) on the nonlinear model
    En = lambda x: 0.5 * (a * x[2] ** 2 + 2 * M * l * np.cos(x[1]) * x[2] * x[3] + (Ip + M * l ** 2) * x[3] ** 2) + M * G * l * np.cos(x[1])
    free = lambda t, x: f(x, 0.0); xf0 = np.array([0.0, 0.10, 0.0, 0.0]); g1 = {}
    for m in ("RK45", "Radau"):
        s = solve(free, xf0, 1.5, m); g1[m] = drift(s, En)[0]
    # closed-loop recovery from 0.15 rad, with saturation
    def cl(t, x): return f(x, float(np.clip(-K @ x, -tmax, tmax)))
    x0 = np.array([0.0, 0.15, 0.0, 0.0]); s = solve(cl, x0, 4.0, "RK45", dense_output=True)
    tt = np.linspace(0, 4, 600); Y = s.sol(tt); u = np.clip(-(K @ Y), -tmax, tmax)
    head = 1 - np.max(np.abs(-(K @ Y))) / tmax
    # remediation example: a lighter weight Q gives smaller torque; report both
    Q2 = np.diag([1.0, 10.0, 0.1, 0.1]); P2 = sla.solve_continuous_are(A, B, Q2, Rr); K2 = (np.linalg.inv(Rr) @ B.T @ P2).ravel()
    head2 = 1 - np.max(np.abs(K2 @ x0)) / tmax; a_cl2, _ = hurwitz(A - B @ K2.reshape(1, 4))
    tm, ns = time_per_step(cl, x0, 4.0)
    R["sys07"] = dict(name="Two-wheeled inverted pendulum", gate1_rk45=g1["RK45"], gate1_radau=g1["Radau"], gate2=head,
                      gate3_rank=f"{rk}/{n}", gate4=a_cl, gate4_open=a_open, K=K.tolist(), ms_step=tm, steps=ns,
                      alt_gate4=a_cl2, alt_gate2=head2, peak_u=float(np.max(np.abs(-(K @ Y)))), conv=convergence(cl, x0, 2.0, None))
    return dict(tt=tt, Y=Y, u=u, tmax=tmax)


# ================================================================== Sys 13: gantry crane (hoist length held)
def sys13():
    Mt, mp, l0, bx, bth, Fmax = 500.0, 50.0, 10.0, 12.5, 1.2, 1500.0
    x_, th_, dx_, dth_ = sp.symbols("x th dx dth")
    px = x_ + l0 * sp.sin(th_); py = -l0 * sp.cos(th_)
    vx = dx_ + l0 * sp.cos(th_) * dth_; vy = l0 * sp.sin(th_) * dth_
    T = sp.Rational(1, 2) * Mt * dx_ ** 2 + sp.Rational(1, 2) * mp * (vx ** 2 + vy ** 2); V = mp * G * py
    Mf, hf, Ef = lagrange(T, V, [x_, th_], [dx_, dth_])
    def acc(x, F, damp=True):
        M = np.array(Mf(*x), float); h = np.array(hf(*x), float).ravel()
        D = np.array([bx * x[2], bth * x[3]]) if damp else np.zeros(2)
        return np.linalg.solve(M, np.array([F, 0.0]) - h - D)
    def f(x, F, damp=True): ac = acc(x, F, damp); return np.array([x[2], x[3], ac[0], ac[1]])
    A = num_jac(lambda x: f(x, 0.0), np.zeros(4)); B = ((f(np.zeros(4), 1e-3) - f(np.zeros(4), -1e-3)) / 2e-3).reshape(4, 1)
    wn = np.sqrt(G * (Mt + mp) / (Mt * l0)); rk, n = ctrb_rank(A, B)
    Q = np.diag([200.0, 2000.0, 100.0, 10.0]); Rr = np.array([[1e-3]])  # sway-weighted LQR
    P = sla.solve_continuous_are(A, B, Q, Rr); K = (np.linalg.inv(Rr) @ B.T @ P).ravel()
    a_cl, _ = hurwitz(A - B @ K.reshape(1, 4))
    En = lambda x: float(Ef(*x)); free = lambda t, x: f(x, 0.0, damp=False); xf0 = np.array([0.0, 0.2, 0.0, 0.0]); g1 = {}
    for m in ("RK45", "Radau"):
        s = solve(free, xf0, 20.0, m); g1[m] = drift(s, En)[0]
    Dist, Tm = 3.5, 10.0
    def ref(t):
        s = np.clip(t / Tm, 0, 1); p = 10 * s ** 3 - 15 * s ** 4 + 6 * s ** 5
        v = (30 * s ** 2 - 60 * s ** 3 + 30 * s ** 4) / Tm * (t < Tm); return Dist * p, Dist * v
    def force(t, x):
        xr, vr = ref(t); e = np.array([x[0] - xr, x[1], x[2] - vr, x[3]])
        return float(np.clip(-K @ e, -Fmax, Fmax)), float(-K @ e)
    def cl(t, x): return f(x, force(t, x)[0])
    x0 = np.zeros(4); s = solve(cl, x0, 25.0, "RK45", dense_output=True)
    tt = np.linspace(0, 25, 1000); Y = s.sol(tt); Fs = np.array([force(t, Y[:, k])[1] for k, t in enumerate(tt)]); xr = np.array([ref(t)[0] for t in tt])
    head = 1 - np.max(np.abs(Fs)) / Fmax
    # power-balance residual for the driven, damped run: integrate dE/dt = F v - b v^2 alongside the states
    def aug(t, z):
        x = z[:4]; F = force(t, x)[0]; d = f(x, F); P_in = F * x[2] - bx * x[2] ** 2 - bth * x[3] ** 2
        return np.r_[d, P_in, abs(F * x[2])]
    sa = solve(aug, np.r_[x0, 0, 0], 25.0, "RK45"); E0 = En(x0)
    Efin = np.array([En(sa.y[:4, k]) for k in range(sa.y.shape[1])])
    resid = np.abs(Efin - E0 - sa.y[4]) / (abs(E0) + 1.0 + sa.y[5])
    # sway reduction: LQR versus uncontrolled (same reference as open-loop force from rigid-body double integrator)
    sway_max = float(np.max(np.abs(Y[1]))); sway_res = float(np.max(np.abs(Y[1][tt > 20])))
    tm, ns = time_per_step(cl, x0, 25.0)
    R["sys13"] = dict(name="Gantry crane (hoist locked)", gate1_rk45=g1["RK45"], gate1_radau=g1["Radau"], gate1_power=float(resid.max()),
                      gate2=head, gate3_rank=f"{rk}/{n}", gate4=a_cl, wn=float(wn), ms_step=tm, steps=ns, sway_max_deg=float(np.degrees(sway_max)),
                      sway_res_deg=float(np.degrees(sway_res)), final_err_mm=float(abs(Y[0, -1] - Dist) * 1e3), peak_F=float(np.max(np.abs(Fs))),
                      conv=convergence(cl, x0, 10.0, None))
    return dict(tt=tt, Y=Y, xr=xr, Fs=Fs, Fmax=Fmax)


# ================================================================== Sys 14: quarter-car suspension
def sys14():
    ms, mu_, ks, kt, cs, ct, Fmax = 250.0, 45.0, 16000.0, 190000.0, 1200.0, 50.0, 2500.0
    Mm = np.diag([ms, mu_])
    def mats(cs_, ct_):
        C = np.array([[cs_, -cs_], [-cs_, cs_ + ct_]]); K = np.array([[ks, -ks], [-ks, ks + kt]])
        return C, K
    h_b, T_b = 0.05, 0.20
    zr = lambda t: h_b / 2 * (1 - np.cos(2 * np.pi * t / T_b)) if 0 <= t <= T_b else 0.0
    vr = lambda t: h_b / 2 * (2 * np.pi / T_b) * np.sin(2 * np.pi * t / T_b) if 0 <= t <= T_b else 0.0
    def f_gen(mode, csky=3000.0, cs_=cs, ct_=ct):
        C, K = mats(cs_, ct_)
        def f(t, z):
            q, v = z[:2], z[2:4]
            u = float(np.clip(-csky * v[0], -Fmax, Fmax)) if mode == "sky" else 0.0
            F = np.array([u, -u + kt * zr(t) + ct_ * vr(t)])
            qdd = np.linalg.solve(Mm, F - C @ v - K @ q); return np.r_[v, qdd], u
        return f
    # Gate 1: undamped, unforced free vibration
    C0, K0 = mats(0.0, 0.0)
    fr = lambda t, z: np.r_[z[2:4], np.linalg.solve(Mm, -K0 @ z[:2])]
    En = lambda z: 0.5 * z[2] ** 2 * ms + 0.5 * z[3] ** 2 * mu_ + 0.5 * ks * (z[0] - z[1]) ** 2 + 0.5 * kt * z[1] ** 2
    zf0 = np.array([0.02, 0.0, 0, 0]); g1 = {}
    for m in ("RK45", "Radau"):
        s = solve(fr, zf0, 5.0, m); g1[m] = drift(s, En)[0]
    out = {}
    for mode in ("passive", "sky"):
        fg = f_gen(mode)
        def aug(t, z):
            d, u = fg(t, z[:4]); v = z[2:4]; cs_dv = cs * (v[0] - v[1])
            P = -cs * (v[0] - v[1]) ** 2 - ct * v[1] * (v[1] - vr(t)) - kt * (z[1] - zr(t)) * vr(t) + u * (v[0] - v[1])
            return np.r_[d, P, abs(P)]
        s = solve_ivp(aug, (0, 3.0), np.zeros(6), method="RK45", rtol=RTOL, atol=ATOL, dense_output=True, max_step=0.005)
        Eg = np.array([En_t(s.y[:4, k]) if False else 0 for k in range(1)])
        tt = np.linspace(0, 3, 1500); Y = s.sol(tt)
        acc_s = np.array([fg(t, Y[:4, k])[0][2] for k, t in enumerate(tt)]); us = np.array([fg(t, Y[:4, k])[1] for k, t in enumerate(tt)])
        Eall = np.array([0.5 * ms * Y[2, k] ** 2 + 0.5 * mu_ * Y[3, k] ** 2 + 0.5 * ks * (Y[0, k] - Y[1, k]) ** 2 + 0.5 * kt * (Y[1, k] - zr(t)) ** 2 for k, t in enumerate(tt)])
        resid = np.max(np.abs(Eall - Eall[0] - Y[4]) / (1.0 + Y[5]))
        out[mode] = dict(tt=tt, Y=Y, acc=acc_s, u=us, resid=float(resid), peak_acc=float(np.max(np.abs(acc_s))), rms_acc=float(np.sqrt(np.mean(acc_s ** 2))),
                         peak_u=float(np.max(np.abs(us))), fg=fg)
    C, K = mats(cs, ct)
    Ass = np.block([[np.zeros((2, 2)), np.eye(2)], [-np.linalg.solve(Mm, K), -np.linalg.solve(Mm, C)]]); Bu = np.r_[np.zeros(2), np.linalg.solve(Mm, [1.0, -1.0])].reshape(4, 1)
    Ask = Ass - Bu @ np.array([[0, 0, 3000.0, 0]]); a4p, _ = hurwitz(Ass); a4s, _ = hurwitz(Ask); rk, n = ctrb_rank(Ass, Bu)
    w = np.sqrt(np.linalg.eigvals(np.linalg.solve(Mm, K)).real); w.sort()
    fgs = out["sky"]["fg"]; rhs = lambda t, z: fgs(t, z)[0]
    tm, ns = time_per_step(rhs, np.zeros(4), 3.0)
    R["sys14"] = dict(name="Quarter-car suspension", gate1_rk45=g1["RK45"], gate1_radau=g1["Radau"], gate1_power=out["sky"]["resid"],
                      gate2=1 - out["sky"]["peak_u"] / Fmax, gate3_rank=f"{rk}/{n}", gate4=a4s, gate4_passive=a4p, ms_step=tm, steps=ns,
                      wn=w.tolist(), peak_acc_passive=out["passive"]["peak_acc"], peak_acc_sky=out["sky"]["peak_acc"],
                      acc_change_pct=100 * (out["sky"]["peak_acc"] - out["passive"]["peak_acc"]) / out["passive"]["peak_acc"],
                      rms_change_pct=100 * (out["sky"]["rms_acc"] - out["passive"]["rms_acc"]) / out["passive"]["rms_acc"],
                      conv=convergence(rhs, np.zeros(4), 1.0, None))
    return out


# ================================================================== Sys 05: compliant gripper (lead-screw drive)
def sys05():
    Me, Be, Ke, Gam, Rm, Lm, Kt, eta, pls = 0.55, 6.0, 200.0, 13.6, 2.5, 0.012, 0.08, 0.85, 0.005
    Kee = Kt / pls; Vmax = 12.0
    kf, cf, xc = 5000.0, 20.0, 0.015   # grasp contact (flexure) engaged beyond jaw position xc
    A = np.array([[0, 1, 0], [-Ke / Me, -Be / Me, Gam / Me], [0, -Kee / Lm, -Rm / Lm]]); Bv = np.array([[0], [0], [1 / Lm]])
    Ac = A.copy(); Ac[1, 0] -= kf / Me; Ac[1, 1] -= cf / Me   # linearisation while in contact
    a4, ev = hurwitz(Ac); rk, n = ctrb_rank(A, Bv)
    def run(V):
        def f(t, z):
            x, v, i = z[0], z[1], z[2]; pen = max(x - xc, 0.0); Fc = kf * pen + (cf * v if pen > 0 else 0.0)
            d = A @ z[:3] + (Bv * V).ravel(); d[1] -= Fc / Me
            return np.r_[d, V * i - Rm * i ** 2 - Be * v ** 2 - (Kee - Gam) * v * i - (cf * v ** 2 if pen > 0 else 0.0), abs(V * i)]
        s = solve(f, np.zeros(5), 1.5, "RK45", dense_output=True, max_step=0.005); tt = np.linspace(0, 1.5, 800); Y = s.sol(tt)
        pen = np.maximum(Y[0] - xc, 0.0)
        E = 0.5 * Lm * Y[2] ** 2 + 0.5 * Me * Y[1] ** 2 + 0.5 * Ke * Y[0] ** 2 + 0.5 * kf * pen ** 2
        resid = np.max(np.abs(E - Y[3])) / (1.0 + Y[4].max())
        return tt, Y, resid, f
    tt, Y, resid, f = run(12.0)
    tm, ns = time_per_step(f, np.zeros(5), 1.5)
    F_nom = float(kf * max(Y[0, -1] - xc, 0))
    # Gate 2 for a voltage-limited actuator: headroom = 1 - V_cmd / V_max
    head_nom = 1 - 12.0 / Vmax; head_re = 1 - 9.0 / Vmax
    tt2, Y2, resid2, _ = run(9.0)
    R["sys05"] = dict(name="Compliant gripper", gate1_power=float(resid), gate2=head_nom, gate2_retuned=head_re, gate3_rank=f"{rk}/{n}", gate4=a4,
                      zeta=float(Be / (2 * np.sqrt(Ke * Me))), wn=float(np.sqrt(Ke / Me)), ms_step=tm, steps=ns, x_ss_mm_nom=float(Y[0, -1] * 1e3),
                      x_ss_mm_re=float(Y2[0, -1] * 1e3), i_ss_nom=float(Y[2, -1]), i_ss_re=float(Y2[2, -1]), F_grip_nom=F_nom,
                      F_grip_re=float(kf * max(Y2[0, -1] - xc, 0)), conv=convergence(f, np.zeros(5), 1.0, None))
    return dict(tt=tt, Y=Y, tt2=tt2, Y2=Y2)


# ================================================================== Sys 16: PMDC motor
def sys16():
    Ra, La, Kt, Ke, Jm, Bm, N, TL = 1.2, 2.5e-3, 0.055, 0.055, 4.5e-4, 1.0e-5, 30.0, 0.30
    A = np.array([[-Ra / La, -Ke / La, 0], [Kt / Jm, -Bm / Jm, 0], [0, 1, 0]]); Bv = np.array([[1 / La], [0], [0]])
    A2 = A[:2, :2]; a4, ev = hurwitz(A2); rk, n = ctrb_rank(A2, Bv[:2])
    V = 24.0
    f = lambda t, z: np.r_[A2 @ z[:2] + Bv[:2].ravel() * V + np.array([0, -TL / N / Jm]), V * z[0] - Ra * z[0] ** 2 - Bm * z[1] ** 2 - (TL / N) * z[1], abs(V * z[0])]
    s = solve(f, np.zeros(4), 0.5, "RK45", dense_output=True); tt = np.linspace(0, 0.5, 800); Y = s.sol(tt)
    E = 0.5 * La * Y[0] ** 2 + 0.5 * Jm * Y[1] ** 2
    resid = np.max(np.abs(E - Y[2])) / (1.0 + Y[3].max())
    tm, ns = time_per_step(f, np.zeros(4), 0.5)
    R["sys16"] = dict(name="PMDC motor", gate1_power=float(resid), gate3_rank=f"{rk}/{n}", gate4=a4, ev=[complex(e).real for e in ev], ms_step=tm, steps=ns,
                      i_peak=float(Y[0].max()), omega_ss=float(Y[1, -1]), conv=convergence(f, np.zeros(4), 0.2, None))
    return dict(tt=tt, Y=Y)


# ================================================================== figures
def figures(d01, d07, d13, d14, d05):
    # Fig. A: leg tracking, torque, step size
    fig, ax = plt.subplots(2, 2, figsize=(11, 7))
    ax[0, 0].plot(d01["tt"], d01["Y"][0], label=r"$\theta_1$"); ax[0, 0].plot(d01["tt"], d01["Y"][1], label=r"$\theta_2$")
    ax[0, 0].plot(d01["tt"], d01["xd"][:, 0], "k:", lw=1); ax[0, 0].plot(d01["tt"], d01["xd"][:, 1], "k:", lw=1, label="command")
    ax[0, 0].set(title="(a) Sys 01 joint angles", xlabel="t [s]", ylabel="angle [rad]"); ax[0, 0].legend()
    ax[0, 1].plot(d01["tt"], d01["taus"][:, 0], label=r"$\tau_1$"); ax[0, 1].plot(d01["tt"], d01["taus"][:, 1], label=r"$\tau_2$")
    ax[0, 1].set(title=r"(b) Commanded torque ($\tau_{max}=80$ N m)", xlabel="t [s]", ylabel="N m"); ax[0, 1].legend()
    cs = d01["cs"]
    ax[1, 0].plot(cs.t, d01["fz"]); ax[1, 0].set(title="(c) Foot normal force during impact (Sys 01)", xlabel="t [s]", ylabel="N")
    ax[1, 1].semilogy(cs.t[1:], d01["hh"] * 1e3, ".-", ms=3); ax[1, 1].set(title="(d) Accepted Radau step size (solver output)", xlabel="t [s]", ylabel="h [ms]")
    fig.tight_layout(); fig.savefig(FIG / "fig_sys01.png"); plt.close(fig)
    # Fig. B: crane
    fig, ax = plt.subplots(2, 2, figsize=(11, 7)); t = d13["tt"]
    ax[0, 0].plot(t, d13["Y"][0], label="trolley"); ax[0, 0].plot(t, d13["xr"], "k:", label="reference"); ax[0, 0].set(title="(a) Trolley position", xlabel="t [s]", ylabel="m"); ax[0, 0].legend()
    ax[0, 1].plot(t, (d13["Y"][0] - d13["xr"]) * 1e3); ax[0, 1].set(title="(b) Tracking error (state minus reference)", xlabel="t [s]", ylabel="mm")
    ax[1, 0].plot(t, np.degrees(d13["Y"][1])); ax[1, 0].set(title="(c) Payload sway", xlabel="t [s]", ylabel="deg")
    ax[1, 1].plot(t, d13["Fs"]); ax[1, 1].axhline(d13["Fmax"], color="r", ls="--"); ax[1, 1].axhline(-d13["Fmax"], color="r", ls="--")
    ax[1, 1].set(title=r"(d) Trolley force ($F_{max}=1500$ N)", xlabel="t [s]", ylabel="N")
    fig.tight_layout(); fig.savefig(FIG / "fig_sys13.png"); plt.close(fig)
    # Fig. C: TWIP + suspension
    fig, ax = plt.subplots(2, 2, figsize=(11, 7))
    ax[0, 0].plot(d07["tt"], np.degrees(d07["Y"][1])); ax[0, 0].set(title="(a) Sys 07 pitch recovery from 0.15 rad", xlabel="t [s]", ylabel="deg")
    ax[0, 1].plot(d07["tt"], d07["u"].ravel()); ax[0, 1].axhline(d07["tmax"], color="r", ls="--"); ax[0, 1].axhline(-d07["tmax"], color="r", ls="--")
    ax[0, 1].set(title="(b) Wheel torque per wheel", xlabel="t [s]", ylabel="N m")
    for m, c in (("passive", "tab:blue"), ("sky", "tab:orange")):
        ax[1, 0].plot(d14[m]["tt"], d14[m]["acc"], c, label=m)
    ax[1, 0].set(title="(c) Sys 14 body acceleration over a 5 cm bump", xlabel="t [s]", ylabel="m/s$^2$"); ax[1, 0].legend()
    ax[1, 1].plot(d14["sky"]["tt"], d14["sky"]["u"]); ax[1, 1].set(title="(d) Skyhook actuator force (limit 2500 N)", xlabel="t [s]", ylabel="N")
    fig.tight_layout(); fig.savefig(FIG / "fig_sys07_14.png"); plt.close(fig)
    # Fig. D: gripper + convergence
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    ax[0].plot(d05["tt"], d05["Y"][0] * 1e3, label="12 V (nominal)"); ax[0].plot(d05["tt2"], d05["Y2"][0] * 1e3, label="9 V (re-tuned)")
    ax[0].set(title="(a) Sys 05 jaw displacement", xlabel="t [s]", ylabel="mm"); ax[0].legend()
    for k, v in R.items():
        if "conv" not in v: continue
        c = np.array(v["conv"]); ax[1].loglog(c[:, 0], c[:, 1], "o-", label=k)
    ax[1].loglog([1e-10, 1e-4], [1e-10, 1e-4], "k:", lw=1); ax[1].set(title="(b) RK45 error vs. rtol (ref.: DOP853)", xlabel="rtol", ylabel="relative error"); ax[1].legend(fontsize=7)
    fig.tight_layout(); fig.savefig(FIG / "fig_sys05_conv.png"); plt.close(fig)


def _cpu_name():
    try:
        import subprocess
        return subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Processor).Name"], capture_output=True, text=True, timeout=30).stdout.strip() or platform.processor()
    except Exception:
        return platform.processor()


def main():
    R["env"] = dict(python=sys.version.split()[0], numpy=np.__version__, scipy=scipy.__version__, sympy=sp.__version__, cpu=_cpu_name(), os=platform.platform())
    d01 = sys01(); d07 = sys07(); d13 = sys13(); d14 = sys14(); d05 = sys05(); sys16()
    figures(d01, d07, d13, d14, d05)
    (RES / "gate_results.json").write_text(json.dumps(R, indent=2, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)), encoding="utf-8")
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "conv"} for k, v in R.items()}, indent=1, default=str))


if __name__ == "__main__":
    main()






