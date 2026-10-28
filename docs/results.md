# Results

All learned-walking results are from Isaac Lab simulation of the measured robot. Speeds and distances are measured along the simulator's travel axis over fixed 8-second evaluations.

| Run | What it shows | Result |
| --- | --- | --- |
| Run63 | First walker trained only on sensors the real robot has (72 inputs: IMU, previous commands, gait clock, foot switches) | 1.22 m in 8 s (about 0.15 m/s) across 2,048 evaluation robots, zero falls, 96.5% foot-contact match |
| Run64 | Speed envelope | 0.27 m/s on a 0.45 m/s command, zero falls, 94.9% foot-contact match |
| Run104 | Large-scale continuation from Run63 | 2,048 parallel robots, 500 PPO updates, 24.6 M transitions in 795.6 s. Selected checkpoint (update 100): 1.00 m mean over three commanded speeds, 96.9% foot-contact match, zero falls |
| Run94.8 | Turning in place | Full ±360° scan turn with zero falls |

## Training setup

- **Simulator:** Isaac Lab on Isaac Sim, articulation with contact sensors, joint, torque and velocity limits.
- **Algorithm:** PPO (`rsl_rl`), up to 2,048 parallel environments.
- **Sensor realism:** IMU noise and per-episode bias, one control step of actuator delay, random foot-switch dropouts, no privileged simulator state in the policy's inputs.
- **Domain randomization:** floor friction, body mass and servo strength.
- **Selection:** every checkpoint is evaluated at fixed speed commands and kept only if it passes falls, foot-contact and distance gates.

Raw numbers: [../evidence/metrics.json](../evidence/metrics.json).
