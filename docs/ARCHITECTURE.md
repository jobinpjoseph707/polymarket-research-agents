# Architecture

```
 Polymarket public API (REST now, WebSocket in phase 4)
            │
            ▼
 ┌──────────────────────┐        ┌──────────────────────────┐
 │ collector            │        │ agents (LangGraph)       │
 │ one place that calls │        │ Researcher → Estimator → │
 │ the API, rate-limits │        │ Critic → Risk Guard      │
 └──────────┬───────────┘        └────────────┬─────────────┘
            │ writes                          │ reads market data, writes estimates + proposals
            ▼                                 ▼
 ┌───────────────────────────────────────────────────────────┐
 │ SQLite  polyagents.db   (checkpoints in agents.db)        │
 └──────────┬───────────────────────────┬────────────────────┘
            │                           │
            ▼                           ▼
 ┌──────────────────────┐   ┌──────────────────────────┐
 │ scorer + paper trader│   │ API (FastAPI) + dashboard │
 │ Brier, calibration,  │   │ Inbox: Approve / Reject   │
 │ fees, order-book fill│   └──────────────────────────┘
 └──────────────────────┘
```

## Parts

| Part | Folder | Job |
|---|---|---|
| Config and guardrails | `src/polyagents/config.py`, `guardrails.py` | Settings, and the rules that cannot be turned off in version 1 |
| Collector | `collector/` | Fetch, rate-limit, store |
| Storage | `store/` | SQLite access, migrations |
| Agents | `agents/` | Graph, state, prompts, model interface |
| Scoring | `scoring/` | Brier, calibration, attempt counter |
| Paper trader | `paper/` | Fills from stored order books, sizing |
| API | `api/` | Endpoints for the dashboard |

## Tables (planned)

| Table | Holds |
|---|---|
| `markets` | id, question, outcomes, end date, resolution text, tags, state |
| `snapshots` | market id, price per outcome, top order-book levels, `known_at` |
| `follows` | the markets being followed |
| `resolutions` | market id, outcome, resolved time |
| `estimates` | append-only: market id, probability, range, reasons, run id, created time. No update or delete. |
| `runs` | one agent run: steps, calls used, result |
| `paper_trades` | open and close, price, size, fee, reason |
| `attempts` | what was tried, on which resolved markets |
| `proposals` | what an agent wants changed, status, who decided |

## Rules the code enforces

1. `estimates` is append-only (a database trigger refuses update and delete).
2. Time order: an agent reading a market sees only rows with `known_at` earlier than the run's start.
3. There is no order-placing function in the code. A test searches for one.
4. Sizes come from one function. It caps each market and the total, and treats linked markets as one bet.
5. The agents have no write access except estimates, runs and proposals.
6. Daily call cap is checked before every model call.

## Agent state (one object passed along the graph)

`market`, `facts[]` (text, source, published date), `estimate`, `range`, `would_change_mind`, `objections[]`, `round`, `final`, `calls_used`.

## Technology

| Part | Choice | Reason |
|---|---|---|
| Python 3.12 | | The Polymarket client and LangGraph are Python |
| LangGraph | | Agents that share state and loop with a limit |
| httpx | | Async requests with timeouts |
| SQLite | | One file, easy to back up and to test |
| FastAPI | | Small typed API |
| pytest | | Same habit as XAutoTrade's tests |
| Docker | | Anyone can run it in paper mode |
