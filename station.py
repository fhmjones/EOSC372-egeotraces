colours = [
    "darkred",
    "limegreen",
    "red",
    "sienna",
    "darkorange",
    "darkgreen",
    "darkviolet",
    "deeppink",
]


class Station:
    def __init__(self, type, lat, lon, name, date, colour):
        self.type = type
        self.lat = lat
        self.lon = lon
        self.name = name
        self.date = date
        self.colour = colour


def in_list(lat, lon, list):
    for s in list:
        if (s.lat == lat) & (s.lon == lon):
            return True
    return False


def remove_from_list(lat, lon, list):
    for s in list:
        if (s["lat"] == lat) & (s["lon"] == lon):
            list.remove(s)
    return list


def is_empty(hov_station):
    if (
        (hov_station["lat"] is None)
        & (hov_station["lon"] is None)
        & (hov_station["name"] is None)
        & (hov_station["date"] is None)
    ):
        return True
    else:
        return False


# colours
def contains_colour(list_stations, colour):
    for s in list_stations:
        if s["colour"] == colour:
            return True
    return False


def get_colour(click_stations):  # getting the next colour in the series to plot
    for c in colours:
        if contains_colour(click_stations, c) is False:
            return c
    return "black"


# get lat and lons from hoverData
def get_hov_station(hov_data):
    hov_station = Station("hover", None, None, None, None, "blue").__dict__
    if hov_data is not None:
        # hovering over the clicked point doesn't give 'hovertext', so when there is no hovertext, set the hover data to the current click data
        if "customdata" in hov_data["points"][0]:
            lat = hov_data["points"][0]["lat"]
            lon = hov_data["points"][0]["lon"]
            name = str(hov_data["points"][0]["customdata"][0])
            date = str(hov_data["points"][0]["customdata"][1])
            hov_station = Station("hover", lat, lon, name, date, "blue").__dict__

    return hov_station


# get lat and lons from clickData
def get_click_stations(click_data, click_stations):
    # when you click on a point that is already clicked, the hovertext is not in the click_data dict
    # in that case, we keep the click_lat, lon and station the same
    if click_data is not None:
        if "customdata" not in click_data["points"][0]:
            lat = click_data["points"][0]["lat"]
            lon = click_data["points"][0]["lon"]
            remove_from_list(lat, lon, click_stations)
        else:
            lat = click_data["points"][0]["lat"]
            lon = click_data["points"][0]["lon"]
            name = click_data["points"][0]["customdata"][0]
            date = str(click_data["points"][0]["customdata"][1])
            click_stations.append(
                Station("click", lat, lon, name, date, get_colour(click_stations)).__dict__
            )

    return click_stations
