#!/usr/bin/env python3
"""Validate that this public portfolio snapshot stays small and sanitized."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_FILE_BYTES = 25 * 1024 * 1024

REQUIRED_FILES = [
    "README.md",
    "docs/architecture.md",
    "docs/engineering-process.md",
    "docs/results.md",
    "docs/safety-and-limitations.md",
    "docs/reproducibility.md",
    "evidence/metrics.json",
    "LICENSE",
    ".gitignore",
    "CITATION.cff",
    "scripts/validate_public_repo.py",
]

TEXT_SUFFIXES = {
    ".cff",
    ".css",
    ".html",
    ".ino",
    ".js",
    ".json",
    ".md",
    ".py",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
]

PATH_PATTERNS = [
    re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/][^\s)>\"]+"),
    re.compile("/" + "mnt" + r"/[a-z]/[^\s)>\"]+"),
]

FORBIDDEN_MAC = ":".join(["dc", "b4", "d9", "14", "27", "d4"])
FORBIDDEN_BINARY_SUFFIXES = {".pt", ".pth", ".onnx", ".engine", ".ckpt", ".bin", ".npz", ".npy"}


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        parts = path.relative_to(ROOT).parts
        if parts and parts[0] == ".git":
            continue
        if "__pycache__" in parts:
            continue
        files.append(path)
    return files


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def validate_required(errors: list[str]) -> None:
    for name in REQUIRED_FILES:
        if not (ROOT / name).is_file():
            errors.append(f"missing required file: {name}")


def validate_metrics(errors: list[str]) -> None:
    path = ROOT / "evidence" / "metrics.json"
    try:
        metrics = json.loads(read_text(path))
    except Exception as exc:
        errors.append(f"metrics JSON did not parse: {exc}")
        return

    platform = metrics.get("physical_platform", {})
    if platform.get("legs") != 6 or platform.get("total_dof") != 18:
        errors.append("metrics must verify 6 legs and 18 DOF")

    status = metrics.get("overall_status", {})
    if status.get("learned_locomotion_status") != "simulator-only":
        errors.append("metrics must mark learned locomotion simulator-only")
    if status.get("hardware_policy_deployment_cleared") is not False:
        errors.append("metrics must say hardware policy deployment is not cleared")

    stage1 = metrics.get("stage1_safe_025", {})
    if stage1.get("promotion") is not False or stage1.get("status") != "not promoted":
        errors.append("stage1_safe_025 must be explicitly not promoted")
    if stage1.get("accepted_optimizer_updates") != 50:
        errors.append("stage1_safe_025 must record 50 accepted optimizer updates")
    if float(stage1.get("forward_gate_m", -1)) != 0.005:
        errors.append("stage1_safe_025 must record the 0.005 m forward gate")


def validate_language(errors: list[str]) -> None:
    combined = "\n".join(
        read_text(path)
        for path in iter_files()
        if path.suffix.lower() in TEXT_SUFFIXES
    ).lower()
    for phrase in ["simulator-only", "not promoted", "autonomous hardware motion is prohibited"]:
        if phrase not in combined:
            errors.append(f"missing required explicit language: {phrase}")


def validate_sanitization(errors: list[str]) -> None:
    for path in iter_files():
        rel = relative(path)
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"file exceeds 25 MiB: {rel}")
        if ".git" in path.relative_to(ROOT).parts and rel != ".gitignore":
            if path.relative_to(ROOT).parts[0] != ".git":
                errors.append(f"nested git metadata found: {rel}")
        if path.suffix.lower() in FORBIDDEN_BINARY_SUFFIXES:
            errors.append(f"forbidden model/checkpoint/binary artifact: {rel}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        text = read_text(path)
        lowered = text.lower()
        if FORBIDDEN_MAC in lowered:
            errors.append(f"forbidden controller identifier found: {rel}")
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                errors.append(f"secret-like pattern found: {rel}")
                break
        for pattern in PATH_PATTERNS:
            if pattern.search(text):
                errors.append(f"absolute local path found: {rel}")
                break


def main() -> int:
    errors: list[str] = []
    validate_required(errors)
    validate_metrics(errors)
    validate_language(errors)
    validate_sanitization(errors)

    if errors:
        print("PUBLIC REPO VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PUBLIC REPO VALIDATION PASSED")
    print(f"checked_files={len(iter_files())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
