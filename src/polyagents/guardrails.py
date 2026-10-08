"""Rules that cannot be switched off in version 1.

- The mode is paper. Any other value is refused.
- Model calls are counted per day and refused after the cap.
"""
from __future__ import annotations

from datetime import date

ALLOWED_MODES = ("paper",)
DEFAULT_MODE = "paper"


class GuardrailError(Exception):
    """Raised when a rule would be broken."""


def check_mode(mode: str | None = None) -> str:
    """Return the mode if allowed, otherwise raise."""
    mode = DEFAULT_MODE if mode is None else mode
    if mode == "live":
        raise GuardrailError(
            "live mode is not available in version 1; this project is paper only"
        )
    if mode not in ALLOWED_MODES:
        raise GuardrailError(f"unknown mode {mode!r}; allowed: {ALLOWED_MODES}")
    return mode


class CallCounter:
    """Counts model calls per day. Refuses the call that would pass the cap."""

    def __init__(self, daily_cap: int, today=date.today):
        if daily_cap < 1:
            raise ValueError("daily_cap must be at least 1")
        self.daily_cap = daily_cap
        self._today = today
        self._day = today()
        self.used = 0

    def take(self) -> int:
        """Use one call. Returns calls used today, or raises at the cap."""
        now = self._today()
        if now != self._day:
            self._day = now
            self.used = 0
        if self.used >= self.daily_cap:
            raise GuardrailError(f"daily model-call cap reached ({self.daily_cap})")
        self.used += 1
        return self.used
