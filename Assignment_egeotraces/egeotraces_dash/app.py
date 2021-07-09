# -*- coding: utf-8 -*-

# Run this app with `python app.py` and visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/
# based on ideas at "Dash App With Multiple Inputs" in https://dash.plotly.com/basic-callbacks
# mouse-over or 'hover' behavior is based on https://dash.plotly.com/interactive-graphing
# plotly express line parameters via https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line
# Mapmaking code initially learned from https://plotly.com/python/mapbox-layers/.


from flask import Flask
from os import environ

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

import plotting as plot

initial_color_checkbox = ['blue']
initial_background = ['plain']
initial_cruise = 'GIPY0405'


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'),
    external_stylesheets=external_stylesheets
)

app.layout = html.Div([
    dcc.Markdown('''
        ### EOSC 372 GEOTRACES Assignment

        #### Learning Goals
        
        1. ...
        2. ... 
        
        #### Instructions  
        
        - Mouse-over a station (dots) will plot the corresponding temperature, salinity & oxygen profiles.  
        - Mouse wheel zooms within the map.  
        - Map background and station dot color can be adjusted with checkboxes.  
        - The map's slider changes vertical size of the map.  
        - Depth scale can be adjusted for all three plots together using the slider above the three depth profiles.  
        - Each depth profile can be saved as a figure which students could submit with an assignment.   

        ----------
        '''),

# the map with location points
    html.Div([
        dcc.Graph(
            id='map',
            config={
                'staticPlot': False,  # True, False
                'scrollZoom': True,  # True, False
                'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,  # True, False
                'displayModeBar': False,  # True, False, 'hover'
                'watermark': True,
                'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d'],
            },
            clear_on_unhover = True,
        )
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20', 'vertical-align': 'middle', 'margin-bottom': 30, 'margin-right': 50, 'margin-left': 20}),


    # slider or checklist details at https://dash.plotly.com/dash-core-components
    # checkboxes can be lumped together but then logic in "update_graph" is messier.
    # Content can be delivered using html, but markdown is simpler.
    html.Div([
        dcc.Markdown('''
        **Select point colour, map type & size**
        '''),
        # switch between plain or satellite view for the map
        dcc.Checklist(
            id='background',
            options=[
                {'label': 'Satellite (from USGS)', 'value': 'satellite'}
            ],
            value=initial_background
        ),

        # change colour to be more visible on satellite.
        dcc.Checklist(
            id='color_checkbox',
            options=[
                {'label': 'change dot color', 'value': 'fuscia'}
            ],
            value=initial_color_checkbox,
            labelStyle={'margin-bottom': 30}
        ),
        # choose the cruise
        dcc.Markdown('''
        **Select Cruise**
        '''),

        dcc.RadioItems(
            id='cruise',
            options=[
                {'label': 'GIPY04 and GIPY05', 'value': 'GIPY0405'},
                {'label': 'GA03', 'value': 'GA03'},
                {'label': 'GP02', 'value': 'GP02'}
            ],
            value=initial_cruise
        )
    ], style={'width': '40%', 'display': 'inline-block', 'vertical-align': 'middle'}),


    html.Div([
        dcc.Graph(
            id='subplots',
            config={
                'staticPlot': False,  # True, False
                'scrollZoom': False,  # True, False
                'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
                'showTips': True,  # True, False
                'displayModeBar': 'hover',  # True, False, 'hover'
                'watermark': False,
                'modeBarButtonsToRemove': ['resetAxis', 'pan2d', 'resetScale2d', 'select2d', 'lasso2d', 'zoom2d',
                                           'zoomIn2d', 'zoomOut2d', 'hoverCompareCartesian', 'hoverClosestCartesian',
                                           'autoScale2d'],
            }
        ),
    ], style={'display': 'inline-block', 'width': '100%'}),

    dcc.Markdown('''
        ----

        ### Questions for students

        To be added when an actual oceanography dashboard is created.

        ### Attributions
 
        - **Code by:** J. Byer, adapted from code by F. Jones at https://github.com/fhmjones/MappedData-DemoApp01
        - **Oceanography Data from:** Schlitzer, R., Anderson, R. F., Masferrer Dodas, E, et al., The GEOTRACES Intermediate Data Product 2017, Chem. Geol. (2018), https://doi.org/10.1016/j.chemgeo.2018.05.040.

        ''')
], style={'width': '1000px'})



#using the plotting import to plot the figures

fig_subplots = plot.initialize_subplots()
fig_map = plot.initialize_map(initial_color_checkbox, initial_background, initial_cruise)

#Suplot graph
@app.callback(
    Output(component_id='subplots', component_property='figure'),
    Input(component_id='map', component_property='hoverData'),
    Input(component_id='map', component_property='clickData'),
    Input(component_id='cruise', component_property='value')
)
def update_subplots(hov_data, click_data, cruise):
    if (dash.callback_context.triggered[0]['prop_id'].split('.')[0] == 'cruise'):
        fig = plot.switch_subplots(hov_data, click_data, cruise, fig_subplots)
    else:
        fig = plot.update_subplots(hov_data, click_data, cruise, fig_subplots)
    return fig



# The callback function with it's app.callback wrapper.
@app.callback(
    Output('map', 'figure'),
    Input('color_checkbox', 'value'),
    Input('background', 'value'),
    Input('cruise', 'value'),
    Input('map', 'clickData')
)
def update_map(color_checkbox, background, cruise, click_data):
    if (dash.callback_context.triggered[0]['prop_id'].split('.')[0] == 'cruise'):
        fig = plot.switch_map(color_checkbox, background, cruise, fig_map)
    else:
        fig = plot.update_map(color_checkbox, background, click_data, cruise, fig_map)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
