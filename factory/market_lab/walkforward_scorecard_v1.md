# Market Lab Walk-Forward Scorecard v1

Research/paper-use only. No live capital.

## Candidate families
- SMA trend: long when close is above a trailing moving average.
- Breakout: enter on a multi-session closing high, exit on a shorter breakdown.
- Pullback mean reversion: buy a defined multi-day decline only while the broader trend is positive, then exit on recovery or a maximum holding period.

## Evaluation protocol
1. Use synchronized SPY, QQQ, IWM and DIA daily data.
2. Freeze strategy rules before validation.
3. Split observations chronologically: first 60% discovery, next 20% validation, final 20% untouched test.
4. Charge at least 5 bps friction on every entry and exit.
5. Compare each strategy against buy-and-hold on the same dates.
6. Reject any candidate that only works on one ETF or whose test-period result collapses versus discovery.
7. Forward-paper track any survivor before considering live capital.

## Required metrics
For every ticker and strategy record:
- total return
- annualized return when sample length permits
- max drawdown
- trade count
- win rate
- average winning trade
- average losing trade
- profit factor
- exposure percentage
- benchmark return
- excess return vs benchmark
- discovery / validation / test returns separately

## Graduation gate for $10 live experiment
A strategy is only eligible for discussion if:
- positive untouched test return after friction,
- no catastrophic drawdown,
- behavior is directionally consistent on multiple ETFs,
- enough trades exist to make the result more than a one-trade accident,
- forward paper behavior does not materially contradict the historical test.

Passing this gate does not imply profitability or authorize a live trade. Explicit owner authorization is still required before real capital is deployed.
