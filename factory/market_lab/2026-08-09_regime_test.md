# Market Lab — 2026-08-09 Regime Test

Research only. No live orders placed.

## Inputs
Alpaca IEX daily bars through 2026-08-07.

- SPY close: 773.16
- QQQ close: 722.89
- SPY 20-session SMA (computed from latest 20 closes): ~749.07
- QQQ 20-session SMA (computed from latest 20 closes): ~700.63
- SPY close vs SMA20: +3.22%
- QQQ close vs SMA20: +3.18%

## Simple regime rule under test
Risk-on candidate only when BOTH SPY and QQQ close above their respective 20-day simple moving averages. Otherwise neutral/risk-off.

Current research classification: RISK-ON CANDIDATE.

## Guardrails before any strategy is considered viable
- Add transaction-cost/slippage assumptions.
- Test out-of-sample and across multiple market regimes.
- Measure max drawdown, hit rate, turnover, and exposure.
- Compare against passive benchmarks.
- Do not infer profitability from the current signal alone.
- No live-capital deployment from this note.
