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
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
GIPY0405 = pd.concat([GIPY04, GIPY05], ignore_index=True)

app.layout = html.Div([
    dcc.Markdown('''
        ### egeotraces assignment for EOSC 372
        instructions
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
    ], style={'width': '50%', 'display': 'inline-block', 'padding': '0 20', 'vertical-align': 'middle', 'margin-bottom': 50, 'margin-right': 50, 'margin-left': 20}),




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
            value=['blue'],
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
            value='GIPY0405'
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
    ###here

    dcc.Markdown('''
        ----

        ### Questions for students

        To be added when an actual oceanography dashboard is created.

        ### Attributions
 
        - **Code:** F. Jones. Based on ideas learned in [Plotly interactive graphing](https://dash.plotly.com/interactive-graphing) documentation and a [great video on interactive plots](https://www.youtube.com/watch?v=G8r2BB3GFVY) using "hover" or "click" events.
        - J. Byer :)

        ''')
], style={'width': '1000px'})








#get lat and lons from hoverData
def get_hov_lat_lon_values(hov_data, cruise):
    lat = hov_data['points'][0]['lat']
    lon = hov_data['points'][0]['lon']
    return [lat, lon]

#get lat and lons from clickData
def get_click_lat_lon_values(click_data, cruise, new_cruise):
    if (click_data is None) or (new_cruise == True):  # necessary for startup before interacting with the map.
        if cruise == 'GIPY0405':
            lat = GIPY0405['Latitude'][0]
            lon = GIPY0405['Longitude'][0]
        elif cruise == 'GA03':
            lat = GA03['Latitude'][0]
            lon = GA03['Longitude'][0]
        elif cruise == 'GP02':
            lat = GP02['Latitude'][0]
            lon = GP02['Longitude'][0]
    else:
        lat = click_data['points'][0]['lat']
        lon = click_data['points'][0]['lon']
    return [lat, lon]

def get_x_y_values(cruise, lat, lon, data_name):
    if cruise == 'GIPY0405':
        xvals = GIPY0405[data_name][(GIPY0405['Latitude'] == lat) & (GIPY0405['Longitude'] == lon)]
        yvals = GIPY0405['Depth'][(GIPY0405['Latitude'] == lat ) & (GIPY0405['Longitude'] == lon)]
    elif cruise == 'GA03':
        xvals = GA03[data_name][(GA03['Latitude'] == lat) & (GA03['Longitude'] == lon)]
        yvals = GA03['Depth'][(GA03['Latitude'] == lat) & (GA03['Longitude'] == lon)]
    elif cruise == 'GP02':
        xvals = GP02[data_name][(GP02['Latitude'] == lat) & (GP02['Longitude'] == lon)]
        yvals = GP02['Depth'][(GP02['Latitude'] == lat) & (GP02['Longitude'] == lon)]
    return [xvals, yvals]

#initialize the subplots
def initialize_subplots():
    fig = make_subplots(rows=1, cols=4, subplot_titles=("Temperature", "Salinity", "Nitrate", "Iron"))

    cruise = 'GIPY0405'
    lat, lon = get_click_lat_lon_values(None, cruise, False)

    xvals_temp, yvals_temp = get_x_y_values(cruise, lat, lon, 'Temperature')
    xvals_sal, yvals_sal = get_x_y_values(cruise, lat, lon, 'Salinity')
    xvals_nit, yvals_nit = get_x_y_values(cruise, lat, lon, 'Nitrate')
    xvals_iron, yvals_iron = get_x_y_values(cruise, lat, lon, 'Iron')

    figT = px.scatter(x=xvals_temp, y=yvals_temp)
    figS = px.scatter(x=xvals_sal, y=yvals_sal)
    figN = px.scatter(x=xvals_nit, y=yvals_nit)
    figI = px.scatter(x=xvals_iron, y=yvals_iron)

    fig.add_trace(figT.data[0], row=1, col=1)
    fig.add_trace(figS.data[0], row=1, col=2)
    fig.add_trace(figN.data[0], row=1, col=3)
    fig.add_trace(figI.data[0], row=1, col=4)

    fig.update_yaxes(range=[500, 0])

    #customize temp plot
    fig.update_xaxes(title_text='deg C', range=[-5, 35], row=1, col=1)
    fig.update_yaxes(title_text='Depth (m)', row=1, col=1)
    fig.update_layout(xaxis=dict(side='top'), xaxis2=dict(side='top'), xaxis3=dict(side='top'), xaxis4=dict(side='top'))
    fig.update_annotations(yshift=-410)
    fig.update_layout(margin={'l': 0, 'b': 30, 'r': 0, 't': 30})

    #customize sal plot
    fig.update_xaxes(title_text='', range=[32, 37], row=1, col=2)

    # customize nit plot
    fig.update_xaxes(title_text="umol/kg", range=[0, 45], row=1, col=3)

    # customize iron plot
    fig.update_xaxes(title_text="nmol/kg", range=[0, 2], row=1, col=4)

    return fig

fig = initialize_subplots()

#Suplot graph
@app.callback(
    Output(component_id='subplots', component_property='figure'),
    Input(component_id='map', component_property='hoverData'),
    Input(component_id='map', component_property='clickData'),
    Input(component_id='cruise', component_property='value')
)
def update_subplots(hov_data, click_data, cruise):
    if hov_data != None:
        lat, lon = get_hov_lat_lon_values(hov_data, cruise)
    else:
        if (dash.callback_context.triggered[0]['prop_id'].split('.')[0] == 'cruise'):
            lat, lon = get_click_lat_lon_values(click_data, cruise, True)
        else:
            lat, lon = get_click_lat_lon_values(click_data, cruise, False)

    xvals_temp, yvals_temp = get_x_y_values(cruise, lat, lon, 'Temperature')
    xvals_sal, yvals_sal = get_x_y_values(cruise, lat, lon, 'Salinity')
    xvals_nit, yvals_nit = get_x_y_values(cruise, lat, lon, 'Nitrate')
    xvals_iron, yvals_iron = get_x_y_values(cruise, lat, lon, 'Iron')

    fig.data[0].update(x=xvals_temp, y=yvals_temp)
    fig.data[1].update(x=xvals_sal, y=yvals_sal)
    fig.data[2].update(x=xvals_nit, y=yvals_nit)
    fig.data[3].update(x=xvals_iron, y=yvals_iron)

    return fig




def initialize_cruise(fig, cruise):
    if cruise == 'GIPY0405':
        fig.add_trace(go.Scattermapbox(lat=[GIPY0405['Latitude'][0]], lon=[GIPY0405['Longitude'][0]],
                                       showlegend=False,
                                       hovertemplate="<b>" + GIPY0405['Station'][
                                           0] + "</b><br><br>Latitude=%{lat} </br> Longitude=%{lon}<extra></extra>",
                                       mode='markers', marker=go.scattermapbox.Marker(size=10, color='rgb(255, 0, 0)')))
    elif cruise == 'GA03':
        fig.add_trace(go.Scattermapbox(lat=[GA03['Latitude'][0]], lon=[GA03['Longitude'][0]],
                                       showlegend=False,
                                       hovertemplate="<b>" + GA03['Station'][
                                           0] + "</b><br><br>Latitude=%{lat} </br> Longitude=%{lon}<extra></extra>",
                                       mode='markers', marker=go.scattermapbox.Marker(size=10, color='rgb(255, 0, 0)')))
    elif cruise == 'GP02':
        fig.add_trace(go.Scattermapbox(lat=[GP02['Latitude'][0]], lon=[GP02['Longitude'][0]],
                                       showlegend=False,
                                       hovertemplate="<b>" + GP02['Station'][
                                           0] + "</b><br><br>Latitude=%{lat} </br> Longitude=%{lon}<extra></extra>",
                                       mode='markers', marker=go.scattermapbox.Marker(size=10, color='rgb(255, 0, 0)')))
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
    # Dot color, map type and map zoom are interactive.
    # code from https://plotly.com/python/mapbox-layers/ without the "fig.show".

    if color_checkbox == ['blue']:
        dotcolor = "blue"
    else:
        dotcolor = 'fuchsia'

    if cruise == 'GIPY0405':
        fig = px.scatter_mapbox(GIPY0405, lat="Latitude", lon="Longitude", hover_name="Station",
                                color_discrete_sequence=[dotcolor], zoom=1.2, center=dict(lat=-50, lon=0))
    elif cruise == 'GA03':
        fig = px.scatter_mapbox(GA03, lat="Latitude", lon="Longitude", hover_name="Station", color_discrete_sequence=[dotcolor],
                                zoom=1.2)
    elif cruise == 'GP02':
        fig = px.scatter_mapbox(GP02, lat="Latitude", lon="Longitude", hover_name="Station", color_discrete_sequence=[dotcolor],
                                zoom=1.2)

    if (click_data is None) | (dash.callback_context.triggered[0]['prop_id'].split('.')[0] == 'cruise'): #determines which of the inputs was changed
        initialize_cruise(fig, cruise) #initializes the click for the new cruise
    else:
        # adding markers from: https://plotly.com/python/scattermapbox/
        fig.add_trace(go.Scattermapbox(lat=[click_data['points'][0]['lat']], lon=[click_data['points'][0]['lon']], showlegend=False,
                                       hovertemplate = "<b>" + click_data['points'][0]['hovertext'] + "</b><br><br>Latitude=%{lat} </br> Longitude=%{lon}<extra></extra>",
                                       mode='markers', marker=go.scattermapbox.Marker(size=10, color='rgb(255, 0, 0)')))



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

    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, title=cruise)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
