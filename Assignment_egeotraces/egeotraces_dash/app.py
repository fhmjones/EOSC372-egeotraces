# -*- coding: utf-8 -*-

# Run this app with `python app.py` and visit http://127.0.0.1:8050/ in your web browser.
# documentation at https://dash.plotly.com/
# based on ideas at "Dash App With Multiple Inputs" in https://dash.plotly.com/basic-callbacks
# mouse-over or 'hover' behavior is based on https://dash.plotly.com/interactive-graphing
# plotly express line parameters via https://plotly.com/python-api-reference/generated/plotly.express.line.html#plotly.express.line
# Mapmaking code initially learned from https://plotly.com/python/mapbox-layers/.


# map doesn't update right for GIPY05
#layout of plots
#layout of buttons

from flask import Flask
from os import environ

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get('JUPYTERHUB_SERVICE_PREFIX', '/'),
    external_stylesheets=external_stylesheets
)

# gather the list of soundings
# see Python routine "parse-csv.py" for the method of building this list
GIPY05 = pd.read_csv("GIPY05_filtered.csv")
GIPY04 = pd.read_csv("GIPY04_filtered.csv")
GA03 = pd.read_csv("GA03_filtered.csv")
GP02 = pd.read_csv("GP02_filtered.csv")


app.layout = html.Div([
    dcc.Markdown('''
        ### egeotraces assignment for EOSC 372
        ----------
        '''),

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
            value=['plain']
        ),
        # change colour to be more visible on satellite.
        dcc.Checklist(
            id='color_checkbox',
            options=[
                {'label': 'change dot color', 'value': 'fuscia'}
            ],
            value=['blue']
        ),
        # choose the cruise
        html.Label('Cruise'),
            dcc.RadioItems(
                id='cruise',
                options=[
                    {'label': 'GIPY05e', 'value': 'GIPY05'},
                    {'label': 'GA03', 'value': 'GA03'},
                    {'label': 'GP02', 'value': 'GP02'}
                ],
                value='GIPY05'
            ),
        # this slider is not necessary but demonstrates use of sliders that may be useful in other apps
        html.Label('map vertical size:'),
        dcc.Slider(id='mapheight', min=300, max=500, value=400, step=50,
                   marks={300: '300 pixels', 400: '400', 500: '500', }
                   )
    ], style={'width': '38%', 'display': 'inline-block'}),

    html.Div([
        dcc.Markdown('''
        **Measured values versus depth.**          
        Click-drag to zoom graphs. Double click to auto-scale. Reset all using axis slider. 
        ''')
    ], style={'width': '60%', 'display': 'inline-block', 'textAlign': 'center'}),

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
            # hoverData={'points:'}
        )
    ], style={'width': '38%', 'display': 'inline-block', 'padding': '0 20'}),

    # two side-by-side data plots
    # these have reduced interactivity to simplify the look and feel
    html.Div([
        dcc.Graph(
            id='temperature',
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
    ], style={'display': 'inline-block', 'width': '15%'}),
    html.Div([
        dcc.Graph(
            id='salinity',
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
    ], style={'display': 'inline-block', 'width': '15%'}),
    html.Div([
        dcc.Graph(
            id='nitrate',
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
    ], style={'display': 'inline-block', 'width': '15%'}),
    html.Div([
        dcc.Graph(
            id='iron',
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
    ], style={'display': 'inline-block', 'width': '15%'}),

    dcc.Markdown('''
        ----

        ### Questions for students

        To be added when an actual oceanography dashboard is created.

        ### Attributions
 
        - **Code:** F. Jones. Based on ideas learned in [Plotly interactive graphing](https://dash.plotly.com/interactive-graphing) documentation and a [great video on interactive plots](https://www.youtube.com/watch?v=G8r2BB3GFVY) using "hover" or "click" events.

        ''')
], style={'width': '1000px'})


# The callback function with it's app.callback wrapper.
@app.callback(
    Output('map', 'figure'),
    Input('mapheight', 'value'),
    Input('color_checkbox', 'value'),
    Input('background', 'value'),
    Input('cruise', 'value')
)
def update_map(mapheight, color_checkbox, background, cruise):
    # Dot color, map type and map zoom are interactive.
    # code from https://plotly.com/python/mapbox-layers/ without the "fig.show".

    if color_checkbox == ['blue']:
        dotcolor = "blue"
    else:
        dotcolor = 'fuchsia'

    if cruise == 'GIPY05':
        fig = px.scatter_mapbox(GIPY05, lat="Latitude", lon="Longitude", hover_name="Station", color_discrete_sequence=[dotcolor],
                                zoom=1.2, height=mapheight)
    elif cruise == 'GA03':
        fig = px.scatter_mapbox(GA03, lat="Latitude", lon="Longitude", hover_name="Station", color_discrete_sequence=[dotcolor],
                                zoom=1.2, height=mapheight)
    elif cruise == 'GP02':
        fig = px.scatter_mapbox(GP02, lat="Latitude", lon="Longitude", hover_name="Station", color_discrete_sequence=[dotcolor],
                                zoom=1.2, height=mapheight)

    # use this for a plain, easy-to-read street map
    if background == ['plain']:
        fig.update_layout(mapbox_style="open-street-map")

    # or, use this for a USGS colored topography raster instead of "open-street-map"
    # I do not know how that URL actually delivers the images
    # it is interactive but loading tiles upon "zoom in" may be slowish.
    # Also, at smaller scales, tiles outside of USA may be blank.
    else:
        fig.update_layout(
            mapbox_style="white-bg",
            mapbox_layers=[
                {"below": 'traces',
                 "sourcetype": "raster",
                 "sourceattribution": "United States Geological Survey",
                 "source": [
                     "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"]
                 }
            ])

    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0},
                      title=cruise)  # use "t":30 to put map below controls if they were there.

    return fig

def get_lat_lon_values(hov_data, cruise):
    if hov_data is None:  # necessary for startup before interacting with the map.
        if cruise == 'GIPY05':
            lat = GIPY05['Latitude'][0]
            lon = GIPY05['Longitude'][0]
        elif cruise == 'GA03':
            lat = GA03['Latitude'][0]
            lon = GA03['Longitude'][0]
        elif cruise == 'GP02':
            lat = GP02['Latitude'][0]
            lon = GP02['Longitude'][0]
    else:
        lat = hov_data['points'][0]['lat']
        lon = hov_data['points'][0]['lon']
    return [lat, lon]

def get_x_y_values(cruise, lat, lon, data_name):
    if cruise == 'GIPY05':
        xvals = GIPY05[data_name][(GIPY05['Latitude'] == lat) & (GIPY05['Longitude'] == lon)]
        yvals = GIPY05['Depth'][(GIPY05['Latitude'] == lat) & (GIPY05['Longitude'] == lon)]
    elif cruise == 'GA03':
        xvals = GA03[data_name][(GA03['Latitude'] == lat) & (GA03['Longitude'] == lon)]
        yvals = GA03['Depth'][(GA03['Latitude'] == lat) & (GA03['Longitude'] == lon)]
    elif cruise == 'GP02':
        xvals = GP02[data_name][(GP02['Latitude'] == lat) & (GP02['Longitude'] == lon)]
        yvals = GP02['Depth'][(GP02['Latitude'] == lat) & (GP02['Longitude'] == lon)]
    return [xvals, yvals]

# Temperature graph based on "hovering" over location on the map
@app.callback(
    Output(component_id='temperature', component_property='figure'),
    Input(component_id='map', component_property='hoverData'),
    Input(component_id='cruise', component_property='value')
)
def update_tgraph(hov_data, cruise):
    lat, lon = get_lat_lon_values(hov_data, cruise)
    xvals, yvals = get_x_y_values(cruise, lat, lon, 'Temperature')

    annot_lat = f'Lat: {lat:4.4f}N'
    annot_long = f'Lon: {lon:4.4f}E'

    figT = px.scatter(x=xvals, y=yvals, title='Temperature')
    figT.update_layout(margin={'l': 0, 'b': 0, 'r': 20, 't': 40})
    #figT.update_xaxes(range=[0, 30], title="deg. C.")
    figT.update_yaxes(range=[500, 0], title="Depth (m)")

    # this puts location information at bottom right of the temperature graph
    # better than making it a title since positioning is more versatile
    # there are no doubt other ways of adding this information
    figT.add_annotation(text=annot_lat,
                        xref="paper", yref="paper",  # Google this annotation function for explanation of "paper"
                        x=.14, y=.1, showarrow=False)
    figT.add_annotation(text=annot_long,
                        xref="paper", yref="paper",
                        x=.14, y=.05, showarrow=False)

    return figT


# Salinity graph based on "hovering" over location on the map
@app.callback(
    Output(component_id='salinity', component_property='figure'),
    Input(component_id='map', component_property='hoverData'),
    Input('cruise', 'value')
)
def update_sgraph(hov_data, cruise):
    lat, lon = get_lat_lon_values(hov_data, cruise)
    xvals, yvals = get_x_y_values(cruise, lat, lon, 'Salinity')

    figS = px.scatter(x=xvals, y=yvals, title='Salinity')
    figS.update_layout(margin={'l': 0, 'b': 0, 'r': 20, 't': 40})
    #figS.update_xaxes(range=[31, 37], title="PSS-78")
    figS.update_yaxes(range=[500, 0], title="Depth (m)")

    return figS


# Nitrate graph based on "hovering" over location on the map
@app.callback(
    Output(component_id='nitrate', component_property='figure'),
    Input(component_id='map', component_property='hoverData'),
    Input('cruise', 'value')
)
def update_ngraph(hov_data, cruise):
    lat, lon = get_lat_lon_values(hov_data, cruise)
    xvals, yvals = get_x_y_values(cruise, lat, lon, 'Nitrate')

    figN = px.scatter(x=xvals, y=yvals, title='Nitrate')
    figN.update_layout(margin={'l': 0, 'b': 0, 'r': 20, 't': 40})
    #figN.update_xaxes(range=[0, 320], title="UMOL/KG")
    figN.update_yaxes(range=[500, 0], title="Depth (m)")

    return figN


# Iron graph based on "hovering" over location on the map
@app.callback(
    Output(component_id='iron', component_property='figure'),
    Input(component_id='map', component_property='hoverData'),
    Input('cruise', 'value')
)
def update_igraph(hov_data, cruise):
    lat, lon = get_lat_lon_values(hov_data, cruise)
    xvals, yvals = get_x_y_values(cruise, lat, lon, 'Iron')

    figI = px.scatter(x=xvals, y=yvals, title='Iron')
    figI.update_layout(margin={'l': 0, 'b': 0, 'r': 20, 't': 40})
    #figI.update_xaxes(range=[0, 320], title="UMOL/KG")
    figI.update_yaxes(range=[500, 0], title="Depth (m)")

    return figI

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
