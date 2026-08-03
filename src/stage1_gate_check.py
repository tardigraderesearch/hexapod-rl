"""Small public example of fail-closed Stage1 promotion logic.

This is not the production evaluator. It mirrors the portfolio-level rule that
training updates alone do not promote a checkpoint when a behavioral gate fails.
"""

from __future__ import annotations


def stage1_promoted(
    accepted_updates: int,
    forward_displacement_m: float,
    forward_gate_m: float = 0.005,
    simulator_only: bool = True,
) -> bool:
    """Return True only when the minimum public promotion contract is met."""

    if not simulator_only:
        return False
    if accepted_updates < 50:
        return False
    return forward_displacement_m >= forward_gate_m


def stage1_status_message(accepted_updates: int, forward_displacement_m: float) -> str:
    promoted = stage1_promoted(accepted_updates, forward_displacement_m)
    if promoted:
        return "simulator gate passed; still not hardware-cleared"
    return "not promoted: forward displacement gate failed or evidence is incomplete"
