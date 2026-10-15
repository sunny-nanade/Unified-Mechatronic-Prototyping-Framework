# System 04: 3-DOF Parallel Tilting Platform (Ball-Balancing Testbed)

## Architecture Overview
This module documents the physical hardware testbed, real-time embedded firmware, computer vision tracking pipeline, and dynamic simulation models for the **3-DOF Parallel Tilting Platform (System 04)**.

The testbed serves as an empirical demonstration of the **rapid mechatronic prototyping pipeline**, validating the transition from first-principles multi-body kinematic derivation to physical embedded deployment.

---

## Technical Specifications

| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Kinematic Configuration** | 3-RSS Parallel Mechanism | 3 symmetrically spaced kinematic limbs at $120^\circ$ radial intervals |
| **Base Radius ($R_b$)** | $120.0\text{ mm}$ | Radius of base actuator mounting circle |
| **Platform Radius ($R_p$)** | $90.0\text{ mm}$ | Radius of moving plate spherical joint connections |
| **Crank Length ($l_c$)** | $45.0\text{ mm}$ | Actuator horn length |
| **Connecting Rod ($l_r$)** | $135.0\text{ mm}$ | Carbon fiber connecting link length |
| **Microcontroller** | Espressif ESP32-WROOM-32 | Dual-core Tensilica Xtensa 32-bit LX6 @ 240 MHz |
| **Control Frequency** | $500\text{ Hz}$ ($T_s = 2.0\text{ ms}$) | Deterministic discrete execution loop (WCET $< 45\,\mu\text{s}$) |
| **Vision Sensor** | Overhead USB Camera | $640 \times 480$ resolution @ 30 FPS |
| **Vision Processing** | OpenCV HSV Segmentation | Spatial contour moments tracking ball centroid |
| **Interface** | High-Speed UART | $115,200\text{ baud}$ asynchronous serial stream |

---

## Module Directory Structure

```
hardware/sys04_parallel_platform/
├── README.md                      # Hardware documentation and kinematics specifications
├── firmware/
│   └── esp32_platform_control.ino # ESP32 500 Hz discrete execution loop & IK solver
├── vision/
│   └── ball_tracker_opencv.py     # 30 Hz OpenCV HSV color segmentation & serial streamer
└── simulation/
    └── pybullet_parallel_sim.py   # PyBullet multi-body dynamic simulation engine
```

---

## Inverse Kinematics Formulation

For a commanded platform orientation defined by pitch angle $\theta_p$ and roll angle $\theta_r$, the required vertical displacement $z_i$ of each spherical joint $i \in \{1, 2, 3\}$ is:

$$z_1 = R_p \sin\theta_p$$
$$z_2 = R_p \left( -\frac{1}{2}\sin\theta_p + \frac{\sqrt{3}}{2}\sin\theta_r \right)$$
$$z_3 = R_p \left( -\frac{1}{2}\sin\theta_p - \frac{\sqrt{3}}{2}\sin\theta_r \right)$$

The corresponding servo crank angle $\alpha_i$ relative to neutral trim ($\alpha_0 = 80^\circ$) is:

$$\alpha_i = \alpha_0 + \arcsin\left(\frac{z_i}{l_c}\right) \cdot \frac{180^\circ}{\pi}$$

---

## Operating Instructions

1. **Simulation:**
   ```bash
   pip install pybullet numpy
   python simulation/pybullet_parallel_sim.py
   ```
2. **Vision Tracking:**
   ```bash
   pip install opencv-python pyserial numpy
   python vision/ball_tracker_opencv.py
   ```
3. **Firmware:**
   Flash `firmware/esp32_platform_control.ino` to the ESP32 using the Arduino IDE with `ESP32Servo` library installed.
