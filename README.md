# polymarket-research-agents

A research system for prediction markets. Several AI agents study Polymarket markets, argue about them, and write down a probability for each. Every estimate is scored against what actually happened. **It starts in paper mode and has no way to place a real order.**

> **Status: planning.** This repo holds the plan and a small tested skeleton (the safety rules). The agents, data collection and paper trading are built in the phases in [`PLAN.md`](PLAN.md). Nothing here is financial advice, and nothing here promises profit. Most people who trade prediction markets lose money.

Sister project: [`xautotrade`](https://github.com/jobinpjoseph707/xautotrade) (gold and forex strategies on MetaTrader 5). This repo is separate on purpose; see [Why a separate repo](#why-a-separate-repo).

---

## What it does

1. **Collects** market data from Polymarket's public REST API and stores it in SQLite, with the time each piece was known.
2. **Agents talk to each other** (Python + LangGraph): a Researcher gathers facts, an Estimator gives a probability, a Critic attacks it, and a Risk Guard checks size. They share one state and one memory per market.
3. **Records every estimate** before the market resolves, so nothing can be edited afterwards.
4. **Scores itself**: Brier score and a calibration table. If the agents are no better than the market price, the app says so.
5. **Paper trades** the estimates that survive, with fees and the real order book, and shows the result.
6. **Asks you** before anything changes. Agents propose; you approve.

## What it will not do

- Place real orders. There is no code path for it in version 1, and a test fails if one appears.
- Hold a wallet or private key. Paper mode needs no account.
- Promise an edge. A market price is already a probability that many people have tried to beat.

## How the agents work

```
Market ──► Researcher ──► Estimator ──► Critic ──► Risk Guard ──► Proposal ──► You
            facts +        probability   attacks     size, cap,     in the
            sources        + reasons     the reasons  correlation    Inbox
                 ▲                         │
                 └─────── sent back (max 2 times) ───────┘
```

Every step is saved, so you can read who said what and why.

## Scoring, in plain words

| Number | Meaning | Good looks like |
|---|---|---|
| Brier score | Average squared error of the probabilities. Lower is better. | Lower than the market's own price over the same markets |
| Calibration | Of the things said to be 70% likely, did about 70% happen? | A straight line |
| Paper profit after fees | What the paper trades earned | Positive over 100+ resolved markets, not 10 |
| Attempts | How many versions were tried on the same data | Shown next to every result |

A result with fewer than 100 resolved markets is shown as "not enough evidence".

## Tech

| Part | Choice |
|---|---|
| Language | Python 3.12 |
| Agents | LangGraph |
| Data | Polymarket public REST (Gamma), then WebSocket for live order books |
| Storage | SQLite (one file) |
| API | FastAPI |
| Tests | pytest |
| Run | Docker, paper mode by default |

## Quick start (skeleton)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Documents

| File | What it is |
|---|---|
| [`PLAN.md`](PLAN.md) | The phases, what each delivers, and what is still unverified |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Parts, data tables, flows |
| [`docs/TEST-PLAN.md`](docs/TEST-PLAN.md) | Every test, listed before it is written |
| [`docs/CARRY-OVER.md`](docs/CARRY-OVER.md) | What comes from XAutoTrade and what does not |
| [`docs/DECISIONS.md`](docs/DECISIONS.md) | Short records: why this, not that |

## Why a separate repo

A prediction market resolves to yes or no on a date. It has no candles, stops or indicators, and the money model is different. Sharing a codebase with a trading-strategy engine would mean twisting one of them. What carries over is the *discipline*: agents propose, you approve, everything is measured, paper first.

## Before you use real money anywhere

Check whether Polymarket is available in your country and whether using it is legal for you. Rules differ by region and change. This repo does not answer that for you.

## Licence

MIT.
