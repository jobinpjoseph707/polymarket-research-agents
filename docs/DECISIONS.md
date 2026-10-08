# Decisions

## 1. Separate repo from XAutoTrade
Different market model, different data, different language. Shared discipline, not shared code.

## 2. Python and LangGraph
The agents must share state and respond to each other, which is what LangGraph is for. The Polymarket client is also in Python. Rust or Go would help only if latency mattered; here it does not (see 3).

## 3. REST first, WebSocket later
The questions are about hours and days, not milliseconds. REST snapshots are enough to learn whether the agents have any skill. WebSocket depth is added in Phase 4 for realistic paper fills.

## 4. SQLite
One file, append-only estimates, easy to test. Same choice as XAutoTrade.

## 5. Paper only in version 1
There is no order-placing code. A test checks this. Going live would be a separate written decision, after a region and legal check.

## 6. Score against the market, not against zero
An agent that matches the market price adds nothing. The baseline is the market's own price at the same moment.

## 7. Estimates are written before the outcome and cannot change
Otherwise results can be quietly improved afterwards.

## 8. No promise of profit, no promise of stars
The README says what is built and what is measured.
