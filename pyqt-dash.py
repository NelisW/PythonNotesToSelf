"""

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


def run_dash(dataSource,mode):

    # start a dash app, which also starts a Flask server
    app = dash.Dash()

    # override security restrictions: allow the serving of local pages 
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True


    # some dummy data for now
    data = [
        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        
        ]
    layout = {
        'title': 'Dash Data Visualization'
    }
    demograph = {'id':'example-graph',
                'figure':{
                    'data': data,
                    'layout': layout
                    }
                }

    # build a page for display
    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        html.Div(children='''
            Hopefully this can grow later.
        '''),

        dcc.Graph(id=demograph['id'],figure=demograph['figure'])

        ])

    # locationUrl = dcc.Location(id="url", refresh=False)
    # print(f'Serving at URL at {locationUrl}')

    app.run_server(debug=False)


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
