# Shared Expense Scenario Comparator

> ⭐ **Gold Star Project — v1.0.2**
> I consider this project complete. Fixes, maintenance and good new ideas are still welcome.
> [About Gold Stars](https://www.loganpendragonforge.com/open-source/?gold=1)
>
> Compare explicit expense splits locally with exact cent allocation and reviewable reports.


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

## Report and installation contract (1.0.2)

The input root must be a JSON object. Invalid input produces `error:` on stderr
and exit status 2 without creating a report. Existing output symlinks are rejected explicitly before exclusive file creation.
Exclusive creation refuses existing ordinary files and ordinary files created
between validation and writing. Symlink checks and creation are separate operations;
concurrent link or parent-directory replacement is outside this guarantee. Parent directories must already exist. An interrupted
or failed write can leave a partial newly created report; multiple-file atomicity
and filesystem rollback are not provided.

Install a downloaded wheel with `python -m pip install /path/to/package.whl`,
or install the source distribution with `python -m pip install /path/to/package.tar.gz`.
Wheel installs include README, DEVELOPMENT, TESTING and CHANGELOG under
`sysconfig.get_path("data")/share/doc/shared-expense-scenario-comparator`, with the sample in `examples/sample.json`.
The source distribution contains the same documents and example. Inputs stay local;
no telemetry or network retrieval is added.

A failed stdout write or flush returns status 2 without a shutdown traceback,
including a closed reader or a full output device.
