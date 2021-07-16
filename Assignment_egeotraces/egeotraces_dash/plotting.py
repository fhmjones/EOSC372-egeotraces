import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# see Python routine "parse-csv.py" for the method of filtering data and making these csvs
GIPY05 = pd.read_csv("GIPY05_filtered.csv")
GIPY04 = pd.read_csv("GIPY04_filtered.csv")
GA03 = pd.read_csv("GA03_filtered.csv")
GP02 = pd.read_csv("GP02_filtered.csv")
GIPY0405 = pd.concat([GIPY04, GIPY05], ignore_index=True)

#global variables to keep track of the hovered and clicked stations for plotting
hov_lat, hov_lon, hov_station = None, None, None
click_lat, click_lon, click_station = None, None, None

###SUBPLOTS PLOTTING
#helper functions
#get lat and lons from hoverData
def set_hov_lat_lon_values(hov_data):
    global hov_lat, hov_lon, hov_station
    global click_lat, click_lon, click_station
    if 'hovertext' in hov_data['points'][0]:
        hov_lat = hov_data['points'][0]['lat']
        hov_lon = hov_data['points'][0]['lon']
        hov_station = str(hov_data['points'][0]['hovertext'])
    else:
        hov_lat = click_lat
        hov_lon = click_lon
        hov_station = click_station

#get lat and lons from clickData
def set_click_lat_lon_values(click_data, cruise, new_cruise):
    global click_lat, click_lon, click_station
    if (click_data is None) or (new_cruise == True):  # necessary for startup before interacting with the map.
        #print(cruise)
        if cruise == 'GIPY0405':
            lat = GIPY0405['Latitude'][0]
            lon = GIPY0405['Longitude'][0]
            station = GIPY0405['Station'][0]
        elif cruise == 'GA03':
            lat = GA03['Latitude'][0]
            lon = GA03['Longitude'][0]
            station = GA03['Station'][0]
        elif cruise == 'GP02':
            lat = GP02['Latitude'][0]
            lon = GP02['Longitude'][0]
            station = GP02['Station'][0]
    # when you click on a point that is already clicked, the hovertext is not in the click_data dict
    # in that case, we keep the click_lat, lon and station the same
    elif 'hovertext' not in click_data['points'][0]:
        lat = click_lat
        lon = click_lon
        station = click_station
    else:
        lat = click_data['points'][0]['lat']
        lon = click_data['points'][0]['lon']
        station = str(click_data['points'][0]['hovertext'])

    click_lat, click_lon, click_station = lat, lon, station

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

#figure functions
#initialize the subplots
def initialize_subplots(cruise, y_range):
    global click_lat, click_lon, click_station
    fig = make_subplots(rows=1, cols=5, subplot_titles=("Temperature", "Salinity", "Nitrate", "Iron", "Nitrate:Iron"))

    set_click_lat_lon_values(None, cruise, False)
    lat, lon = click_lat, click_lon

    xvals_temp, yvals_temp = get_x_y_values(cruise, lat, lon, 'Temperature')
    xvals_sal, yvals_sal = get_x_y_values(cruise, lat, lon, 'Salinity')
    xvals_nit, yvals_nit = get_x_y_values(cruise, lat, lon, 'Nitrate')
    xvals_iron, yvals_iron = get_x_y_values(cruise, lat, lon, 'Iron')
    xvals_ratio, yvals_ratio = get_x_y_values(cruise, lat, lon, 'Ratio')

    #traces for clicked data
    figT = px.scatter(x=xvals_temp, y=yvals_temp, color_discrete_sequence=['red'])
    figS = px.scatter(x=xvals_sal, y=yvals_sal, color_discrete_sequence=['red'])
    figN = px.scatter(x=xvals_nit, y=yvals_nit, color_discrete_sequence=['red'])
    figI = px.scatter(x=xvals_iron, y=yvals_iron, color_discrete_sequence=['red'])
    figR = px.scatter(x=xvals_ratio, y=yvals_ratio, color_discrete_sequence=['red'])

    fig.add_trace(figT.data[0], row=1, col=1)
    fig.add_trace(figS.data[0], row=1, col=2)
    fig.add_trace(figN.data[0], row=1, col=3)
    fig.add_trace(figI.data[0], row=1, col=4)
    fig.add_trace(figR.data[0], row=1, col=5)

    #empty traces for hovered data
    figT = px.scatter(x=[0], y=[0], color_discrete_sequence=['blue'])
    figS = px.scatter(x=[0], y=[0], color_discrete_sequence=['blue'])
    figN = px.scatter(x=[0], y=[0], color_discrete_sequence=['blue'])
    figI = px.scatter(x=[0], y=[0], color_discrete_sequence=['blue'])
    figR = px.scatter(x=[0], y=[0], color_discrete_sequence=['blue'])

    fig.add_trace(figT.data[0], row=1, col=1)
    fig.add_trace(figS.data[0], row=1, col=2)
    fig.add_trace(figN.data[0], row=1, col=3)
    fig.add_trace(figI.data[0], row=1, col=4)
    fig.add_trace(figR.data[0], row=1, col=5)

    fig.update_yaxes(range=y_range)
    fig.update_layout(xaxis=dict(side='top'), xaxis2=dict(side='top'), xaxis3=dict(side='top'), xaxis4=dict(side='top'), xaxis5=dict(side='top'))
    fig.update_annotations(yshift=-410)
    fig.update_layout(margin={'l': 0, 'b': 40, 'r': 100, 't': 30})

    #customize y axes
    #fig.update_yaxes(title_text='Depth (m)', row=1, col=1)
    #fig.update_yaxes(visible=False, row=1, col=1)
    #customize x axes
    fig.update_xaxes(title_text='deg C', range=[-5, 35], row=1, col=1)
    fig.update_xaxes(title_text='Practical Salinity', range=[30, 37], row=1, col=2)
    fig.update_xaxes(title_text="umol/kg", range=[-2, 45], row=1, col=3)
    fig.update_xaxes(title_text="nmol/kg", range=[-0.1, 2], row=1, col=4)
    fig.update_xaxes(title_text="", range=[-1000, 1000*650], row=1, col=5)

    if click_lat is not None and click_lon is not None:
        fig['data'][0]['showlegend'] = True
        fig['data'][0]['name'] = str(click_station) + '<br>lat: ' + str("{:.2f}".format(click_lat)) + '<br>lon: ' + str("{:.2f}".format(click_lon))
        fig.update_layout(legend_title_text='Selected Stations from ' + str(cruise))

    return fig

def switch_subplots(hov_data, click_data, cruise, fig, y_range):
    global hov_lat, hov_lon, hov_station
    global click_lat, click_lon, click_station
    set_click_lat_lon_values(click_data, cruise, True)
    lat, lon = click_lat, click_lon

    xvals_temp, yvals_temp = get_x_y_values(cruise, lat, lon, 'Temperature')
    xvals_sal, yvals_sal = get_x_y_values(cruise, lat, lon, 'Salinity')
    xvals_nit, yvals_nit = get_x_y_values(cruise, lat, lon, 'Nitrate')
    xvals_iron, yvals_iron = get_x_y_values(cruise, lat, lon, 'Iron')
    xvals_ratio, yvals_ratio = get_x_y_values(cruise, lat, lon, 'Ratio')

    fig.data[0].update(x=xvals_temp, y=yvals_temp)
    fig.data[1].update(x=xvals_sal, y=yvals_sal)
    fig.data[2].update(x=xvals_nit, y=yvals_nit)
    fig.data[3].update(x=xvals_iron, y=yvals_iron)
    fig.data[4].update(x=xvals_ratio, y=yvals_ratio)

    #update ylim
    fig.update_yaxes(range=y_range)

    #update xlims for temp based on cruise
    if cruise == 'GIPY0405':
        fig.update_xaxes(range=[-5, 25], row=1, col=1)
        fig.update_xaxes(range=[-1000, 1000*650], row=1, col=5)
    elif cruise == 'GA03':
        fig.update_xaxes(range=[5, 35], row=1, col=1)
        fig.update_xaxes(range=[-1000, 1000*50], row=1, col=5)
    elif cruise == 'GP02':
        fig.update_xaxes(range=[0, 30], row=1, col=1)
        fig.update_xaxes(range=[-1000, 1000*250], row=1, col=5)

    #display cruise info
    if click_lat is not None and click_lon is not None:
        fig['data'][0]['showlegend'] = True
        fig['data'][0]['name'] = str(click_station) + '<br>lat: ' + str("{:.2f}".format(click_lat)) + '<br>lon: ' + str("{:.2f}".format(click_lon))
        fig.update_layout(legend_title_text='Selected Stations from ' + str(cruise))


    return fig

def update_subplots(hov_data, click_data, cruise, fig, y_range):
    global click_lat, click_lon, click_station
    global hov_lat, hov_lon, hov_station
    if hov_data != None:
        set_hov_lat_lon_values(hov_data)

        hov_xvals_temp, hov_yvals_temp = get_x_y_values(cruise, hov_lat, hov_lon, 'Temperature')
        hov_xvals_sal, hov_yvals_sal = get_x_y_values(cruise, hov_lat, hov_lon, 'Salinity')
        hov_xvals_nit, hov_yvals_nit = get_x_y_values(cruise, hov_lat, hov_lon, 'Nitrate')
        hov_xvals_iron, hov_yvals_iron = get_x_y_values(cruise, hov_lat, hov_lon, 'Iron')
        hov_xvals_ratio, hov_yvals_ratio = get_x_y_values(cruise, hov_lat, hov_lon, 'Ratio')

        fig.data[5].update(x=hov_xvals_temp, y=hov_yvals_temp)
        fig.data[6].update(x=hov_xvals_sal, y=hov_yvals_sal)
        fig.data[7].update(x=hov_xvals_nit, y=hov_yvals_nit)
        fig.data[8].update(x=hov_xvals_iron, y=hov_yvals_iron)
        fig.data[9].update(x=hov_xvals_ratio, y=hov_yvals_ratio)
    else:
        hov_lat, hov_lon, hov_station = None, None, None
        fig.data[5].update(x=[], y=[])
        fig.data[6].update(x=[], y=[])
        fig.data[7].update(x=[], y=[])
        fig.data[8].update(x=[], y=[])
        fig.data[9].update(x=[], y=[])

    if click_data != None:
        set_click_lat_lon_values(click_data, cruise, False)

        click_xvals_temp, click_yvals_temp = get_x_y_values(cruise, click_lat, click_lon, 'Temperature')
        click_xvals_sal, click_yvals_sal = get_x_y_values(cruise, click_lat, click_lon, 'Salinity')
        click_xvals_nit, click_yvals_nit = get_x_y_values(cruise, click_lat, click_lon, 'Nitrate')
        click_xvals_iron, click_yvals_iron = get_x_y_values(cruise, click_lat, click_lon, 'Iron')
        click_xvals_ratio, click_yvals_ratio = get_x_y_values(cruise, click_lat, click_lon, 'Ratio')

        fig.data[0].update(x=click_xvals_temp, y=click_yvals_temp)
        fig.data[1].update(x=click_xvals_sal, y=click_yvals_sal)
        fig.data[2].update(x=click_xvals_nit, y=click_yvals_nit)
        fig.data[3].update(x=click_xvals_iron, y=click_yvals_iron)
        fig.data[4].update(x=click_xvals_ratio, y=click_yvals_ratio)


    #display cruise info
    if hov_lat is not None and hov_lon is not None:
        fig['data'][5]['showlegend'] = True
        fig['data'][5]['name'] = str(hov_station) + '<br>lat: ' + str("{:.2f}".format(hov_lat)) + '<br>lon: ' + str("{:.2f}".format(hov_lon))
        fig.update_layout(legend_title_text='Selected Stations from ' + str(cruise))
    if click_data is not None:
        fig['data'][0]['showlegend'] = True
        fig['data'][0]['name'] = str(click_station) + '<br>lat: ' + str("{:.2f}".format(click_lat)) + '<br>lon: ' + str("{:.2f}".format(click_lon))
        fig.update_layout(legend_title_text='Selected Stations from ' + str(cruise))

    #update ylim
    fig.update_yaxes(range=y_range)

    return fig




###MAP PLOTTING
#helper functions
def get_dotcolor(color_checkbox):
    if color_checkbox == ['blue']:
        dotcolor = "blue"
    else:
        dotcolor = 'fuchsia'
    return dotcolor

def update_background(background, fig):
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
    return fig

#initializes click marker for map
def map_initialize_cruise(fig, cruise):
    global click_lat, click_lon, click_station
    set_click_lat_lon_values(None, cruise, False)
    fig.add_trace(go.Scattermapbox(lat=[click_lat], lon=[click_lon], showlegend=False, hovertemplate="<b>" + str(click_station) +
                                     "</b><br><br>Latitude=%{lat} </br> Longitude=%{lon}<extra></extra>",
                                   mode='markers', marker=go.scattermapbox.Marker(size=10, color='rgb(255, 0, 0)')))

    return fig

def plot_stations(dotcolor, cruise):
    if cruise == 'GIPY0405':
        fig = px.scatter_mapbox(GIPY0405, lat="Latitude", lon="Longitude", hover_name="Station",
                                color_discrete_sequence=[dotcolor], zoom=1.2, center=dict(lat=-50, lon=0))
    elif cruise == 'GA03':
        fig = px.scatter_mapbox(GA03, lat="Latitude", lon="Longitude", hover_name="Station",
                                color_discrete_sequence=[dotcolor],
                                zoom=1.2)
    elif cruise == 'GP02':
        fig = px.scatter_mapbox(GP02, lat="Latitude", lon="Longitude", hover_name="Station",
                                color_discrete_sequence=[dotcolor],
                                zoom=1.2)
    return fig

#figure functions
def initialize_map(color_checkbox, background, cruise):
    dotcolor = get_dotcolor(color_checkbox)

    fig = plot_stations(dotcolor, cruise)

    fig = map_initialize_cruise(fig, cruise)  # initializes the click for the new cruise

    fig = update_background(background, fig)
    if cruise == 'GIPY0405':
        fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, title='GIPY04 and GIPY05')
    else:
        fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, title=cruise)

    return fig

# update map for cruise changes
def switch_map(color_checkbox, background, cruise, fig):
    fig.data = []

    dotcolor = get_dotcolor(color_checkbox)

    fig = plot_stations(dotcolor, cruise)

    fig = map_initialize_cruise(fig, cruise)  # initializes the click for the new cruise

    update_background(background, fig)

    if cruise == 'GIPY0405':
        fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, title='GIPY04 and GIPY05')
    else:
        fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, title=cruise)

    return fig


def update_map(color_checkbox, background, click_data, cruise, fig):
    global click_lat, click_lon, click_station
    # Dot color, map type and map zoom are interactive.
    # code from https://plotly.com/python/mapbox-layers/ without the "fig.show".
    dotcolor = get_dotcolor(color_checkbox)

    fig = plot_stations(dotcolor, cruise)

    # adding markers from: https://plotly.com/python/scattermapbox/
    if click_lat is not None and click_lon is not None:
        fig.add_trace(go.Scattermapbox(lat=[click_lat], lon=[click_lon], showlegend=False, hovertemplate = "<b>" + click_station +
                                       "</b><br><br>Latitude=%{lat} </br> Longitude=%{lon}<extra></extra>",
                                       mode='markers', marker=go.scattermapbox.Marker(size=10, color='rgb(255, 0, 0)')))
    else:
        fig = map_initialize_cruise(fig, cruise)  # initializes the click for the new cruise
    fig = update_background(background, fig)
    if cruise == 'GIPY0405':
        fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, title='GIPY04 and GIPY05')
    else:
        fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0}, title=cruise)
    return fig