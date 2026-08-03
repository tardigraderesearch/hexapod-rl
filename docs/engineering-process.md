# Engineering Process

The project uses small gates instead of broad success claims.

## Pattern

1. Define a measurable contract before a run.
2. Preserve source and asset provenance.
3. Run bounded simulator or hardware-safe tests.
4. Review failures as evidence rather than relabeling them as progress.
5. Promote only when the stated gate passes unchanged thresholds.

## Examples

- August 3, 2026 correction: rendered simulator evidence exposed a frame-sign mismatch in the legacy Run63 handoff/trainer. The physical robot convention is body +X as forward, but the legacy evaluator treated URDF -X displacement as positive command-vx progress.
- Run63 remains a canonical historical deployable-observation simulator policy only under the legacy -X evaluator axis, backward relative to the physical chassis front.
- Run64 remains simulator speed-envelope evidence only under the legacy -X evaluator axis; it is not physical-forward speed evidence or full balance qualification.
- Run104 completed 500 updates across 2,048 environments and 24,576,000 transitions, with update 100 selected within the legacy-axis campaign; it is not a physical-forward champion.
- Run105 completed 500 updates under the invalid legacy-axis convention, but no candidate was promoted and the parent was retained; it is not reported as speed progress.
- Run94.8 retained scan-turn qualification as simulator-only evidence using the selected Run94.6 `model_11` checkpoint.
- RunV4 Stage1 force-drive reached 50 optimizer updates, but the forward-displacement gate failed. It is therefore not promoted.

## Validation Philosophy

The core habit is fail-closed validation: if evidence is partial, contaminated, uses relaxed thresholds, or cannot be reproduced from its stated source, it is not promoted. This is why the public snapshot includes negative results and current boundaries.

Physical-forward learned locomotion capability is reopened pending +X-corrected retraining and validation. No learned policy is cleared for hardware.
