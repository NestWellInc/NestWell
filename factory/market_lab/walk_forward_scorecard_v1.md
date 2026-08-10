# Market Lab Walk-Forward Scorecard v1

Research/paper-trading only. No live orders.

## Dataset split
For each ETF independently, split chronological daily data:
- Discovery: first 60%
- Validation: next 20%
- Untouched test: final 20%

Never tune parameters on the untouched test segment.

## Candidate families
1. Trend: simple fast/slow moving-average regime.
2. Breakout: enter after a defined closing high; use an explicit exit rule before graduation.
3. Mean reversion: defined multi-day pullback only within a positive long-term regime; use explicit recovery/time exits before graduation.

## Required metrics
- Total return
- Annualized return where sample permits
- Maximum drawdown
- Closed trade count
- Win rate
- Average trade return
- Average winner / average loser
- Exposure percentage
- Turnover / position transitions
- Result after assumed friction
- Buy-and-hold return and drawdown for the same period

## Graduation gates
A candidate does **not** qualify for the future $10 live experiment unless:
- Rules were frozen before the untouched test.
- Validation and untouched-test results remain positive after friction.
- It is not dependent on a single ETF.
- Drawdown is acceptable relative to return.
- Trade count is large enough that one or two lucky trades do not dominate results.
- It survives forward paper tracking after historical testing.

## $10 live-capital rule
Even a graduated strategy receives no real capital until the owner separately authorizes live trading. Historical or paper profit never counts as Factory revenue.
