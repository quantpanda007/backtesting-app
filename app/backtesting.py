import vectorbt as vbt
from multiprocessing import Pool, cpu_count
import numpy as np

def run_backtest(data, short_ema, long_ema, initial_cash, fees):
    """Run a backtest using VectorBT."""
    investment_per_trade=10000
    portfolios = {}
    # Calculate EMAs
    for stock in data.columns:
        short_ema_series = vbt.MA.run(data[stock], short_ema, ewm=True).ma
        long_ema_series = vbt.MA.run(data[stock], long_ema, ewm=True).ma

        # Generate signals
        entries = short_ema_series > long_ema_series
        exits = short_ema_series < long_ema_series

        # Run portfolio
        portfolio = vbt.Portfolio.from_signals(
            data[stock],
            entries=entries,
            exits=exits,
            init_cash=initial_cash,
            fees=fees / 100,
            size=1.0,  # Use 100% of cash per trade
        )
        portfolios[stock] = portfolio
    return portfolios



def process_stock(args):
    """Backtest a single stock."""
    stock, close, fast_window, slow_window, investment_per_trade = args

    fast_sma = vbt.MA.run(close, window=fast_window).ma
    slow_sma = vbt.MA.run(close, window=slow_window).ma

    entries = fast_sma > slow_sma
    exits = fast_sma < slow_sma

    portfolio = vbt.Portfolio.from_signals(
        close=close,
        entries=entries,
        exits=exits,
        size=np.where(entries, investment_per_trade, 0)
    )

    return stock, portfolio

def run_crossover_backtest(data, fast_window, slow_window, investment_per_trade):
    """Run SMA crossover backtest using multiprocessing."""
    args = [
        (stock, data[stock], fast_window, slow_window, investment_per_trade)
        for stock in data.columns
    ]

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(process_stock, args)

    return {stock: portfolio for stock, portfolio in results}