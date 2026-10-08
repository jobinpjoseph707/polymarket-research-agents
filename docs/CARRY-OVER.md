# What comes from XAutoTrade, and what does not

| Idea | Carried over? | How it looks here |
|---|---|---|
| Agents propose, you approve | Yes | Inbox with Approve / Reject |
| Demo before anything real | Yes | Paper only; real money is not in version 1 |
| Pass marks and counting attempts | Yes | 100 resolved markets; each attempt on the same data raises the bar |
| Scoped lessons (only the same market type) | Yes | Notes are scoped by tag, such as "elections" or "sports" |
| Lessons fade with age | Yes | Old notes lose weight |
| Daily cap on model calls | Yes | Same cap, same refusal |
| Model behind one interface | Yes | Cloud now, a local model later |
| Backtester, candles, indicators | **No** | Not meaningful for yes/no markets |
| Stops, targets, trailing | **No** | A market resolves; there is no stop |
| MT5 bridge | **No** | Replaced by Polymarket's API |
| Risk tiers T1–T5 | Adapted | Caps per market and in total, with linked markets as one bet |
| Node server | **No** | Python throughout |

## What is new here

- The edge is "my probability vs the market's price", not a pattern in candles.
- Resolution rules matter: the exact wording decides who wins. Agents must read and quote them.
- Money is locked until resolution, so capital turns over slowly and sample sizes grow slowly. This is why the pass mark is counted in resolved markets, and why it will take months.
