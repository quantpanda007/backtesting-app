import streamlit as st
import pandas as pd
from backtesting import run_backtest
from plotting import plot_equity_curve
from data_processing import load_data_from_folder


def main():
    # Set up the Streamlit app
    st.set_page_config(page_title="SMA Crossover Backtesting", layout="wide")
    st.title("Simple Moving Average Crossover Backtesting")

    # Load data
    st.sidebar.header("Data Source")
    st.sidebar.info("Loading data from the 'data' folder.")
    data = load_data_from_folder("data/nifty100_stock_prices_yahoo.csv")

    #data=data.iloc[:,0:10]
    st.write("## Data Preview")
    st.dataframe(data.head(), use_container_width=True)

    # Input parameters for the strategy
    st.sidebar.header("Strategy Parameters")
    fast_window = st.sidebar.number_input("Fast SMA Window", min_value=1, value=10)
    slow_window = st.sidebar.number_input("Slow SMA Window", min_value=1, value=50)
    investment_per_trade = st.sidebar.number_input("Investment Per Trade ($)", min_value=1, value=10000)
    fee=3
    # Run the backtest when the button is clicked
    if st.sidebar.button("Run Backtest"):
        st.write("### Running Backtest...")

        try:
            # Run the crossover backtest
            
            portfolios = run_backtest(data, fast_window, slow_window, investment_per_trade,fee)
            
            # Collect equity curves and performance metrics      

            results = []
            trades=[]
            for stock, portfolio in portfolios.items():
                portfolio_value = portfolio.value()
                results.append(pd.DataFrame({stock: portfolio_value}))
                temp_df=portfolio.trades.records_readable
                temp_df.insert(0,column='Ticker',value=stock)
                trades.append(temp_df)

            # Display results
            st.write("## Backtest Results")
            st.write("### Performance Metrics")
            portfolio_values = pd.concat(results, axis=1)
            tear_sheet=pd.concat(trades, axis=0)
            #tear_sheet = tear_sheet.style.map(lambda x: f"background-color: {'green' if x>0 else 'red'}", subset='Return')

            st.dataframe(portfolio_values)
            st.dataframe(tear_sheet)
            st.write("### Portfolio Final Value")
            st.dataframe(portfolio_values.tail(1).T)
            #st.plotly_chart(plot_equity_curve(equity_curves), use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred during the backtest: {e}")


if __name__ == "__main__":
    main()
