# Changelog

## [1.0.2] - 2026-10-19

- Handle failed stdout writes and flushes without an interpreter-shutdown traceback.
- Reject non-object JSON input with a concise CLI error.
- Create reports exclusively so existing files, dangling symlinks and concurrently created reports are preserved.
- Ship the sample alongside the installed handoff documents.

## [1.0.1] - 2026-10-16

Amounts and every supplied weight must be finite and non-negative; each complete weighted scenario must have a positive weight total. Amounts retain nearest-cent rounding with ties to even. Splits use exact rational cent quotas derived from Decimal values: floor each quota, then award remaining cents by descending fractional remainder, breaking equal remainders by participant input order. Three cents across five equal participants therefore gives 0.01, 0.01, 0.01, 0.00, 0.00. Every scenario conserves the rounded total without a negative residual. The rounding report records the input amount, rounded cent total, exact amount adjustment (a rational string), floors, remainder count and extra-cent recipients. JSON numeric decimals are parsed exactly. Percentage and custom values remain relative weights; participants must agree on inputs and this rounding policy. Results remain local arithmetic scenarios without payment, banking, exchange-rate or tax operations.


## 1.0.0 - 2026-07-26

- Released the first complete Shared Expense Scenario Comparator command-line workflow.
- Added deterministic reporting, representative examples, cross-platform tests, and explicit limitations.
