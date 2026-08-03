# Engineering Process

The project uses small gates instead of broad success claims.

## Pattern

1. Define a measurable contract before a run.
2. Preserve source and asset provenance.
3. Run bounded simulator or hardware-safe tests.
4. Review failures as evidence rather than relabeling them as progress.
5. Promote only when the stated gate passes unchanged thresholds.

## Examples

- Run63 established a deployable-observation simulator walker and remains the canonical historical walker.
- Run64 expanded the simulator speed envelope, but its balance-table gate did not fully pass; the result is reported as speed-envelope evidence, not full balance qualification.
- Run94.8 retained scan-turn qualification as simulator-only evidence using the selected Run94.6 `model_11` checkpoint.
- RunV4 Stage1 force-drive reached 50 optimizer updates, but the forward-displacement gate failed. It is therefore not promoted.

## Validation Philosophy

The core habit is fail-closed validation: if evidence is partial, contaminated, uses relaxed thresholds, or cannot be reproduced from its stated source, it is not promoted. This is why the public snapshot includes negative results and current boundaries.
