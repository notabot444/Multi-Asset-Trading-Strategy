from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from config import (
    END_DATE,
    INITIAL_CAPITAL,
    LONG_WINDOW,
    MOMENTUM_WINDOW,
    RISK_FREE_RATE,
    SHORT_WINDOW,
    START_DATE,
    STOP_LOSS_PCT,
    TICKERS,
)
from data import download_prices, sample_prices
from metrics import summary
from strategy import backtest, momentum_signal, moving_average_signal


def pct(x: float) -> str:
    return f"{100*x:.2f}%"


def run(use_sample: bool = False) -> None:
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    if use_sample:
        prices = sample_prices()
        data_label = "SYNTHETIC SAMPLE DATA"
    else:
        prices = download_prices(TICKERS, START_DATE, END_DATE)
        data_label = "YFINANCE MARKET DATA"

    prices.to_csv(out_dir / "prices.csv")
    price_returns = prices.pct_change().dropna()
    price_returns.corr().to_csv(out_dir / "correlation_matrix.csv")

    rows = []
    for asset in prices.columns:
        s = prices[asset].dropna()
        strategies = {
            "MovingAverage": moving_average_signal(s, SHORT_WINDOW, LONG_WINDOW),
            "Momentum": momentum_signal(s, MOMENTUM_WINDOW),
        }

        for strategy_name, signal in strategies.items():
            bt = backtest(s, signal, STOP_LOSS_PCT)
            bt.to_csv(out_dir / f"{asset}_{strategy_name}_backtest.csv")

            strat_metrics = summary(bt["StrategyReturn"], RISK_FREE_RATE)
            bh_metrics = summary(bt["BuyHoldReturn"], RISK_FREE_RATE)
            rows.append({"Asset": asset, "Strategy": strategy_name, **strat_metrics})
            rows.append({"Asset": asset, "Strategy": "BuyHold", **bh_metrics})

            wealth = INITIAL_CAPITAL * (1 + bt[["StrategyReturn", "BuyHoldReturn"]]).cumprod()
            ax = wealth.plot(title=f"{asset}: {strategy_name} vs Buy & Hold")
            ax.set_ylabel("Portfolio Value")
            ax.set_xlabel("Date")
            plt.tight_layout()
            plt.savefig(out_dir / f"{asset}_{strategy_name}_equity_curve.png", dpi=160)
            plt.close()

    report = pd.DataFrame(rows).drop_duplicates(subset=["Asset", "Strategy"])
    report.to_csv(out_dir / "performance_summary.csv", index=False)

    print(f"Data source: {data_label}")
    print("\nPerformance summary:\n")
    display = report.copy()
    for c in ["Cumulative Return", "Annualized Volatility", "Max Drawdown", "Win Rate", "95% 1D VaR"]:
        display[c] = display[c].map(pct)
    display["Sharpe Ratio"] = display["Sharpe Ratio"].map(lambda x: f"{x:.2f}")
    print(display.to_string(index=False))
    print("\nFiles written to ./outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-asset trading strategy and risk analysis")
    parser.add_argument("--sample", action="store_true", help="Run with clearly-labelled synthetic sample data")
    args = parser.parse_args()
    run(use_sample=args.sample)
