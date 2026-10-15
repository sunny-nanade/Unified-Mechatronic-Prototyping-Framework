import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.patches as P
import pathlib
F = pathlib.Path(__file__).parent / "figures"
# ---- Fig 1: workflow
fig, ax = plt.subplots(figsize=(11, 3.6)); ax.set_xlim(0, 11); ax.set_ylim(0, 3.6); ax.axis("off")
boxes = [("1  Model", "Lagrangian / Newton-Euler\nM(q) q'' + C q' + G + ... = B u"),
         ("2  State space", "x' = f(x,u,t)\nRK45 (explicit), Radau IIA (stiff)"),
         ("3  Four gates", "G1 energy / power residual\nG2 actuator headroom\nG3 architecture clearance\nG4 local Hurwitz stability"),
         ("4  Decision", "all pass: report\nany fail: rule-based\nre-tuning (Algorithm 1)\nand re-evaluate all gates")]
cols = ["#DCE9F7", "#DDF1E8", "#FBEBD3", "#F6DCDC"]
for i, (t, s) in enumerate(boxes):
    x = 0.2 + i * 2.75
    ax.add_patch(P.FancyBboxPatch((x, 0.6), 2.4, 2.4, boxstyle="round,pad=0.05", fc=cols[i], ec="#444"))
    ax.text(x + 1.2, 2.7, t, ha="center", va="center", fontweight="bold", fontsize=11)
    ax.text(x + 1.2, 1.6, s, ha="center", va="center", fontsize=8.5)
    if i < 3: ax.annotate("", xy=(x + 2.7, 1.8), xytext=(x + 2.45, 1.8), arrowprops=dict(arrowstyle="-|>", lw=1.6))
ax.annotate("", xy=(1.4, 0.55), xytext=(9.4, 0.55), arrowprops=dict(arrowstyle="-|>", lw=1.2, ls="--", color="#B00", connectionstyle="arc3,rad=-0.0"))
ax.text(5.4, 0.25, "revise parameters / design and repeat (simulation only; no hardware is involved)", ha="center", fontsize=8.5, color="#B00")
fig.savefig(F / "fig1_workflow.png", dpi=300, bbox_inches="tight"); plt.close(fig)
# ---- Fig 2: portfolio status
status = {1: ("2-DOF leg", "D1", 1), 2: ("Hexapod", "D1", 0), 3: ("Humanoid", "D1", 0), 4: ("Stewart platform", "D2", 0), 5: ("Compliant gripper", "D2", 1),
          6: ("Mobile manipulator", "D2", 0), 7: ("Inverted pendulum", "D3", 1), 8: ("Skid vehicle", "D3", 0), 9: ("Rover", "D3", 0), 10: ("Rocket lander", "D4", 0),
          11: ("Fuel-cell UAV", "D4", 0), 12: ("Underwater ROV", "D4", 0), 13: ("Gantry crane", "D5", 1), 14: ("Quarter-car", "D5", 1), 15: ("Conveyor", "D5", 0),
          16: ("DC motor", "D5", 1), 17: ("Motor thermal twin", "D5", 0)}
fig, ax = plt.subplots(figsize=(11, 3.8)); ax.set_xlim(0, 11); ax.set_ylim(0, 5.4); ax.axis("off")
doms = ["D1 Legged", "D2 Manipulation", "D3 Underactuated", "D4 Aerospace / marine", "D5 Industrial / actuators"]
for j, d in enumerate(["D1", "D2", "D3", "D4", "D5"]):
    ax.text(j * 2.2 + 1.1, 5.15, doms[j], ha="center", fontweight="bold", fontsize=8)
    k = 0
    for sid, (nm, dd, ok) in status.items():
        if dd != d: continue
        ax.add_patch(P.FancyBboxPatch((j * 2.2 + 0.1, 4.2 - 0.85 * k), 2.0, 0.7, boxstyle="round,pad=0.02", fc="#CFE8CF" if ok else "#EEEEEE", ec="#555"))
        ax.text(j * 2.2 + 1.1, 4.55 - 0.85 * k, f"Sys {sid:02d}  {nm}", ha="center", va="center", fontsize=8)
        k += 1
ax.add_patch(P.Rectangle((0.1, 0.0), 0.3, 0.25, fc="#CFE8CF", ec="#555")); ax.text(0.5, 0.12, "gates evaluated in this study (6)", va="center", fontsize=8.5)
ax.add_patch(P.Rectangle((4.2, 0.0), 0.3, 0.25, fc="#EEEEEE", ec="#555")); ax.text(4.6, 0.12, "formulated only; gates not evaluated here (11)", va="center", fontsize=8.5)
fig.savefig(F / "fig2_status.png", dpi=300, bbox_inches="tight"); plt.close(fig)
print("ok")

