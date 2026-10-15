"""
Unified Mechatronic Prototyping Framework
System 04: 3-DOF Parallel Tilting Platform (Ball-Balancing Testbed)
Real-Time Computer Vision State Estimator (OpenCV HSV Tracking)

Tracks ball centroid at 30 Hz and streams normalized (X, Y) error over UART serial.
"""

import cv2
import numpy as np
import serial
import time
import sys

# Serial Configuration
SERIAL_PORT = 'COM3'  # Update to local COM port
BAUD_RATE = 115200

# Color Segmentation Thresholds (HSV for orange ball)
LOWER_HSV = np.array([5, 120, 120])
UPPER_HSV = np.array([22, 255, 255])

# Frame Geometry
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CENTER_X = FRAME_WIDTH / 2.0
CENTER_Y = FRAME_HEIGHT / 2.0
MAX_RADIUS = min(FRAME_WIDTH, FRAME_HEIGHT) / 2.0

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)
        time.sleep(1.0)
        print(f"Connected to ESP32 on {SERIAL_PORT} at {BAUD_RATE} baud.")
    except Exception as e:
        print(f"Warning: Serial port {SERIAL_PORT} unavailable ({e}). Running in visual-only mode.")
        ser = None

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        sys.exit(1)

    print("Camera initialized. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Color Space Conversion & Filtering
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_HSV, UPPER_HSV)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Spatial Contour Moments
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        norm_x, norm_y = 0.0, 0.0
        ball_detected = False

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            
            if M["m00"] > 0 and radius > 8:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m20"] / M["m00"])
                
                # Normalized Coordinates [-1.0, +1.0]
                norm_x = (cx - CENTER_X) / MAX_RADIUS
                norm_y = -(cy - CENTER_Y) / MAX_RADIUS
                norm_x = np.clip(norm_x, -1.0, 1.0)
                norm_y = np.clip(norm_y, -1.0, 1.0)
                ball_detected = True

                # Draw Visual Feedback
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        # Draw Setpoint Center
        cv2.circle(frame, (int(CENTER_X), int(CENTER_Y)), 6, (255, 0, 0), -1)
        cv2.putText(frame, f"X: {norm_x:+.2f}  Y: {norm_y:+.2f}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Stream Coordinates to ESP32
        if ser is not None and ser.is_open:
            msg = f"{norm_x:.3f},{norm_y:.3f}\n"
            ser.write(msg.encode('ascii'))

        cv2.imshow("Parallel Platform Ball Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    if ser is not None:
        ser.close()

if __name__ == "__main__":
    main()
