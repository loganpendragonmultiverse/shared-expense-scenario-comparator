# Testing

Run the repository CI commands: ruff format --check ., ruff check ., mypy src, pytest and python -m build.

## 1.0.1 — 2026-10-16

Amounts and every supplied weight must be finite and non-negative; each complete weighted scenario must have a positive weight total. Amounts retain nearest-cent rounding with ties to even. Splits use exact rational cent quotas derived from Decimal values: floor each quota, then award remaining cents by descending fractional remainder, breaking equal remainders by participant input order. Three cents across five equal participants therefore gives 0.01, 0.01, 0.01, 0.00, 0.00. Every scenario conserves the rounded total without a negative residual. The rounding report records the input amount, rounded cent total, exact amount adjustment (a rational string), floors, remainder count and extra-cent recipients. JSON numeric decimals are parsed exactly. Percentage and custom values remain relative weights; participants must agree on inputs and this rounding policy. Results remain local arithmetic scenarios without payment, banking, exchange-rate or tax operations.

Regression tests use synthetic inputs and disposable trees. Run the complete suite and inspect built wheel/source documentation before preparing a draft PR.

## 1.0.2 regressions

Test malformed JSON roots and containers, clean CLI diagnostics, existing files,
dangling output links and a deterministic concurrent report-creation boundary.
Inspect and install the actual wheel and source distribution outside the checkout;
verify all four documents, the sample, license, CLI output and unchanged inputs.

Retain exact-cent conservation, ties-to-even amount rounding, largest-remainder
allocation and participant-order tie breaking for every existing scenario.

A subprocess regression closes the stdout reader before execution and requires
status 2 without a traceback or interpreter-shutdown warning.

A small-report subprocess regression writes stdout to /dev/full and requires
status 2 without an interpreter-shutdown warning; skip when the device is absent.

Keep the real dangling-output-link check enabled on Windows when symlink creation
is available. Also simulate an exclusive-open implementation that follows an
existing dangling link, requiring status 2 and an unchanged link/missing target.
