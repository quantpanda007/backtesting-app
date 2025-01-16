import plotly.graph_objects as go

def plot_equity_curve(portfolio):
    """Plot the equity curve of the portfolio."""
    equity = portfolio.value()
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=equity.index, y=equity, mode="lines", name="Equity"))
    fig.update_layout(
        title="Equity Curve",
        xaxis_title="Date",
        yaxis_title="Portfolio Value",
        template="plotly_white"
    )
    return fig

def plot_drawdown_curve(portfolio):
    """Plot the drawdown curve of the portfolio."""
    drawdown = portfolio.drawdown() * 100
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=drawdown.index, 
        y=drawdown, 
        mode="lines", 
        name="Drawdown",
        fill="tozeroy"
    ))
    fig.update_layout(
        title="Drawdown Curve",
        xaxis_title="Date",
        yaxis_title="Drawdown (%)",
        template="plotly_white"
    )
    return fig
