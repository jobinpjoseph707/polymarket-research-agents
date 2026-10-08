# Plan

Written 8 October 2026. Four phases, built in order. Each phase ends with something you can run and a test report.

## Facts checked, and facts not yet checked

Only the first block was read from Polymarket's own documentation. Everything in the second block must be read and confirmed **before** the phase that uses it.

| Checked (Polymarket docs, 8 Oct 2026) |
|---|
| Public market-list API: Gamma, base `https://gamma-api.polymarket.com`, with a keyset-paged markets list |
| Official clients exist: Python package `polymarket` (`AsyncPublicClient`, `list_markets()`); TypeScript `@polymarket/client` |
| Doc index for further reading: `docs.polymarket.com/llms.txt`; status page `status.polymarket.com` |

| NOT checked — verify first | Needed by |
|---|---|
| Order-book (CLOB) REST endpoints and their response shape | Phase 1 |
| WebSocket channels (market data), message format, reconnect rules | Phase 3 |
| Rate limits | Phase 1 |
| How and when a market resolves, who decides, and what happens in a dispute | Phase 2 |
| Fee schedule | Phase 1 (paper fills) |
| Regions where Polymarket is blocked or restricted, including the UAE; terms of use for API data | Before any real-money step |
| Whether there is a separate API for US users (`docs.polymarket.us`) | Only if it applies to you |

The README and this plan say "will" for design and "is" only for the checked block.

## Principles (same as XAutoTrade)

1. Agents propose; you approve. Talking is free, acting is gated.
2. Paper first. A real-money step is a separate, later decision and is **not** in this plan.
3. Every number is shown with how many cases it rests on.
4. Every estimate is saved before the outcome is known and cannot be edited.
5. No profit is promised anywhere.

---

## Phase 1 — Collect and store (read only)

**Result:** a database of markets and prices that grows by itself, and a page that lists them.

| # | Task |
|---|---|
| 1.1 | Project skeleton: package, config, SQLite, pytest, Docker file. |
| 1.2 | Market list: fetch all open markets through the public API, store question, outcomes, end date, resolution rules text, tags. |
| 1.3 | Price snapshots: every N minutes store the price and the order-book top levels for markets you follow. Each row stores `known_at`. |
| 1.4 | Follow list: you choose up to 50 markets to follow. |
| 1.5 | Polite fetching: rate limit, retry with back-off, one place that calls the API. |
| 1.6 | Resolution tracker: when a followed market resolves, store the outcome and the time. |

Done when: snapshots run for 7 days unattended; a second run adds no duplicates; tests P-1 to P-8 pass.

## Phase 2 — Agents that talk (still no money)

**Result:** for each followed market, a saved reasoning thread and a probability.

| # | Task |
|---|---|
| 2.1 | Shared state per market: facts, sources, estimate, objections, final. |
| 2.2 | Graph: Researcher → Estimator → Critic → (back to Estimator, max 2) → Risk Guard. |
| 2.3 | Researcher uses only sources you allow (a list in config). Every fact carries its source and the date it was published. |
| 2.4 | Estimator must give a probability, a range, and "what would change my mind". |
| 2.5 | Estimates are written to an append-only table the moment they are made. |
| 2.6 | Cap on model calls per day and per market. |
| 2.7 | Model access through one small interface so any model can sit behind it (cloud now, a local one later). |

Done when: a full run works with a fake model and no network; tests A-1 to A-12 pass.

## Phase 3 — Scoring and paper trading

**Result:** an honest report of whether the agents beat the market price.

| # | Task |
|---|---|
| 3.1 | When a market resolves, score every estimate: Brier score, and the market price at that time as the baseline. |
| 3.2 | Calibration table by bucket (0–10%, 10–20%, …) with counts. |
| 3.3 | Paper trader: a position opens only when the estimate and the market differ by more than fees plus a margin. Fills use the saved order book, not the mid price. |
| 3.4 | Size rule: a fraction of the Kelly size, hard-capped per market and in total; markets that depend on each other count as one bet. |
| 3.5 | Attempt counter: each new prompt or rule tried on the same resolved markets raises the bar. |
| 3.6 | Report page: "not enough evidence" until 100 resolved markets. |

Done when: the report can be rebuilt from the database alone; tests S-1 to S-12 pass.

## Phase 4 — Live order book and the app

**Result:** a dashboard and live depth for followed markets.

| # | Task |
|---|---|
| 4.1 | WebSocket client for market data with reconnect and gap detection. |
| 4.2 | Order-book store, kept small (top levels, sampled). |
| 4.3 | Inbox: proposals from the agents, Approve / Reject. |
| 4.4 | Web dashboard (read-only plus Inbox). |
| 4.5 | Docker compose: one command starts everything in paper mode. |

## Not in this plan

- Real orders, wallets, keys or funds. If this is ever wanted it needs its own written decision, a region and legal check, and a new set of tests that prove the limits.
- A promise that any of it makes money.

## Open question for the owner

Should the agents run continuously on every followed market, or once per day per market plus when a market's price moves a lot? Default used here: once per day plus on a large price move, to keep model calls low.
