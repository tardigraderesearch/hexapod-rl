# Safety And Limitations

## Hard Boundaries

- Autonomous hardware motion is prohibited.
- Learned locomotion in this snapshot is simulator-only.
- `stage1_safe_025` is not promoted and must not be represented as hardware-ready.
- This repository contains no checkpoints, binaries, launch scripts, private run directories, controller identifiers, credentials, or absolute local paths.

## Known Gaps

- IMU mount-frame calibration remains required before deployable observation slots are trustworthy on hardware.
- Foot-switch ordering and debounce must be re-verified against the exact firmware used for any future bridge.
- Servo torque, rail sag, thermal behavior, backlash, and compliance need bench evidence.
- Simulator contact and actuator models are approximations; passing a simulator gate is not equivalent to safe hardware deployment.

## Public Snapshot Limitation

The snapshot is designed for review in under five minutes. It intentionally omits training runs, checkpoints, heavyweight assets, private process-management artifacts, and hardware-control entry points.
