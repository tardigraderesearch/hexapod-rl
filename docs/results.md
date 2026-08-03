# Results

All learned-locomotion results below are simulator-only.

## Verified Platform Facts

- Physical form: 6 legs, 18 total degrees of freedom.
- Joint grouping: coxa yaw, femur pitch, tibia pitch on each leg.
- Physical hardware exists and deterministic gait has been proven under controlled, non-autonomous operation.

## Simulator Results

| Evidence | Status | Conservative result |
| --- | --- | --- |
| Run63 deploy-observation walker | Canonical historical simulator walker | Deployable-observation forward-walking baseline. |
| Run104 Run63-actor relearn continuation | Training completed; update 100 selected; final update 500 not promoted | Simulator-only continuation initialized from the preserved verified Run63 deployable-observation actor. The campaign ran 2,048 parallel environments for 500 PPO updates, totaling 24,576,000 transitions in 795.6 seconds wall time. Fixed-command evaluations commanded no hardware and had zero falls. The seed three-speed 8-second evaluation measured 1.00149 m mean displacement and 0.9468 contact match. Update 100 measured 1.00323 m mean displacement (+0.174%) and 0.96855 contact match with zero falls, so it was selected as champion. Update 500 measured 0.7601 m mean displacement (-24.10%) and 0.97092 contact match with zero falls; it was rejected because it traded locomotion speed for contact/stability. Final explained variance was 0.9028, showing value-function learning but not actor improvement. |
| Run64 speed envelope | Simulator speed evidence | 0.2704 m/s achieved on 0.45 m/s command, zero falls, contact 0.9488. |
| Run94.8 scan-turn | Simulator qualification | Selected Run94.6 `model_11`; zero-fall full +/-360 simulation qualification. |
| RunV4 zero-action force-drive gate | Simulator diagnostic | 64 env x 3,000 steps, zero true terminations, min body height 0.109568983 m, peak applied torque 0.394471645 Nm, peak abs qd 0.331431627 rad/s. |
| `stage1_safe_025` | Not promoted | 50 updates, but +0.05 m/s forward replay displaced about 0.00003036 m vs 0.005 m gate. |
| August 3, 2026 first end-to-end RunV4 Stage-2 PPO campaign | Pipeline succeeded; not promoted | Headless Isaac Lab completed 25 genuine optimizer updates across 64 env x 24 steps, produced a finite checkpoint, ran fixed-command evaluation, and cleaned up process/lock ownership. The learned gait failed: fixed +0.05 m/s evaluation produced about -0.000042 m mean forward displacement vs the unchanged 0.005 m gate, so it was simulator-only, truthfully blocked, and not promoted. |

## Interpretation

The strongest result is not a single speed number; it is the engineering separation between what is physically proven, what is simulator-qualified, and what remains blocked. Run104 completed successfully as simulator training and selected update 100 as the best continuation result, but the final update 500 was not promoted. The current learned capability is not cleared for physical deployment.
