import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

# initialise Dash
app = dash.Dash()

# override security restrictions: allow the serving of local pages
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


# get some data to display
# df = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/' +
#     '5d1ea79569ed194d432e56108a04d188/raw/' +
#     'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
#     'gdp-life-exp-2007.csv')
df = pd.read_csv("data/gdp-life-exp-2007.csv")

# define style and colours
colors = {"background": "#111111", "text": "#7FDBFF"}

markdown_text = """
### Dash and Markdown

Dash supports [Markdown](http://commonmark.org/help).

Markdown is a simple way to write and format text.
It includes a syntax for things like **bold text** and *italics*,
[links](http://commonmark.org/help), inline `code` snippets, lists,
quotes, and more.
"""

# do the layout insode a Div
# create a Div, which can contain HTML elements
app.layout = html.Div(
    [
        dcc.Markdown(children=markdown_text),
        html.Div(
            [
                html.Div(
                    children=[
                        html.H3("Life expectancy vs GDP"),
                        # dcc.Graph(id='g1', figure={'data': [{'y': [1, 2, 3]}]})
                        dcc.Graph(
                            id="life-exp-vs-gdp",
                            figure={
                                "data": [
                                    go.Scatter(
                                        x=df[df["continent"] == i]["gdp per capita"],
                                        y=df[df["continent"] == i]["life expectancy"],
                                        text=df[df["continent"] == i]["country"],
                                        mode="markers",
                                        opacity=0.8,
                                        marker={
                                            "size": 15,
                                            "line": {"width": 0.5, "color": "white"},
                                        },
                                        name=i,
                                    )
                                    for i in df.continent.unique()
                                ],
                                "layout": go.Layout(
                                    xaxis={"type": "log", "title": "GDP Per Capita"},
                                    yaxis={"title": "Life Expectancy"},
                                    margin={"l": 40, "b": 40, "t": 10, "r": 10},
                                    legend={"x": 0, "y": 1},
                                    hovermode="closest",
                                ),
                            },
                        ),
                    ],
                    className="six columns",
                ),
                html.Div(
                    children=[
                        html.H3("Simple line plot"),
                        dcc.Graph(id="g2", figure={"data": [{"y": [1, 2, 3]}]}),
                    ],
                    className="six columns",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    children=[
                        html.H3("Dropdown box"),
                        dcc.Dropdown(
                            options=[
                                {"label": "New York City", "value": "NYC"},
                                {"label": u"Montreal", "value": "MTL"},
                                {"label": "San Francisco", "value": "SF"},
                            ],
                            value="MTL",
                        ),
                    ],
                    className="six columns",
                ),
                html.Div(
                    children=[
                        html.H3("Multi-Select Dropdown box"),
                        dcc.Dropdown(
                            options=[
                                {"label": "New York City", "value": "NYC"},
                                {"label": u"Montreal", "value": "MTL"},
                                {"label": "San Francisco", "value": "SF"},
                            ],
                            value=["MTL", "SF"],
                            multi=True,
                        ),
                    ],
                    className="six columns",
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    children=[
                        html.H3("Radio Items"),
                        dcc.RadioItems(
                            options=[
                                {"label": "New York City", "value": "NYC"},
                                {"label": u"Montreal", "value": "MTL"},
                                {"label": "San Francisco", "value": "SF"},
                            ],
                            value="MTL",
                        ),
                    ],
                    className="six columns",
                ),
                html.Div(
                    children=[
                        html.H3("Checkboxes"),
                        dcc.Checklist(
                            options=[
                                {"label": "New York City", "value": "NYC"},
                                {"label": u"Montreal", "value": "MTL"},
                                {"label": "San Francisco", "value": "SF"},
                            ],
                            values=["NYC", "SF"],
                        ),
                    ],
                    className="six columns",
                ),
            ],
            className="row",
        ),
        html.H3("Text Box"),
        dcc.Input(value="MTL", type="text"),
        html.H3("Slider"),
        dcc.Slider(
            id="my-slider",
            min=0,
            max=20,
            step=0.5,
            marks={
                0: "0 °F",
                3: "3 °F",
                5: "5 °F",
                7.65: "7.65 °F",
                10: "10 °F",
                20: "20 °F",
            },
            value=10,
        ),
        html.Div(id="slider-output-container"),
    ]
)


# app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
# app.css.append_css({'external_url': './css/bWLwgP.css'})
# dcc._css_dist[0]['relative_package_path'].append('css/bWLwgP.css')

if __name__ == "__main__":
    app.run_server()
