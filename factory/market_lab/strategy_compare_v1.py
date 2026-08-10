#!/usr/bin/env python3
"""Simple research harness for ETF strategy comparison.
Research/paper use only; not an order execution system.
Input CSV requires date,open,high,low,close columns.
"""
from __future__ import annotations
import argparse
import csv
from math import prod


def sma(xs, n, i):
    if i + 1 < n: return None
    return sum(xs[i-n+1:i+1]) / n


def max_drawdown(equity):
    peak = equity[0]
    worst = 0.0
    for x in equity:
        peak = max(peak, x)
        worst = min(worst, x / peak - 1)
    return worst


def evaluate(rows, signal_fn, friction_bps=5):
    closes = [float(r['close']) for r in rows]
    eq=[1.0]; pos=0; trades=0; wins=0; trade_entry=None; trade_rets=[]
    for i in range(1,len(rows)):
        newpos = 1 if signal_fn(rows, closes, i-1) else 0
        daily = closes[i]/closes[i-1]-1 if pos else 0
        if newpos != pos:
            daily -= friction_bps/10000
            trades += 1
            if newpos and not pos: trade_entry = closes[i]
            if pos and not newpos and trade_entry:
                tr=closes[i]/trade_entry-1-2*friction_bps/10000
                trade_rets.append(tr); wins += tr>0; trade_entry=None
        eq.append(eq[-1]*(1+daily)); pos=newpos
    return {
      'return':eq[-1]-1,'max_drawdown':max_drawdown(eq),'transitions':trades,
      'closed_trades':len(trade_rets),'win_rate': wins/len(trade_rets) if trade_rets else 0,
      'avg_trade':sum(trade_rets)/len(trade_rets) if trade_rets else 0
    }


def trend(rows,c,i):
    a=sma(c,20,i); b=sma(c,100,i)
    return a is not None and b is not None and a>b

def breakout(rows,c,i):
    if i<20:return False
    return c[i] >= max(c[i-20:i+1])

def pullback(rows,c,i):
    if i<100:return False
    long=sma(c,100,i)
    three=c[i]/c[i-3]-1
    return c[i]>long and three<=-0.03


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('csv'); ap.add_argument('--friction-bps',type=float,default=5)
    a=ap.parse_args()
    with open(a.csv,newline='',encoding='utf-8-sig') as f: rows=list(csv.DictReader(f))
    for name,fn in [('trend_20_100',trend),('breakout_20',breakout),('pullback_3pct_3d',pullback)]:
        print(name,evaluate(rows,fn,a.friction_bps))

if __name__=='__main__': main()
