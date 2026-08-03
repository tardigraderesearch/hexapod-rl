"""Representative deployable-observation contract for the Run63 walker.

Provenance: distilled from the read-only Run63 handoff. It documents the public
schema without including checkpoint files or operational launch paths.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


OBS_DIM = 72
ACTION_DIM = 18
CONTROL_HZ = 30.0


@dataclass(frozen=True)
class DeployObservation:
    angular_velocity_body_rad_s: tuple[float, float, float]
    gravity_body: tuple[float, float, float]
    joint_position_error_rad: tuple[float, ...]
    joint_velocity_proxy_rad_s: tuple[float, ...]
    phase: float
    command_vx_mps: float
    previous_action: tuple[float, ...]
    foot_switches: tuple[float, ...]


def build_observation(obs: DeployObservation) -> list[float]:
    """Build the 72-slot actor input from deployable or commanded-proxy data."""

    if len(obs.joint_position_error_rad) != ACTION_DIM:
        raise ValueError("joint_position_error_rad must have 18 values")
    if len(obs.joint_velocity_proxy_rad_s) != ACTION_DIM:
        raise ValueError("joint_velocity_proxy_rad_s must have 18 values")
    if len(obs.previous_action) != ACTION_DIM:
        raise ValueError("previous_action must have 18 values")
    if len(obs.foot_switches) != 6:
        raise ValueError("foot_switches must have 6 values")

    vector = [0.0, 0.0, 0.0]
    vector.extend(0.25 * x for x in obs.angular_velocity_body_rad_s)
    vector.extend(obs.gravity_body)
    vector.extend(obs.joint_position_error_rad)
    vector.extend(0.05 * x for x in obs.joint_velocity_proxy_rad_s)
    vector.append(math.sin(2.0 * math.pi * obs.phase))
    vector.append(math.cos(2.0 * math.pi * obs.phase))
    vector.append(3.0 * obs.command_vx_mps)
    vector.extend(obs.previous_action)
    vector.extend(obs.foot_switches)

    if len(vector) != OBS_DIM:
        raise RuntimeError(f"expected {OBS_DIM} observation slots, got {len(vector)}")
    return [max(-10.0, min(10.0, float(x))) for x in vector]
