#!/usr/bin/env python3
"""Market Lab v1: simple long-only strategy comparison.

Input CSV columns: date,close. No live trading. Research/paper use only.
Strategies:
- sma20: long when close > prior 20-day SMA
- breakout20: long when close > prior 20-day high; exit when close < prior 10-day low
- pullback3: while close > 50-day SMA, buy after 3 consecutive down closes; hold max 5 sessions or until close > prior close

Reports total return, max drawdown, trades and win rate. Assumes 5 bps friction on each entry/exit.
"""
from __future__ import annotations
import csv, math, sys
from pathlib import Path

FRICTION = 0.0005

def load(path):
    rows=[]
    with Path(path).open() as f:
        for r in csv.DictReader(f):
            rows.append((r['date'], float(r['close'])))
    return rows

def dd(equity):
    peak=equity[0]; worst=0.0
    for x in equity:
        peak=max(peak,x)
        worst=min(worst, x/peak-1)
    return worst

def run(rows, kind):
    c=[x[1] for x in rows]; pos=False; entry=0.0; hold=0; eq=1.0; curve=[eq]; trades=[]
    for i in range(1,len(c)):
        prev=c[i-1]; now=c[i]
        enter=exit=False
        if kind=='sma20' and i>=20:
            sma=sum(c[i-20:i])/20
            enter=(not pos and now>sma); exit=(pos and now<=sma)
        elif kind=='breakout20' and i>=20:
            enter=(not pos and now>max(c[i-20:i])); exit=(pos and i>=10 and now<min(c[i-10:i]))
        elif kind=='pullback3' and i>=50:
            sma50=sum(c[i-50:i])/50
            down3=c[i-3]>c[i-2]>c[i-1]>now
            enter=(not pos and now>sma50 and down3)
            exit=(pos and (now>prev or hold>=5))
        if enter:
            pos=True; entry=now*(1+FRICTION); hold=0
        if pos:
            eq *= now/prev
            hold += 1
        if exit and pos:
            px=now*(1-FRICTION); trades.append(px/entry-1); eq *= (1-FRICTION); pos=False; hold=0
        curve.append(eq)
    if pos:
        px=c[-1]*(1-FRICTION); trades.append(px/entry-1)
    wins=sum(t>0 for t in trades)
    return {
        'strategy':kind,
        'total_return_pct':round((curve[-1]-1)*100,2),
        'max_drawdown_pct':round(dd(curve)*100,2),
        'trades':len(trades),
        'win_rate_pct':round((wins/len(trades)*100) if trades else 0,2),
        'avg_trade_pct':round((sum(trades)/len(trades)*100) if trades else 0,2),
    }

def main():
    rows=load(sys.argv[1])
    for kind in ['sma20','breakout20','pullback3']:
        print(run(rows,kind))

if __name__=='__main__':
    main()
