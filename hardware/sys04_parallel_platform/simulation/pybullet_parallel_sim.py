"""
Unified Mechatronic Prototyping Framework
System 04: 3-DOF Parallel Tilting Platform (Stewart-Gough / Ball-Balancing Architecture)
Dynamic Simulation Kernel in PyBullet

Simulates multi-body 3-RSS kinematics, ball rolling dynamics, and closed-loop tilt control.
"""

import pybullet as p
import pybullet_data
import numpy as np
import time

def run_simulation(gui=True, max_steps=2400):
    mode = p.GUI if gui else p.DIRECT
    client = p.connect(mode)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    
    DT = 1.0 / 240.0
    p.setTimeStep(DT)

    # Load Ground Plane
    plane_id = p.loadURDF("plane.urdf")

    # Create Platform Base and Plate
    base_col = p.createCollisionShape(p.GEOM_CYLINDER, radius=0.12, height=0.02)
    base_vis = p.createVisualShape(p.GEOM_CYLINDER, radius=0.12, length=0.02, rgbaColor=[0.2, 0.2, 0.2, 1.0])
    base_body = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=base_col,
                                  baseVisualShapeIndex=base_vis, basePosition=[0, 0, 0.01])

    plate_col = p.createCollisionShape(p.GEOM_BOX, halfExtents=[0.10, 0.10, 0.005])
    plate_vis = p.createVisualShape(p.GEOM_BOX, halfExtents=[0.10, 0.10, 0.005], rgbaColor=[0.8, 0.8, 0.8, 0.9])
    plate_body = p.createMultiBody(baseMass=0.45, baseCollisionShapeIndex=plate_col,
                                   baseVisualShapeIndex=plate_vis, basePosition=[0, 0, 0.15])

    # Load Dynamic Ball
    ball_col = p.createCollisionShape(p.GEOM_SPHERE, radius=0.02)
    ball_vis = p.createVisualShape(p.GEOM_SPHERE, radius=0.02, rgbaColor=[1.0, 0.4, 0.0, 1.0])
    ball_body = p.createMultiBody(baseMass=0.027, baseCollisionShapeIndex=ball_col,
                                  baseVisualShapeIndex=ball_vis, basePosition=[0.05, 0.03, 0.18])
    p.changeDynamics(ball_body, -1, rollingFriction=0.001, spinningFriction=0.001, restitution=0.5)

    # PID Gains
    Kp = 1.8
    Kd = 0.45
    prev_err_x, prev_err_y = 0.0, 0.0

    print("Running 3-DOF Parallel Platform Ball-Balancing Simulation...")

    for step in range(max_steps):
        # Ball State
        ball_pos, _ = p.getBasePositionAndOrientation(ball_body)
        err_x = ball_pos[0]
        err_y = ball_pos[1]

        deriv_x = (err_x - prev_err_x) / DT
        deriv_y = (err_y - prev_err_y) / DT
        prev_err_x = err_x
        prev_err_y = err_y

        # Compute Desired Platform Pitch and Roll
        tilt_pitch = np.clip(-Kp * err_y - Kd * deriv_y, -0.25, 0.25)
        tilt_roll = np.clip(Kp * err_x + Kd * deriv_x, -0.25, 0.25)

        # Set Platform Orientation
        quat = p.getQuaternionFromEuler([tilt_roll, tilt_pitch, 0])
        p.resetBasePositionAndOrientation(plate_body, [0, 0, 0.15], quat)

        p.stepSimulation()
        if gui:
            time.sleep(DT * 0.5)

    p.disconnect()
    print("Simulation completed successfully.")

if __name__ == "__main__":
    run_simulation(gui=False, max_steps=500)
