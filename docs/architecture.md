# Architecture

![Simulation training loop and real robot hardware](diagrams/architecture.png)

Edit the diagram in draw.io: [diagrams/architecture.drawio](diagrams/architecture.drawio) (SVG export: [diagrams/architecture.svg](diagrams/architecture.svg)).

## Hardware

- Six legs, three joints per leg (coxa yaw, femur pitch, tibia pitch), 18 servos.
- One ESP32-S3 drives two PCA9685 servo boards over I2C and reads six foot switches. It clamps every joint command to a per-joint safety table.
- A Jetson Orin runs the gait and talks to the ESP32 over USB serial; an OAK-D Pro provides depth and IMU data.

## Simulation

Isaac Lab provides the articulation model, contact sensors, joint limits, torque and velocity limits, randomized friction and mass, and PPO rollouts across thousands of parallel copies of the robot.

## Policy inputs

The policy sees only what the real robot can measure: IMU angular rate and gravity direction, the speed command, the gait phase, its previous action, commanded-target joint proxies and the six foot-switch bits. See [../src/deploy_observation_contract.py](../src/deploy_observation_contract.py).
