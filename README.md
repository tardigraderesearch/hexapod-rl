# hexapod-rl

**A six-legged walking robot that I designed and built, then taught to walk with reinforcement learning.**

![The trained hexapod walking in NVIDIA Isaac Lab](media/hero-sim-gait.gif)

- **What it is:** an 18-motor, 3D-printed hexapod robot (6 legs, 3 joints each), plus the simulator setup used to train its walking brain.
- **What it does:** a neural network practises walking millions of times in a physics simulator (NVIDIA Isaac Lab) and learns its own gait. The real robot walks with a programmed gait.
- **Why it matters:** this is the same train-in-simulation approach research labs use for legged robots, done end to end by one person: CAD, printing, wiring, firmware, simulation and training.

| The real robot walking | The build | Learning in Isaac Sim |
|---|---|---|
| <img src="media/real-walk-preview.gif" width="260" alt="Real robot walking with a scripted gait"> | <img src="media/hardware-build.jpg" width="260" alt="Printed frame, legs and servos"> | <a href="media/build-evolution/05-learning-to-walk/learning-to-walk-progress.mp4"><img src="media/build-evolution/05-learning-to-walk/learning-to-walk-progress-frame.jpg" width="260" alt="Isaac Sim training view"></a> |
| Walking build, scripted tripod gait ([full clip](media/build-evolution/04-first-walking-build/physical-scripted-walk-demo.mp4)) | Second build: printed frame and custom legs | Early training run in Isaac Sim (click to play) |

## Highlights

| | |
|---|---|
| **2,048** robots trained in parallel | **24.6 M** practice steps in about **13 minutes** |
| **0 falls** in the fixed-speed evaluations | **0.27 m/s** top simulated walking speed |
| **97%** foot-contact match with the target gait | **72** sensor inputs, all available on the real robot |

Full numbers: [docs/results.md](docs/results.md).

## How it works

![Architecture: simulation training loop and real robot hardware](docs/diagrams/architecture.png)

The robot was measured (leg lengths, mass, servo limits) and rebuilt as a digital twin. Isaac Lab runs thousands of copies of it at once, each with randomized floor friction and body mass, and PPO (a reinforcement-learning algorithm) rewards the copies that walk well. The policy only sees what the real robot can sense: body tilt and turn rate from the IMU, its own previous commands, the gait clock and the six foot switches. Diagram source: [docs/diagrams/architecture.drawio](docs/diagrams/architecture.drawio).

## Bill of materials

Parts as used on the walking build. Prices are approximate 2026 street prices in USD. **TBD** marks a spec that hasn't been recorded yet; nothing here is guessed.

### Motion

| Part | Qty | Spec | Approx. cost | Source |
|---|---|---|---|---|
| Hip (coxa) servo: JX CLS6322HV | 6 | HV coreless, 2.07 N·m at 7.4 V, 120° variant | ~$40–46 each | [ServoDatabase](https://servodatabase.com/servo/jx-servo/cls6322hv) |
| Knee and ankle servo: Yipin GX3270BLS | 12 | 70 kg-class brushless HV, 25T spline, 270° variant, 0.10 s/60° at 7.4 V | ~$35–70 each | [Hands-on review](https://rccrawlers.net/2025/05/14/yipin_70kg_2505/) |
| Servo arms, 25T (knee and ankle) | 12 | Femur pocket: Ø16.2 mm hub, 12.6 → 7.6 mm taper, 4.4 mm deep | TBD | TBD |
| Servo arms (hip) | 6 | TBD | TBD | TBD |

### Control and sensing

| Part | Qty | Spec | Approx. cost | Source |
|---|---|---|---|---|
| ESP32-S3 dev board | 1 | Dual-core, native USB; mounted on a screw-terminal breakout (breakout model TBD) | ~$15 | [Espressif](https://www.espressif.com/en/products/socs/esp32-s3) |
| PCA9685 16-channel servo driver | 2 | I2C, 50 Hz; addresses 0x40 (left) and 0x41 (right, A0 bridged) | ~$6–10 each | [Adafruit 815](https://www.adafruit.com/product/815) |
| Foot-contact switch | 6 | COM / NO / NC switch, wired COM → GPIO, NO → GND; exact model TBD | TBD | TBD |
| Luxonis OAK-D Pro | 1 | Stereo depth camera with built-in IMU (the policy's tilt and turn-rate source) | ~$300–400 | [RobotShop](https://uk.robotshop.com/products/luxonis-oak-d-pro-camera-fixed-focus) |
| NVIDIA Jetson Orin + Waveshare case | 1 | Onboard computer; exact Orin module and RAM TBD | TBD | [NVIDIA](https://developer.nvidia.com/embedded/jetson-orin) |

### Power

| Part | Qty | Spec | Approx. cost | Source |
|---|---|---|---|---|
| 20 V tool battery (DeWalt-compatible, labelled DCB204) | 2 | 20 V, 8.0 Ah, 160 Wh Li-ion | ~$25–45 each (aftermarket) | Any DeWalt 20 V-compatible pack |
| Battery-to-wire adapter for the 20 V packs | 2 | Model TBD | TBD | TBD |
| Castle Creations BEC (servo rail) | 2 | Set to 7.4 V; outputs kept separate, never paralleled; model and amp rating TBD | TBD | [Castle Creations](https://www.castlecreations.com/) |
| Buck converter (Jetson supply) | 1 | Finned aluminium module; model and rating TBD | TBD | TBD |

### Frame and hardware

| Part | Qty | Spec | Approx. cost | Source |
|---|---|---|---|---|
| Upper and lower frame plates (printed) | 1 set | Remix of the MakeYourPet hexapod: widened, elongated, angled coxa mounts. Chassis 271 mm long, ~151 cm³ of plastic | in filament | [MakeYourPet hexapod](https://github.com/MakeYourPet/hexapod) (MIT), modified |
| Coxa brackets (printed) | 6 | ~16 cm³ each | in filament | TBD |
| Femurs (printed) | 6 | 78.5 mm horn to horn, ~22 cm³ each | in filament | Original design (Onshape) |
| Tibias (printed) | 6 | 139 mm from ankle horn to floor, ~16 cm³ each | in filament | Original design (Onshape) |
| Foot tips (printed) | 6 | ~0.4 cm³ each | in filament | TBD |
| Filament: PLA / PLA Pro, PETG for flexing parts | ~0.3–0.6 kg | ~484 cm³ of parts in total; printed on a Bambu A1 | ~$20 per 1 kg spool | Any |
| Print settings | | Layer height, walls and infill TBD | | |
| Heat-set inserts | TBD | Size TBD (ankles and coxa mounts) | TBD | TBD |
| M3 screws | TBD | Servo-arm tip screw is M3 (Ø3.2 mm clearance, 30 mm from the pivot); other sizes and lengths TBD | TBD | TBD |
| Epoxy putty | 1 | Fills and locks the coxa mounts around the inserts | TBD | TBD |

### Wiring

| Part | Qty | Spec | Approx. cost | Source |
|---|---|---|---|---|
| Servo extension leads | 18 | Length TBD; plug-in connectors rather than solder splices, so parts can be swapped | TBD | TBD |
| Servo power wire | TBD | Gauge TBD; at least as heavy as the servo leads | TBD | TBD |
| Foot-switch wire | 6 runs | Gauge TBD | TBD | TBD |
| I2C and logic jumpers | ~10 | Dupont or screw terminal | TBD | TBD |

**Optional voice add-on (used in the live demo):** a LavMicro lavalier mic and a BTS0011 Bluetooth speaker on the Jetson, for offline voice commands ("stand", "salute", "down").

Known-price subtotal: roughly **$1,000–1,550** for servos, controller, drivers, camera, batteries and filament, before the Jetson and the TBD power parts.

## Build it yourself

<img src="media/build-evolution/00-aluminum-prototype.jpg" width="520" alt="Aluminium first prototype">

*Where it started: hand-cut aluminium brackets, hobby servos and power-tool batteries. Full history: [docs/build-evolution.md](docs/build-evolution.md).*

### 1. Print

Print the frame plates from the [MakeYourPet hexapod](https://github.com/MakeYourPet/hexapod) and widen them to suit your servos. Model your femurs and tibias to the measured lengths (coxa 48 mm, femur 78.5 mm, tibia 139 mm) so the simulator's numbers match your robot. Prototype in PLA, and use PETG where a part flexes or takes impacts.

### 2. Assemble

<img src="media/build-evolution/04-first-walking-build/current-model-workbench.jpg" width="360" alt="Servos and electronics laid out before assembly">

1. Drill the femurs for the servo arms and test-fit them. Set heat-set inserts in the ankles and let them cool straight.
2. Pack the coxa mounts with epoxy putty, embed inserts, and keep servo and arm travel clear while it cures.
3. Centre every servo at 1500 µs **before** fitting its arm, and label each one by leg and joint.
4. Build one complete reference leg, move every joint by hand, fix any binding, then copy it five times.
5. Mount the legs to the chassis and sweep each one through its range by hand to check for collisions.
6. Fit a foot switch in each tibia so the toe presses it on contact and releases when lifted ([concept sketch](media/build-evolution/01-concept-sketches/concept-foot-contact-switch.jpg)).

### 3. Wire

<img src="media/build-evolution/04-first-walking-build/current-model-power-and-control-stack.jpg" width="360" alt="Power and control stack">

- **I2C:** ESP32 GPIO1 = SDA, GPIO2 = SCL, shared by both PCA9685 boards. Bridge A0 on the right board so it answers at 0x41.
- **Servo power:** BEC output (7.4 V) into each PCA9685's `V+` terminal. Never feed 7.4 V into the board's logic `VCC`.
- **Common ground:** tie the battery, BEC, PCA9685 and ESP32 grounds together. If servos jump to random extremes, check this first.
- **Foot switches:** COM → GPIO, NO → GND, inputs set to `INPUT_PULLUP` (pressed reads LOW).

| Foot switch | Front | Middle | Rear |
|---|---|---|---|
| Left | GPIO7 | GPIO4 | GPIO6 |
| Right | GPIO16 | GPIO15 | GPIO17 |

| PCA9685 channel (front / middle / rear) | Coxa | Knee | Ankle |
|---|---|---|---|
| Left board, 0x40 | 15 / 11 / 7 | 14 / 10 / 5 | 13 / 9 / 4 |
| Right board, 0x41 | 15 / 11 / 7 | 14 / 10 / 6 | 13 / 9 / 5 |

Check polarity with a meter before connecting any servo, and use connectors rather than solder splices on anything you may need to replace.

### 4. Flash

The ESP32-S3 firmware is an Arduino sketch built with `arduino-cli` (board `esp32:esp32:esp32s3:CDCOnBoot=cdc`, so serial works over native USB). It takes newline-terminated text commands at 115200 baud, holds a per-joint table (board, channel, direction, zero pulse, min and max angle) and clamps every command to that table before it reaches a servo. The firmware source isn't in this repo yet; [src/ik_geometry.py](src/ik_geometry.py) and [config/servo_and_sim_limits.json](config/servo_and_sim_limits.json) carry the geometry and limits it uses.

| Joint clamp | Min | Max | Zero |
|---|---|---|---|
| Coxa, front | 2° | 88° | 45° |
| Coxa, middle | 47° | 133° | 90° |
| Coxa, rear | 92° | 178° | 135° |
| Knee | 30° | 160° | 125° |
| Ankle | 55° | 150° | 68° |

Pulse window 620–2050 µs. These are the walking build's values; measure your own.

### 5. Calibrate

1. Put the robot on a stand with all six feet off the ground and the battery connector in reach (pulling it is the emergency stop).
2. Send all joints to 1500 µs. Zero pose: hip straight out, femur 35° above horizontal, knee interior angle 68°. Re-seat any arm that is off by a spline tooth.
3. Pulse one joint at a time by a few degrees (for example 1500 → 1530 → 1500 µs) and confirm the expected joint moved. Positive pulses should swing the hip forward, lift the knee and extend the ankle; mark any joint that moves the other way as inverted.
4. Record small per-joint trims (the walking build needed three).
5. Stand it: feet on a 185 mm radius from the body centre, 110 mm below the body.
6. Walk it: the scripted tripod gait uses an 18° stride, 42° lift and a 1.6–2.1 s period.

<img src="media/build-evolution/04-first-walking-build/physical-scripted-walk-demo-frame.jpg" width="520" alt="Scripted walk on the real robot">

## Training and running the policy

1. **Install** [Isaac Sim and Isaac Lab](https://isaac-sim.github.io/IsaacLab/) on a machine with an NVIDIA RTX GPU (trained here on Isaac Sim 5.1).
2. **Build the digital twin:** a URDF with your measured segment lengths, joint limits, measured mass (5.53 kg here) and servo torque limits (2.07 N·m hips, 5.9 N·m knees and ankles).
3. **Match the real sensors:** use the 72-input observation in [src/deploy_observation_contract.py](src/deploy_observation_contract.py) (schema: [config/run63_deploy_observation_schema.json](config/run63_deploy_observation_schema.json)) with IMU noise and bias, one control step of actuator delay, and random foot-switch dropouts.
4. **Randomize the world:** floor friction 0.4–1.1, body mass ±10%, servo strength 65–100%.
5. **Train** with `rsl_rl` PPO through Isaac Lab's standard training script, headless, with 2,048 environments. The policy runs at 30 Hz and outputs 18 joint corrections on top of a scripted tripod-gait reference.
6. **Evaluate** each checkpoint at fixed speed commands for 8 s and keep it only with zero falls and a good foot-contact match ([src/stage1_gate_check.py](src/stage1_gate_check.py) shows the pattern).
7. **Run the policy** with Isaac Lab's matching `play` script to watch it walk, as in the clip at the top of this page ([full video](media/ari_run63_deploy_walk_0p25.mp4)).

## Repository layout

- `docs/`: [results](docs/results.md), [architecture](docs/architecture.md), [build evolution](docs/build-evolution.md), [draw.io diagram source](docs/diagrams/architecture.drawio)
- `src/`, `config/`: geometry and inverse kinematics, observation contract, evaluation gate, limits
- `evidence/metrics.json`: raw training and evaluation numbers
- `media/`: build photos, robot video and simulation renders
- `scripts/validate_public_repo.py`: checks the repo for secrets, local paths and oversized files

## Credits

- **Femurs and tibias:** original designs, modeled in Onshape.
- **Frame plates:** started from the open-source [MakeYourPet hexapod](https://github.com/MakeYourPet/hexapod) (MIT), then substantially reworked: widened, elongated, angled coxa mounts, new wall angles and reliefs for this hardware.
- Control, simulation setup, training and evaluation: original work.

## License

MIT, see [LICENSE](LICENSE). Citation metadata: [CITATION.cff](CITATION.cff).
