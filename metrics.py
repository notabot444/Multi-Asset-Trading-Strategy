from __future__ import annotations

import numpy as np
import pandas as pd


def daily_returns(prices: pd.Series) -> pd.Series:
    return prices.pct_change().fillna(0.0)


def cumulative_return(returns: pd.Series) -> float:
    return float((1.0 + returns).prod() - 1.0)


def annualized_volatility(returns: pd.Series, trading_days: int = 252) -> float:
    return float(returns.std(ddof=0) * np.sqrt(trading_days))


def sharpe_ratio(returns: pd.Series, risk_free_rate: float = 0.04, trading_days: int = 252) -> float:
    rf_daily = (1.0 + risk_free_rate) ** (1.0 / trading_days) - 1.0
    excess = returns - rf_daily
    vol = excess.std(ddof=0)
    if vol == 0:
        return 0.0
    return float(excess.mean() / vol * np.sqrt(trading_days))


def max_drawdown(returns: pd.Series) -> float:
    wealth = (1.0 + returns).cumprod()
    running_peak = wealth.cummax()
    drawdown = wealth / running_peak - 1.0
    return float(drawdown.min())


def win_rate(returns: pd.Series) -> float:
    active = returns[returns != 0]
    if active.empty:
        return 0.0
    return float((active > 0).mean())


def historical_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """Positive number representing one-day loss threshold at given confidence."""
    q = float(returns.quantile(1.0 - confidence))
    return max(0.0, -q)


def summary(returns: pd.Series, risk_free_rate: float = 0.04) -> dict[str, float]:
    return {
        "Cumulative Return": cumulative_return(returns),
        "Annualized Volatility": annualized_volatility(returns),
        "Sharpe Ratio": sharpe_ratio(returns, risk_free_rate),
        "Max Drawdown": max_drawdown(returns),
        "Win Rate": win_rate(returns),
        "95% 1D VaR": historical_var(returns, 0.95),
    }
