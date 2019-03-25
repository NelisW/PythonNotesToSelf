import dash
import dash_core_components as dcc
import dash_html_components as html

# initialise Dash
app = dash.Dash()

# override security restrictions: allow the serving of local pages 
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True


# define style and colours
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# do the layout insode a Div
# create a Div, which can contain HTML elements
app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    dcc.Graph(
        id='Graph1',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True,port=8050)


