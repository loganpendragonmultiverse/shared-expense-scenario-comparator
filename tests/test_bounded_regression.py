import json
from decimal import Decimal

import pytest

from expense_scenario_comparator.cli import main
from expense_scenario_comparator.core import analyze


def test_three_cents_five_equal_shares_are_conserved_without_negative_residual():
    report = analyze({"amount": "0.03", "participants": [{"name": str(i)} for i in range(5)]})
    assert list(report["scenarios"]["equal"].values()) == ["0.01", "0.01", "0.01", "0.00", "0.00"]
    assert sum(map(Decimal, report["scenarios"]["equal"].values())) == Decimal("0.03")


@pytest.mark.parametrize("bad", ["NaN", "Infinity", "-Infinity", "-0.01", True, "invalid"])
@pytest.mark.parametrize("field", ["amount", "income", "usage", "percentage", "custom"])
def test_nonnegative_finite_numbers_required(bad, field):
    data = {"amount": "1.00", "participants": [{"name": "a"}, {"name": "b"}]}
    if field == "amount":
        data[field] = bad
    else:
        for participant in data["participants"]:
            participant[field] = bad
    with pytest.raises(ValueError):
        analyze(data)


@pytest.mark.parametrize("cents", [0, 1, 2, 3, 5, 99, 100, 101, 100003])
@pytest.mark.parametrize("weights", [[1, 1, 1, 1, 1], [0, 2, 3, 7, 0], [1, 2, 3, 4, 5]])
def test_cent_conservation_and_rounding_evidence(cents, weights):
    participants = [{"name": str(i), "custom": str(w)} for i, w in enumerate(weights)]
    report = analyze({"amount": str(Decimal(cents) / 100), "participants": participants})
    for scenario in report["scenarios"].values():
        values = list(map(Decimal, scenario.values()))
        assert min(values) >= 0 and sum(values) == Decimal(cents) / 100
    assert report["rounding"]["scenarios"]["custom"]["allocated_cents"] == cents
    assert report == analyze({"amount": str(Decimal(cents) / 100), "participants": participants})


@pytest.mark.parametrize(
    "amount,rounded", [("0.005", "0.00"), ("0.015", "0.02"), ("0.025", "0.02")]
)
def test_amount_rounding_retains_half_even_policy(amount, rounded):
    report = analyze({"amount": amount, "participants": [{"name": "a"}]})
    assert report["amount"] == rounded
    assert report["rounding"]["input_amount"] == amount


def test_cli_invalid_weights_have_no_output(tmp_path, capsys):
    source, output = tmp_path / "source.json", tmp_path / "output.json"
    source.write_text(
        json.dumps(
            {
                "amount": "0.03",
                "participants": [{"name": "a", "custom": "-1"}, {"name": "b", "custom": "2"}],
            }
        )
    )
    assert main([str(source), "--output", str(output)]) == 2
    captured = capsys.readouterr()
    assert not output.exists() and not captured.out and "finite non-negative" in captured.err


def test_partial_weight_is_validated_and_large_decimal_is_exact():
    with pytest.raises(ValueError):
        analyze({"amount": 1, "participants": [{"name": "a", "income": -1}, {"name": "b"}]})
    amount = "123456789012345678901234567890.03"
    result = analyze({"amount": amount, "participants": [{"name": str(i)} for i in range(5)]})
    assert result["amount"] == amount
    assert (
        result["rounding"]["scenarios"]["equal"]["allocated_cents"]
        == 12345678901234567890123456789003
    )
