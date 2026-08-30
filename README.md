# Multi-Asset Trading Strategy & Risk Analysis

A compact educational project for analysing multiple asset classes, generating simple trading signals, backtesting them, and measuring risk-adjusted performance.

## What it does

- Downloads market proxy data with `yfinance`:
  - Equity: SPY
  - Gold: GLD
  - Fixed-income proxy: TLT
  - Crude-oil proxy: USO
- Calculates returns and cross-asset correlations.
- Implements two simple long/cash strategies:
  1. Moving-average crossover
  2. Momentum
- Uses a one-day signal lag to reduce look-ahead bias.
- Adds a simple stop-loss rule.
- Compares each strategy with buy-and-hold.
- Reports:
  - Cumulative return
  - Annualized volatility
  - Sharpe ratio
  - Maximum drawdown
  - Win rate
  - Historical 95% one-day VaR
- Saves CSV outputs and equity-curve plots to `outputs/`.

## Important honesty note

This is an educational backtest, not evidence of a profitable live trading system. ETF prices are used as liquid proxies for asset classes; they are not the same as directly trading futures contracts. The `--sample` mode uses synthetic data only for testing the code offline and must not be described as historical market data.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\\Scripts\\activate   # Windows
pip install -r requirements.txt
```

## Run with real market proxy data

```bash
python main.py
```

Internet access is required because the script uses `yfinance`.

## Run offline with synthetic sample data

```bash
python main.py --sample
```

## Project structure

```text
axxela_trading_project/
├── config.py
├── data.py
├── metrics.py
├── strategy.py
├── main.py
├── requirements.txt
├── interview_notes.md
├── .gitignore
└── README.md
```

## Core logic

### Daily return

`r_t = P_t / P_(t-1) - 1`

### Moving-average strategy

Long when the 20-day moving average is above the 50-day moving average; otherwise stay in cash.

### Momentum strategy

Long when the 20-day price return is positive; otherwise stay in cash.

### Sharpe ratio

Annualized excess return per unit of volatility. Higher is better, but it should never be judged alone.

### Maximum drawdown

Largest peak-to-trough decline in the strategy's equity curve.

### Value at Risk (VaR)

The project uses historical 95% one-day VaR: the loss threshold exceeded on roughly 5% of historical days.

## Limitations

- No transaction costs or slippage.
- Long/cash only; no short selling.
- ETF proxies rather than direct futures data.
- Simple rules are used for learning, not production trading.
- Historical performance does not guarantee future performance.
