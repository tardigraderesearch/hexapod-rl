# Reproducibility

This repository is not a full reproduction package. It is a public portfolio snapshot.

## What Can Be Reproduced Here

- Parse and inspect the conservative metrics file.
- Read representative control, observation, and evaluator examples.
- Run the public repository validator.
- Review simulator media from the Run63 capture.

## What Is Not Included

- Isaac Lab runtime environment.
- Full URDF/USD asset tree.
- Training run directories.
- Model checkpoints.
- Operational firmware or hardware deployment scripts.
- Private source paths, machine identifiers, and local vault internals.

## Validation Command

```bash
python3 scripts/validate_public_repo.py
```

The validator checks required files, metrics structure, explicit simulator-only and non-promoted language, file-size limits, path leakage, secret-like strings, model/checkpoint binaries, controller identifiers, and accidental nested Git directories.
