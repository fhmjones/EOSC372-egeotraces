# EOSC 372 Assignments
## Assignment 6
Assignment 6 instructs students to observe certain plots from NOAA data [here](https://data.pmel.noaa.gov/nvods/las/UI.vm).
- Images of each of the plots have been collected and are in the "images" folder.
- Data for each of the plots has been collected and is in the "data" folder.
- Plots have been reconstructed from the data and are in a Jupyter Notebook.
## New Assignment: eGEOTRACES
The eGEOTRACES assignment is the construction of a Dash that displays selected data from the GEOTRACES cruises. 
### Outline
The desired depth profiles are as follows:
- From the GIPY04 and GIPY05e cruises: 4 depth profiles south of 65S and 4 depth profiles north of 45S.
- From the GA03w cruise: 2 depth profiles in the Sargasso Sea and 2 depth profiles close to the Sahara Desert.
- From the GP02w cruise: 2 depth profiles closest to the east side and 2 depth profiles closest to the west side.
### Data Collection
- The data is collected [here](https://www.egeotraces.org/) for the following parameters: nitrate, iron, salinity, temperature.
- The ratio of [nitrate] to [iron] is calculated from this data and added to the csv files.
- Density is calculated from salinity and temperature.
- Data collection and filtering is detailed in the "data_documentation" file.
### Plotting the Data
- The Dash shows a map of the stations for the chosen cruise. Hovering over the stations produces the depth profiles (temperature, salinity, nitrate, iron, ratio of nitrate to iron, density) on subplots below. Clicking on a station creates fixed depth profiles on the subplots below. 
- The subplots show the depth profiles from 0 to 500m depth. This can be adjusted with a slider to the left of the subplots. 
- There are radiobuttons to select a cruise to plot.
- The x-axis range can be changed by radiobuttons. 'default' selects a constant x-axis, and 'fit to data' chooses an x-axis for the current plot.
- The subplots can be saved as a png file to submit.

