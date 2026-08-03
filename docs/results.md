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
| Run64 speed envelope | Simulator speed evidence | 0.2704 m/s achieved on 0.45 m/s command, zero falls, contact 0.9488. |
| Run94.8 scan-turn | Simulator qualification | Selected Run94.6 `model_11`; zero-fall full +/-360 simulation qualification. |
| RunV4 zero-action force-drive gate | Simulator diagnostic | 64 env x 3,000 steps, zero true terminations, min body height 0.109568983 m, peak applied torque 0.394471645 Nm, peak abs qd 0.331431627 rad/s. |
| `stage1_safe_025` | Not promoted | 50 updates, but +0.05 m/s forward replay displaced about 0.00003036 m vs 0.005 m gate. |
| August 3, 2026 first end-to-end RunV4 Stage-2 PPO campaign | Pipeline succeeded; not promoted | Headless Isaac Lab completed 25 genuine optimizer updates across 64 env x 24 steps, produced a finite checkpoint, ran fixed-command evaluation, and cleaned up process/lock ownership. The learned gait failed: fixed +0.05 m/s evaluation produced about -0.000042 m mean forward displacement vs the unchanged 0.005 m gate, so it was simulator-only, truthfully blocked, and not promoted. |

## Interpretation

The strongest result is not a single speed number; it is the engineering separation between what is physically proven, what is simulator-qualified, and what remains blocked. The current learned capability is not cleared for physical deployment.
