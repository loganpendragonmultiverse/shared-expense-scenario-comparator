from __future__ import annotations

import json
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from typing import Any

PROJECT = "shared-expense-scenario-comparator"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _number(value: Any, field: str) -> Decimal:
    try:
        if isinstance(value, bool):
            raise TypeError(f"{field} must be a finite non-negative number")
        number = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be a finite non-negative number") from exc
    if not number.is_finite() or number < 0:
        raise ValueError(f"{field} must be a finite non-negative number")
    return number


def _money(cents: int) -> str:
    return f"{cents // 100}.{cents % 100:02d}"


def _expense_scenarios(data: dict[str, Any]) -> dict[str, Any]:
    amount = _number(_require(data, "amount"), "amount")
    participants = _require(data, "participants")
    if not isinstance(participants, list) or not all(isinstance(p, dict) for p in participants):
        raise ValueError("participants must be a non-empty list of objects")
    names = [str(_require(item, "name")) for item in participants]
    if len(names) != len(set(names)):
        raise ValueError("participant names must be unique")
    # Fraction preserves Decimal's exact value independently of decimal context.
    total_cents = round(Fraction(amount) * 100)
    evidence: dict[str, Any] = {}

    def split(weights: list[Decimal], label: str) -> dict[str, str]:
        exact_weights = [Fraction(weight) for weight in weights]
        total = sum(exact_weights)
        if total <= 0:
            raise ValueError("scenario weights must total more than zero")
        quotas = [total_cents * weight / total for weight in exact_weights]
        floors = [quota.numerator // quota.denominator for quota in quotas]
        remainder = total_cents - sum(floors)
        order = sorted(range(len(names)), key=lambda i: (-(quotas[i] - floors[i]), i))
        recipients = order[:remainder]
        cents = floors.copy()
        for index in recipients:
            cents[index] += 1
        evidence[label] = {
            "floor_cents": dict(zip(names, floors)),
            "remainder_cents": remainder,
            "extra_cent_recipients": [names[i] for i in recipients],
            "allocated_cents": sum(cents),
        }
        return dict(zip(names, map(_money, cents)))

    scenarios = {"equal": split([Decimal(1)] * len(participants), "equal")}
    for field, label in (
        ("income", "income_weighted"),
        ("usage", "usage_weighted"),
        ("percentage", "percentage"),
        ("custom", "custom"),
    ):
        # Validate every supplied weight even when this scenario is incomplete.
        values = [_number(item[field], field) for item in participants if field in item]
        if len(values) == len(participants):
            scenarios[label] = split(values, label)
    return {
        "amount": _money(total_cents),
        "currency": data.get("currency", "USD"),
        "scenarios": scenarios,
        "rounding": {
            "input_amount": str(amount),
            "amount_policy": "Nearest cent, ties to even",
            "amount_cents": total_cents,
            "amount_adjustment": str(Fraction(total_cents, 100) - Fraction(amount)),
            "allocation_policy": "Floor exact cent quotas, then largest fractional remainder",
            "tie_break": "Participant input order",
            "scenarios": evidence,
        },
    }


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("input must be a JSON object")  # noqa: TRY004 - CLI input validation
    return {"version": 1, "project": PROJECT, **_expense_scenarios(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False, default=str) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.extend(
                [
                    f"## {key.replace('_', ' ').title()}",
                    "",
                    f"```json\n{json.dumps(value, indent=2, ensure_ascii=False, default=str)}\n```",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"
