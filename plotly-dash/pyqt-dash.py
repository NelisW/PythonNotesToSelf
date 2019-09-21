"""
https://github.com/plotly/dash-recipes
https://github.com/plotly/dash-recipes/blob/master/multiple-hover-data.py
https://plot.ly/python/subplots/

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
import pandas as pd

from PyQt5 import QtWidgets
import PyQt5.QtCore as QtCore
from PyQt5 import QtWebEngineWidgets

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# import plotly.graph_objs as go


def makeDccGraph(gid, height, title, data):
    dccgraph = dcc.Graph(
                id=gid,
                figure={'layout':{'title':title},'data':data},
                style={'height': str(height)},
            )
    return dccgraph


def makeHTMLPage(pagetitle,pageheader,lstgraphs):
    # build a page for display
    page = html.Div(
        children=[
            html.H1(children=pagetitle),
            html.Div([dcc.Markdown(children=pageheader)]),
            # following is a list of dcc.Graph(() graphs
            *lstgraphs
        ]
    )
    return page


def run_dash(pageLayout,mode):
    # start a dash app, which also starts a Flask server
    app = dash.Dash()
    # override security restrictions: allow the serving of local pages
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True
    app.layout = pageLayout
    # app.css.append_css({
    #     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
    # })
    app.run_server(debug=False, port=8050)

class WebViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        page = QtWebEngineWidgets.QWebEnginePage(self)
        self.setPage(page)
        self.setUrl(QtCore.QUrl("http://127.0.0.1:8050"))


#####################################################
def makePageFromCVS(configfile,datafile):



    # read the data file
    df = pd.read_csv(datafile, sep="\s+", index_col=None)
    # print(df.columns)
    # print(df.head())

    grpData1 = [
        {
            "x": df["%CurrentSimTime"],
            "y": df["Rel-distance"],
            "type": "line",
            "name": "Distance",
        },
        {
            "x": df["%CurrentSimTime"],
            "y": df["Rel-loc-World[0]"],
            "type": "line",
            "name": "X",
        },
        {
            "x": df["%CurrentSimTime"],
            "y": df["Rel-loc-World[1]"],
            "type": "line",
            "name": "Y",
        },
        {
            "x": df["%CurrentSimTime"],
            "y": df["Rel-loc-World[2]"],
            "type": "line",
            "name": "Z",
        },
    ]

    grpData2 = [
        {
            "x": df["%CurrentSimTime"].values,
            "y": df["Rel-speed"].values,
            "type": "line",
            "name": u"Speed",
        },
        {
            "x": df["%CurrentSimTime"].values,
            "y": df["Rel-vel-World[0]"].values,
            "type": "line",
            "name": u"Vx",
        },
        {
            "x": df["%CurrentSimTime"].values,
            "y": df["Rel-vel-World[1]"].values,
            "type": "line",
            "name": u"Vy",
        },
        {
            "x": df["%CurrentSimTime"].values,
            "y": df["Rel-vel-World[2]"].values,
            "type": "line",
            "name": u"Vz",
        },
    ]

    grpData3 = [
        {
            "x": df["Rel-vel-World[0]"].values,
            "y": df["Rel-speed"].values,
            "type": "line",
            "name": u"Speed",
        },
    ]

    demograph1 = makeDccGraph(gid="position", height=300, title="position", data=grpData1)
    demograph2 = makeDccGraph(gid="speed", height=600, title="speed", data=grpData2)
    demograph3 = makeDccGraph(gid="speedxy", height=600, title="speed", data=grpData3)

    lstgraphs = [demograph1,demograph2,demograph3]

    pageheader = """Attempting to use *Dash* for plotting in PyQt5."""
    pagetitle='Dash Experiments'

    page = makeHTMLPage(pagetitle,pageheader,lstgraphs)

    return page

##########################################
#

if __name__ == "__main__":

    sys.argv.append("--disable-web-security")

    datafile = "data/tp05j2a.rgeo"
    configfile = None
    pageLayout = makePageFromCVS(configfile,datafile) 
    mode = None # fill in later, we need this to make the thread work

    threading.Thread(target=run_dash, args=(pageLayout,mode), daemon=True).start()
    app = QtWidgets.QApplication(sys.argv)
    main_widget = QtWidgets.QWidget(None)
    window_layout = QtWidgets.QVBoxLayout(main_widget)
    # window_layout.addWidget(WebViewer(main_widget))
    window_layout.addWidget(WebViewer(main_widget))
    main_widget.show()

    sys.exit(app.exec_())
