# Shared Expense Scenario Comparator

[![CI](https://github.com/loganpendragonmultiverse/shared-expense-scenario-comparator/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/shared-expense-scenario-comparator/actions/workflows/ci.yml)

Compare equal, percentage, income-weighted, usage-weighted, and custom expense splits. The command uses explicit UTF-8 JSON input and produces reviewable JSON or Markdown output.

## Three-minute start

```bash
python -m pip install .
expense-scenarios examples/sample.json
expense-scenarios examples/sample.json --format json --output report.json
```

The example documents the v1 input shape. Existing report files are never overwritten. Source inputs are read-only except where the documented purpose explicitly creates a new output artifact.

## Privacy and platforms

The tool runs locally and does not upload input or include telemetry. Python 3.10 or newer is supported on Windows, macOS, and Linux.

## Interpretation boundary

Results are arithmetic scenarios, not financial, tax, or legal advice. Participants must agree on the inputs and rounding policy.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).

## 1.0.1 — 2026-10-16

Amounts and every supplied weight must be finite and non-negative; each complete weighted scenario must have a positive weight total. Amounts retain nearest-cent rounding with ties to even. Splits use exact rational cent quotas derived from Decimal values: floor each quota, then award remaining cents by descending fractional remainder, breaking equal remainders by participant input order. Three cents across five equal participants therefore gives 0.01, 0.01, 0.01, 0.00, 0.00. Every scenario conserves the rounded total without a negative residual. The rounding report records the input amount, rounded cent total, exact amount adjustment (a rational string), floors, remainder count and extra-cent recipients. JSON numeric decimals are parsed exactly. Percentage and custom values remain relative weights; participants must agree on inputs and this rounding policy. Results remain local arithmetic scenarios without payment, banking, exchange-rate or tax operations.
