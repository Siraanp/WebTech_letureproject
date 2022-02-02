import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import flask


data = pd.read_csv("finance-charts-apple.csv")

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

app.layout = html.Div(
    children=[
        html.H1(children="AAPL",),
        html.P(
            children="Apple inc."
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["Date"],
                        "y": data["AAPL.High"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "AAPL High"},
            },
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
