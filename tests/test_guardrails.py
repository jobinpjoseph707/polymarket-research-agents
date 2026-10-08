from datetime import date, timedelta
from pathlib import Path

import pytest

from polyagents.guardrails import (
    CallCounter,
    GuardrailError,
    check_mode,
)


def test_g1_default_mode_is_paper():
    assert check_mode() == "paper"


def test_g2_live_mode_is_refused():
    with pytest.raises(GuardrailError, match="paper only"):
        check_mode("live")


def test_g3_unknown_mode_is_refused():
    with pytest.raises(GuardrailError, match="unknown mode"):
        check_mode("demo")


def test_g4_counter_refuses_after_cap():
    c = CallCounter(2, today=lambda: date(2026, 10, 8))
    assert c.take() == 1
    assert c.take() == 2
    with pytest.raises(GuardrailError, match="cap reached"):
        c.take()


def test_g5_counter_resets_on_new_day():
    day = {"d": date(2026, 10, 8)}
    c = CallCounter(1, today=lambda: day["d"])
    c.take()
    with pytest.raises(GuardrailError):
        c.take()
    day["d"] += timedelta(days=1)
    assert c.take() == 1


def test_g6_no_order_placing_function_in_source():
    src = Path(__file__).resolve().parents[1] / "src"
    banned = ("place_order", "create_order", "post_order", "submit_order", "private_key")
    hits = []
    for f in src.rglob("*.py"):
        text = f.read_text()
        for word in banned:
            # "private_key" may be named in a refusal message; defining functions is what we forbid
            if f"def {word}" in text or (word == "private_key" and f"{word} =" in text):
                hits.append((f.name, word))
    assert hits == []
