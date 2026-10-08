# Test plan

Tests are listed before the code. The group G tests exist now (the skeleton). The rest are written in the phase named.

Rules: no network in tests (fake client, recorded sample responses); a temporary database per test; a fake model.

## G — Guardrails (skeleton, exist now)

| ID | Test |
|---|---|
| G-1 | Default mode is `paper` |
| G-2 | Mode `live` is refused with a clear error |
| G-3 | Unknown mode is refused |
| G-4 | A model-call counter refuses the call after the daily cap |
| G-5 | The counter resets on a new day |
| G-6 | The source scan finds no order-placing function in `src/` |

## P — Collect and store (Phase 1)

| ID | Test |
|---|---|
| P-1 | Market list is stored from a recorded response |
| P-2 | A second run adds no duplicates |
| P-3 | Every snapshot has `known_at` |
| P-4 | Rate limiter spaces calls |
| P-5 | A 429 or 5xx is retried with back-off, then given up cleanly |
| P-6 | Following more than 50 markets is refused |
| P-7 | A resolved market stores its outcome once |
| P-8 | Malformed API data is skipped and counted, not crashed on |

## A — Agents (Phase 2)

| ID | Test |
|---|---|
| A-1 | Full graph runs with a fake model |
| A-2 | Critic can send back to Estimator, and stops after 2 rounds |
| A-3 | Estimator output without a probability is rejected |
| A-4 | A fact without a source is dropped |
| A-5 | A source not on the allow-list is refused |
| A-6 | Estimates are written the moment they are made |
| A-7 | Update or delete on `estimates` fails |
| A-8 | A run reading data sees nothing with `known_at` after its start |
| A-9 | Daily and per-market call caps stop a run |
| A-10 | A crashed run leaves no half-written estimate |
| A-11 | Proposals are stored as pending; nothing applies without approval |
| A-12 | Run steps can be read back in order |

## S — Scoring and paper trading (Phase 3)

| ID | Test |
|---|---|
| S-1 | Brier score matches a hand-worked example |
| S-2 | Market-price baseline is taken at the same time as the estimate |
| S-3 | Calibration buckets and counts are right |
| S-4 | Fewer than 100 resolved markets gives "not enough evidence" |
| S-5 | A paper trade opens only when the gap beats fees plus margin |
| S-6 | Fill walks the stored order book |
| S-7 | Size is a fraction of Kelly and never above the per-market cap |
| S-8 | Total exposure cap holds |
| S-9 | Linked markets count as one bet |
| S-10 | Fees are subtracted from paper profit |
| S-11 | Attempt counter raises the bar |
| S-12 | The report rebuilds from the database alone |

## W — Live data and app (Phase 4)

| ID | Test |
|---|---|
| W-1 | WebSocket reconnects after a drop |
| W-2 | A gap in messages is detected and logged |
| W-3 | Order-book store keeps only the top levels |
| W-4 | Approve and Reject change a proposal's status once |
| W-5 | Dashboard endpoints are read-only except the Inbox |

## Hand checks

- After 7 days of collecting: row counts are sensible and no gaps longer than expected.
- Read three agent threads end to end. Do the reasons make sense?
