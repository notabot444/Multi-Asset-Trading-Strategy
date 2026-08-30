from __future__ import annotations

import numpy as np
import pandas as pd


def download_prices(tickers: dict[str, str], start: str, end: str | None = None) -> pd.DataFrame:
    """Download adjusted close prices with yfinance.

    If download fails, raise an informative error. Use sample_prices() for an
    offline/demo run.
    """
    import yfinance as yf

    symbols = list(tickers.values())
    raw = yf.download(symbols, start=start, end=end, auto_adjust=True, progress=False)
    if raw.empty:
        raise RuntimeError("No market data downloaded. Check internet connection or ticker symbols.")

    if isinstance(raw.columns, pd.MultiIndex):
        prices = raw["Close"].copy()
    else:
        prices = raw[["Close"]].copy()
        prices.columns = [symbols[0]]

    reverse = {v: k for k, v in tickers.items()}
    prices = prices.rename(columns=reverse).dropna(how="all").ffill()
    return prices


def sample_prices(n: int = 800, seed: int = 7) -> pd.DataFrame:
    """Create deterministic SYNTHETIC sample prices so the repo runs offline.

    This data is for demonstration/testing only and must not be described as
    historical market data.
    """
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2022-01-03", periods=n)
    assets = {
        "Equity": (0.00035, 0.010),
        "Gold": (0.00015, 0.007),
        "FixedIncome": (0.00005, 0.006),
        "CrudeOil": (0.00025, 0.018),
    }
    out = {}
    for name, (mu, sigma) in assets.items():
        rets = rng.normal(mu, sigma, n)
        out[name] = 100 * np.exp(np.cumsum(rets))
    return pd.DataFrame(out, index=dates)
