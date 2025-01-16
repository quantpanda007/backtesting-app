import pytest
import pandas as pd
from app.backtesting import run_backtest

def test_run_backtest():
    """Test the backtest function."""
    # Sample data
    data = pd.Series([100, 105, 110, 95, 90], 
                     index=pd.date_range("2023-01-01", periods=5))

    # Run backtest
    portfolio = run_backtest(data, short_ema=2, long_ema=4, initial_cash=1000, fees=0.1)

    assert portfolio.total_profit() != 0, "Backtest should return non-zero profit/loss."
