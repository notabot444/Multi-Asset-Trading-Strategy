from __future__ import annotations

import pandas as pd


def moving_average_signal(prices: pd.Series, short_window: int = 20, long_window: int = 50) -> pd.Series:
    short_ma = prices.rolling(short_window).mean()
    long_ma = prices.rolling(long_window).mean()
    signal = (short_ma > long_ma).astype(float)
    return signal.fillna(0.0)


def momentum_signal(prices: pd.Series, lookback: int = 20) -> pd.Series:
    momentum = prices.pct_change(lookback)
    signal = (momentum > 0).astype(float)
    return signal.fillna(0.0)


def backtest(prices: pd.Series, signal: pd.Series, stop_loss_pct: float | None = None) -> pd.DataFrame:
    """Simple long/cash backtest.

    Signal is shifted by one day to avoid look-ahead bias: today's close-based
    signal can only affect tomorrow's return.
    """
    asset_ret = prices.pct_change().fillna(0.0)
    position = signal.shift(1).fillna(0.0).copy()

    if stop_loss_pct is not None:
        entry_price = None
        in_position = False
        adjusted = []
        for dt in prices.index:
            desired = float(position.loc[dt])
            px = float(prices.loc[dt])
            if desired > 0 and not in_position:
                entry_price = px
                in_position = True
            if in_position and entry_price is not None and px <= entry_price * (1 - stop_loss_pct):
                desired = 0.0
                in_position = False
                entry_price = None
            if desired == 0:
                in_position = False
                entry_price = None
            adjusted.append(desired)
        position = pd.Series(adjusted, index=prices.index)

    strat_ret = position * asset_ret
    return pd.DataFrame({
        "Price": prices,
        "AssetReturn": asset_ret,
        "Signal": signal,
        "Position": position,
        "StrategyReturn": strat_ret,
        "BuyHoldReturn": asset_ret,
    })
