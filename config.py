"""Project configuration."""

TICKERS = {
    "Equity": "SPY",
    "Gold": "GLD",
    "FixedIncome": "TLT",
    "CrudeOil": "USO",
}

START_DATE = "2022-01-01"
END_DATE = None
SHORT_WINDOW = 20
LONG_WINDOW = 50
MOMENTUM_WINDOW = 20
TRADING_DAYS = 252
RISK_FREE_RATE = 0.04
INITIAL_CAPITAL = 100000.0
STOP_LOSS_PCT = 0.05
