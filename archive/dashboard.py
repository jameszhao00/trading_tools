import json
from datetime import datetime, date

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

import strategies
from backtest import Backtester, BacktestResult

FACTOR_HEDGE_UNIVERSE = [
    "SPXS",
    "SQQQ",
    "VXX",
]
FACTOR_SHORT_UNIVERSE = [
    "IWF"
]

long_universe = [
    "AMZN",
    "BABA",
    "BYND",
    "CHWY",
    "COUP",
    "CRSP",
    "CRWD",
    "CVNA",
    "DDOG",
    "DOCU",
]
short_universe = ["XOM"]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = html.Div(children=[
    # html.Div(className="navbar navbar-dark sticky-top bg-dark flex-md-nowrap p-0", children=[
    #     html.A(className="navbar-brand col-sm-3 col-md-2 mr-0", children="Optimizer")
    # ]),
    html.Div(className="container-fluid", children=[
        html.Div(className="row", children=[
            html.Nav(className="col-md-2 d-none d-md-block bg-light sidebar", children=[
                html.Div(className="sidebar-sticky", children=[
                    html.Ul(className="nav flex-column", children=[
                        html.Li(className="nav-item", children=[
                            html.A(className="nav-link", children="Content")
                        ])
                    ])
                ])
            ]),
            html.Main(className="col-md-9 ml-sm-auto col-lg-10 pt-3 px-4", role="main", children=[
                html.Div(id="debug"),
                html.Div(id="hidden-div1", style={"display": "none"}),
                html.Div(id="hidden-div2", style={"display": "none"}),
                html.Div([
                    html.Div([
                        dcc.Markdown("""
            Longs
            """),
                        dash_table.DataTable(
                            id='long-universe-table',
                            columns=[{"name": "Ticker", "id": "ticker"}],
                            data=[{"ticker": ticker} for ticker in long_universe],
                            editable=True
                        )]),
                    html.Div([
                        dcc.Markdown("""
            Shorts
            """),
                        dash_table.DataTable(
                            id='short-universe-table',
                            columns=[{"name": "Ticker", "id": "ticker"}],
                            data=[{"ticker": ticker} for ticker in short_universe],
                            editable=True
                        )]),
                ]),
                dcc.DatePickerRange(
                    id='backtest-date-range',
                    min_date_allowed=date(2010, 1, 1),
                    max_date_allowed=date.today(),
                    initial_visible_month=date(2020, 8, 5),
                    start_date=date(2020, 6, 1),
                    end_date=date(2020, 10, 25)
                ),
                html.Button(id='backtest-portfolio', n_clicks=0, children='Submit'),
                html.Div([
                    dcc.Graph(id="nav-graph", figure={}),
                ]),
                html.Div([
                    dcc.Graph(id="nav-graph-details")
                ]),
            ])
        ])
    ])
])
backtester = Backtester(datetime(2020, 8, 1, 0, 0, 0))
backtest_results: BacktestResult = None


@app.callback(
    Output("hidden-div1", "children"),
    [Input('long-universe-table', 'data')])
def modify_long_universe(rows):
    global long_universe
    long_universe = [item["ticker"] for item in rows]


@app.callback(
    Output("hidden-div2", "children"),
    [Input('short-universe-table', 'data')])
def modify_short_universe(rows):
    global short_universe
    short_universe = [item["ticker"] for item in rows]


@app.callback(
    Output("nav-graph-details", "figure"),
    [Input('nav-graph', 'hoverData')])
def nav_graph_hover(nav_graph_hover_data):
    if backtest_results:
        date_str = nav_graph_hover_data["points"][0]["x"]
        # There may be component stock data before when we started backtesting.
        if date_str not in backtest_results.allocation_history.index:
            return {}
        data = backtest_results.allocation_history.loc[date_str]
        fig = px.bar(data, orientation='h', )
        fig.update_xaxes(range=[0, 1])
        return fig

    return {}


@app.callback(Output('nav-graph', 'figure'),
              [Input('backtest-portfolio', 'n_clicks')],
              [Input('backtest-date-range', 'start_date'), Input('backtest-date-range', 'end_date')])
def run_backtest(n_clicks, start_date, end_date):
    if n_clicks == 0:
        return {}

    global backtester
    start_date = datetime.fromisoformat(start_date)
    end_date = datetime.fromisoformat(end_date)
    if backtester.start_date != start_date or backtester.end_date != end_date:
        backtester = Backtester(start_date=start_date, end_date=end_date)
    r = backtester.backtest(long_universe, short_universe, strategies.min_variance_portfolio)
    global backtest_results
    backtest_results = r
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True)

    cum_returns = (r.returns_history + 1).cumprod()
    fig.add_trace(go.Scatter(x=cum_returns.index, y=cum_returns), row=1, col=1)
    fig.update_yaxes(type="log", row=1, col=1)

    for (k, v) in r.allocation_history.items():
        fig.add_trace(go.Scatter(x=r.allocation_history.index, y=v, name=k, stackgroup='one'), row=2, col=1)

    component_cum_returns = (r.component_returns + 1).cumprod()
    for column in component_cum_returns.columns:
        fig.add_trace(go.Scatter(x=component_cum_returns.index, y=component_cum_returns[column], name=column), row=3,
                      col=1)
    fig.update_layout({
        "height": 800
    })
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
