"""
https://github.com/plotly/dash-recipes
https://github.com/plotly/dash-recipes/blob/master/multiple-hover-data.py

conda config --add channels conda-forge
conda search dash-daq --channel conda-forge




conda install dash
conda install dash-html-components
conda install dash-core-components
conda install dash-table
conda install dash-daq


"""

import sys
import threading

from PyQt5 import QtWidgets
import PyQt5.QtCore as QtCore
from PyQt5 import QtWebEngineWidgets

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd

def run_dash(dataSource,mode):

    # start a dash app, which also starts a Flask server
    app = dash.Dash()

    # override security restrictions: allow the serving of local pages 
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True

    filename = 'data/tp05j2a.rgeo'
    df = pd.read_csv(filename, sep='\s+',index_col=None)
    print(df.columns)
    print(df.head())
    # CurrentSimTime     Rel-distance  Rel-speed

    demograph1 = {'id':'position',
                'figure':{
                    'data': [
                        {'x':df['%CurrentSimTime'], 'y':df['Rel-distance'], 'type': 'line', 'name': 'Distance'},
                        {'x':df['%CurrentSimTime'], 'y':df['Rel-loc-World[0]'], 'type': 'line', 'name': 'X'},
                        {'x':df['%CurrentSimTime'], 'y':df['Rel-loc-World[1]'], 'type': 'line', 'name': 'Y'},
                        {'x':df['%CurrentSimTime'], 'y':df['Rel-loc-World[2]'], 'type': 'line', 'name': 'Z'},

                        ],
                    'layout':  {
                        'title': 'Position'
                        }
                    }
                }


    demograph2 = {'id':'speed',
                'figure':{
                    'data': [
                        {'x':df['%CurrentSimTime'], 'y':df['Rel-speed'], 'type': 'line', 'name': u'Speed'},
                        {'x':df['%CurrentSimTime'], 'y':df['Rel-vel-World[0]'], 'type': 'line', 'name': u'Vx'},
                        {'x':df['%CurrentSimTime'], 'y':df['Rel-vel-World[1]'], 'type': 'line', 'name': u'Vy'},
                        {'x':df['%CurrentSimTime'], 'y':df['Rel-vel-World[2]'], 'type': 'line', 'name': u'Vz'},
                        ],
                    'layout':  {
                        'title': 'Speed'
                        }
                    }
                }


    # build a page for display
    app.layout = html.Div(children=[
        html.H1(children='Dash Experiments'),

        # html.Div([dcc.Markdown(children='''Attempting to use *Dash* for plotting in PyQt5.''')]),


        dcc.Graph(id=demograph1['id'],figure=demograph1['figure']),

        dcc.Graph(id=demograph2['id'],figure=demograph2['figure'])

        ])



    # @app.callback(Output('Relative position', 'hoverData'), events=[Event('Relative speed', 'hover')])
    # def resetHoverData1():
    #     return None


    # @app.callback(Output('Relative speed', 'hoverData'), events=[Event('Relative position', 'hover')])
    # def resetHoverData2():
    #     return None


    # import plotly.tools as tls

    # fig = tls.make_subplots(rows=2, cols=1, shared_xaxes=True,vertical_spacing=0.009,horizontal_spacing=0.009)
    # fig['layout']['margin'] = {'l': 30, 'r': 10, 'b': 50, 't': 25}

    # fig.append_trace({'x':df['%CurrentSimTime'],'y':df['Rel-distance'],'type':'scatter','name':'Distance'},1,1)
    # fig.append_trace({'x':df['%CurrentSimTime'],'y':df['Rel-loc-World[0]'],'type':'scatter','name':'X'},1,1)
    # fig.append_trace({'x':df['%CurrentSimTime'],'y':df['Rel-loc-World[1]'],'type':'scatter','name':'Y'},1,1)
    # fig.append_trace({'x':df['%CurrentSimTime'],'y':df['Rel-loc-World[2]'],'type':'scatter','name':'Z'},1,1)
    # fig.append_trace({'x':df['%CurrentSimTime'],'y':df['Rel-speed'],'type':'scatter','name':'Speed'},2,1)

    app.css.append_css({
        'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    })

    app.run_server(debug=False,port=8050)


class WebViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        page = QtWebEngineWidgets.QWebEnginePage(self)
        self.setPage(page)
        self.setUrl(QtCore.QUrl('http://127.0.0.1:8050'))
#

if __name__ == '__main__':

    sys.argv.append("--disable-web-security")

    dataSource = None # fill in later
    mode = None # fill in later


    threading.Thread(target=run_dash, args=(dataSource,mode), daemon=True).start()

    app = QtWidgets.QApplication(sys.argv)

    main_widget = QtWidgets.QWidget(None)
    window_layout = QtWidgets.QVBoxLayout(main_widget)
    window_layout.addWidget(WebViewer(main_widget))
    main_widget.show()

    sys.exit(app.exec_())
