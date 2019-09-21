"""

This script reads a CSV file with a header and an Excel config file 
that defines the dash page layout, plotting a number of line graphs.

The config file has any number of sheets where each sheet defines
a different line graph (except for the header sheet, which defines 
the page header.)
Each graph sheet defines the title and height of the graph, 
one x-value column name and any number of y-value column names.

The data file is read and a set of Dash data structures are formed
according to the Excel config file specifications.

In the present script the config filename and data filename are hard coded.
Adapt this script according to your needs.


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

Dash starts a Flask server at 8050, so the browser must be pointing to 
localhost:8050
This means that once the server is running, you can view the page with 
the PyQt browser as used here, or in an external browser.
https://dash.plot.ly/integrating-dash
https://www.datacamp.com/community/tutorials/learn-build-dash-python

"""

import sys
import threading
import pandas as pd
import openpyxl as oxl

from PyQt5 import QtWidgets
import PyQt5.QtCore as QtCore
from PyQt5 import QtWebEngineWidgets

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
# import plotly.graph_objs as go

# creates a browser widget
class WebViewer(QtWebEngineWidgets.QWebEngineView):
    def __init__(self, parent, url):
        """
        """
        super().__init__(parent)
        page = QtWebEngineWidgets.QWebEnginePage(self)
        self.setPage(page)
        self.setUrl(QtCore.QUrl(url))



def makeDccGraph(gid, height, title, data):
    """Builds the data structure for one set of line graphs.

    id: must be unique to differentiate between graphs.
    figure: defines the graph layout in terms of
        title 
        data set (a complex data structure)
    style: defines some properties of the graph.

    This function can probably be expanded for improved style

    The function returns a dcc.Graph()function with parameters.
    """

    return dcc.Graph(
                id=gid,
                figure={'layout':{'title':title},'data':data},
                style={'height': str(height)},
            )


def makeHTMLPage(pagetitle,pageheader,lstgraphs):
    """Builds the complete page layout to be used in the browser.

    pagetitle: the text displayed in H1 format at the top of page.
    pageheader: a Markdown text block displayed immediately after 
                the title.
    lstgraphs: a list of data structures for the different graphs
               on the page. The list of structures is unpacked when 
               html.Div is called.  This means that what is passed 
               as a list is unpacked into separate function arguments
               by the *list operator.
    """
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
    """
    """
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



#####################################################
def makePageFromCVS(configfile,datafile):

    # read the data file
    df = pd.read_csv(datafile, sep="\s+", index_col=None)
    # print(df.columns)
    # print(df.head())

    #read the config file
    cxls = pd.ExcelFile(configfile)
    dfc = pd.read_excel(cxls, 'header')
    dfc = dfc.set_index('Variable')

    # get a list of graph sheetnames
    cwb =  oxl.load_workbook(configfile)
    sheetnames = [sn for sn in cwb.get_sheet_names() if 'graph' in sn]
    dfg = pd.DataFrame()
    # build one df with all sheets' info
    for shtnum,sheetname in enumerate(sheetnames):
        dft = pd.read_excel(cxls, sheetname)
        dft['Index'] = dft['Variable']
        dft['Graph'] = sheetname
        dft['ShtNum'] = shtnum
        # create unique index values
        i = 0
        for index,row in dft.iterrows():
            if 'yValue' in row['Variable']:
                dft.loc[index,'Index'] = f"{row['Variable']}{i:03d}"
                i = i + 1
        dft = dft.set_index('Index')
        dfg = dfg.append(dft)

        # now we have one df with the columns:
        # Variable, Value , Name, LineType, Graph, ShtNum

    # print(dfg)

    graphs = dfg['Graph'].unique()
    lstgraphs = []
    for graph in graphs:
        dft = dfg[(dfg['Graph']==graph)]
        dfx = dft[(dft['Variable']=='xValue')]
        # for all yValue lines in this graph
        dfy = dft[(dft['Variable']=='yValue')]
        grpData = []
        for index,row in dfy.iterrows():
            # each line in each graph must be a dict as follows:
            grpData.append({
                # 'x':df[dfx.iloc[0]['Value']],
                'x':dft.loc['xValue','Value'],
                'y':df[row['Value']],
                'type':row['LineType'],
                'name':row['Name'],
            })

        lstgraphs.append(makeDccGraph(gid=graph, 
                                    height=dft.loc['Height','Value'], 
                                    title=dft.loc['Title','Value'], 
                                    data=grpData))

    pageheader = dfc.loc['Pageheader','Value']
    pagetitle = dfc.loc['Pagetitle','Value']

    page = makeHTMLPage(pagetitle,pageheader,lstgraphs)

    return page

##########################################
#

if __name__ == "__main__":

    sys.argv.append("--disable-web-security")

    datafile = "data/tp05j2a.rgeo"
    configfile = 'data/pyqt-dash-config.xlsx'
    pageLayout = makePageFromCVS(configfile,datafile) 
    mode = None # fill in later, we need this to make the thread work
    threading.Thread(target=run_dash, args=(pageLayout,mode), daemon=True).start()

    app = QtWidgets.QApplication(sys.argv)
    main_widget = QtWidgets.QWidget(None)
    window_layout = QtWidgets.QVBoxLayout(main_widget)
    window_layout.addWidget(WebViewer(main_widget,"http://127.0.0.1:8050"))
    main_widget.show()

    sys.exit(app.exec_())
