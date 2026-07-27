from __future__ import annotations

import json
from decimal import Decimal
from typing import Any

PROJECT = "shared-expense-scenario-comparator"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _expense_scenarios(data: dict[str, Any]) -> dict[str, Any]:
    amount = Decimal(str(_require(data, "amount")))
    participants = _require(data, "participants")
    if amount < 0 or not participants:
        raise ValueError("amount must be non-negative and participants are required")
    names = [str(_require(item, "name")) for item in participants]
    if len(names) != len(set(names)):
        raise ValueError("participant names must be unique")

    def split(weights: list[Decimal]) -> dict[str, str]:
        total = sum(weights)
        if total <= 0:
            raise ValueError("scenario weights must total more than zero")
        raw = [amount * weight / total for weight in weights]
        cents = [value.quantize(Decimal("0.01")) for value in raw]
        cents[-1] += amount.quantize(Decimal("0.01")) - sum(cents)
        return dict(zip(names, map(str, cents)))

    scenarios = {"equal": split([Decimal(1)] * len(participants))}
    for field, label in (
        ("income", "income_weighted"),
        ("usage", "usage_weighted"),
        ("percentage", "percentage"),
        ("custom", "custom"),
    ):
        if all(field in item for item in participants):
            scenarios[label] = split([Decimal(str(item[field])) for item in participants])
    return {
        "amount": str(amount.quantize(Decimal("0.01"))),
        "currency": data.get("currency", "USD"),
        "scenarios": scenarios,
    }


def analyze(data: dict[str, Any]) -> dict[str, Any]:
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
