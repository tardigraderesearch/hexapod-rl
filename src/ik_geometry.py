"""Representative ARI hexapod geometry and analytical IK.

Provenance: sanitized from the read-only engineering tree's hardware-state
geometry module. This portfolio copy keeps measured geometry, joint limits,
and the solver shape, but omits private package structure and hardware IO.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


COXA_LEN_MM = 48.0
FEMUR_LEN_MM = 78.5
TIBIA_LEN_MM = 139.0

COXA_LIMIT_DEG = (45.0, 135.0)
FEMUR_LIMIT_DEG = (30.0, 150.0)
TIBIA_LIMIT_DEG = (30.0, 150.0)


@dataclass(frozen=True)
class Vec3:
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class JointAngles:
    coxa: float
    femur: float
    tibia: float
    reachable: bool


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def solve_leg_ik(target_local: Vec3) -> JointAngles:
    """Solve one 3-DOF leg in a local frame where +y points outward.

    Returned angles are servo-space degrees. The caller must still apply the
    embedded firmware's side-specific trim, inversion, and pulse clamps.
    """

    coxa_deg = math.degrees(math.atan2(target_local.y, target_local.x))
    dist_xy = math.hypot(target_local.x, target_local.y)
    horiz = dist_xy - COXA_LEN_MM
    vert = target_local.z

    upper = FEMUR_LEN_MM
    lower = TIBIA_LEN_MM
    dist = math.hypot(horiz, vert)
    reachable = True

    max_reach = upper + lower - 1.0
    min_reach = abs(upper - lower) + 1.0
    if dist > max_reach:
        reachable = False
        scale = max_reach / dist
        horiz *= scale
        vert *= scale
        dist = max_reach
    elif dist < min_reach:
        reachable = False
        dist = min_reach

    cos_knee = (upper * upper + lower * lower - dist * dist) / (2.0 * upper * lower)
    knee_interior = math.degrees(math.acos(_clamp(cos_knee, -1.0, 1.0)))

    pitch = math.atan2(vert, max(horiz, 0.01))
    cos_alpha = (upper * upper + dist * dist - lower * lower) / (2.0 * upper * dist)
    alpha = math.acos(_clamp(cos_alpha, -1.0, 1.0))
    femur_servo = 90.0 + math.degrees(pitch + alpha)

    return JointAngles(
        coxa=_clamp(coxa_deg, *COXA_LIMIT_DEG),
        femur=_clamp(femur_servo, *FEMUR_LIMIT_DEG),
        tibia=_clamp(knee_interior, *TIBIA_LIMIT_DEG),
        reachable=reachable,
    )
