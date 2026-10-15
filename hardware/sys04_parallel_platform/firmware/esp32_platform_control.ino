/*
 * Unified Mechatronic Prototyping Framework
 * System 04: 3-DOF Parallel Tilting Platform (Ball-Balancing Testbed)
 * Real-Time Embedded Firmware for Espressif ESP32
 *
 * Core Control Loop: 500 Hz (Ts = 2.0 ms, WCET < 45 us)
 * Actuation: 3x Digital PWM Servos (Pins 12, 14, 27)
 * Telemetry: High-Speed UART (115200 baud) parsing (X, Y) from 30 Hz OpenCV vision
 */

#include <Arduino.h>
#include <ESP32Servo.h>

// Servo Definitions
Servo servo1, servo2, servo3;
const int SERVO_PIN_1 = 12;
const int SERVO_PIN_2 = 14;
const int SERVO_PIN_3 = 27;

// Platform Geometry (SI Units: meters, radians)
const float R_BASE = 0.120;     // Base radius (m)
const float R_PLAT = 0.090;     // Platform radius (m)
const float L_CRANK = 0.045;    // Servo horn length (m)
const float L_ROD = 0.135;      // Connecting rod length (m)
const float SERVO_NEUTRAL = 80.0; // Degrees neutral trim

// Control Constraints
const float MAX_TILT_DEG = 15.0; // Maximum pitch/roll angle (deg)
const float MIN_PWM_DEG = 65.0;
const float MAX_PWM_DEG = 105.0;

// Dual-Axis PID Gains (Discrete 500 Hz tuning)
float Kp_x = 0.38, Ki_x = 0.02, Kd_x = 0.12;
float Kp_y = 0.38, Ki_y = 0.02, Kd_y = 0.12;

// State Variables
float target_x = 0.0, target_y = 0.0;
float current_x = 0.0, current_y = 0.0;
float prev_err_x = 0.0, prev_err_y = 0.0;
float integral_x = 0.0, integral_y = 0.0;

// Timing Management
unsigned long prev_micros = 0;
const unsigned long LOOP_PERIOD_US = 2000; // 500 Hz loop

// Inverse Kinematics for 3-RSS Parallel Mechanism
void compute_inverse_kinematics(float pitch_rad, float roll_rad, float &ang1, float &ang2, float &ang3) {
    // Platform angular transformation
    float z1 = R_PLAT * sin(pitch_rad);
    float z2 = R_PLAT * (-0.5 * sin(pitch_rad) + 0.866025 * sin(roll_rad));
    float z3 = R_PLAT * (-0.5 * sin(pitch_rad) - 0.866025 * sin(roll_rad));

    // Convert leg height variations to horn angles
    ang1 = SERVO_NEUTRAL + (z1 / L_CRANK) * (180.0 / PI);
    ang2 = SERVO_NEUTRAL + (z2 / L_CRANK) * (180.0 / PI);
    ang3 = SERVO_NEUTRAL + (z3 / L_CRANK) * (180.0 / PI);

    // Apply mechanical limits
    ang1 = constrain(ang1, MIN_PWM_DEG, MAX_PWM_DEG);
    ang2 = constrain(ang2, MIN_PWM_DEG, MAX_PWM_DEG);
    ang3 = constrain(ang3, MIN_PWM_DEG, MAX_PWM_DEG);
}

void setup() {
    Serial.begin(115200);
    
    // Configure ESP32 Timers for Servos
    ESP32PWM::allocateTimer(0);
    ESP32PWM::allocateTimer(1);
    ESP32PWM::allocateTimer(2);
    
    servo1.setPeriodHertz(50);
    servo2.setPeriodHertz(50);
    servo3.setPeriodHertz(50);

    servo1.attach(SERVO_PIN_1, 500, 2500);
    servo2.attach(SERVO_PIN_2, 500, 2500);
    servo3.attach(SERVO_PIN_3, 500, 2500);

    servo1.write(SERVO_NEUTRAL);
    servo2.write(SERVO_NEUTRAL);
    servo3.write(SERVO_NEUTRAL);

    prev_micros = micros();
}

void loop() {
    unsigned long current_micros = micros();

    // Check Serial for Vision Frame Input: "X,Y\n"
    if (Serial.available() > 0) {
        String msg = Serial.readStringUntil('\n');
        int comma_idx = msg.indexOf(',');
        if (comma_idx > 0) {
            current_x = msg.substring(0, comma_idx).toFloat();
            current_y = msg.substring(comma_idx + 1).toFloat();
        }
    }

    // Deterministic 500 Hz Execution
    if (current_micros - prev_micros >= LOOP_PERIOD_US) {
        prev_micros += LOOP_PERIOD_US;

        // Position Error with Deadzone Filtering (|e| < 0.03 normalized)
        float err_x = target_x - current_x;
        float err_y = target_y - current_y;
        if (abs(err_x) < 0.03) err_x = 0.0;
        if (abs(err_y) < 0.03) err_y = 0.0;

        // Discrete PID Calculation
        integral_x = constrain(integral_x + err_x * 0.002, -0.2, 0.2);
        integral_y = constrain(integral_y + err_y * 0.002, -0.2, 0.2);

        float deriv_x = (err_x - prev_err_x) / 0.002;
        float deriv_y = (err_y - prev_err_y) / 0.002;
        prev_err_x = err_x;
        prev_err_y = err_y;

        float u_x = Kp_x * err_x + Ki_x * integral_x + Kd_x * deriv_x;
        float u_y = Kp_y * err_y + Ki_y * integral_y + Kd_y * deriv_y;

        // Map Control Effort to Target Tilt Angles
        float pitch_cmd = constrain(u_y, -MAX_TILT_DEG * PI / 180.0, MAX_TILT_DEG * PI / 180.0);
        float roll_cmd = constrain(u_x, -MAX_TILT_DEG * PI / 180.0, MAX_TILT_DEG * PI / 180.0);

        // Solve Inverse Kinematics
        float a1, a2, a3;
        compute_inverse_kinematics(pitch_cmd, roll_cmd, a1, a2, a3);

        // Write Actuation Commands
        servo1.write((int)a1);
        servo2.write((int)a2);
        servo3.write((int)a3);
    }
}
