---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.11.2
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

```{code-cell} ipython3
import matplotlib.pyplot as plt
import pandas as pd

GA03 = pd.read_csv("./data/GA03w.csv")
GIPY05 = pd.read_csv("./data/GIPY05e.csv")
GP02 = pd.read_csv("./data/GP02w.csv")
GIPY04 = pd.read_csv("./data/GIPY04.csv")

GA03_stations = GA03['Station']
GA03_lat = GA03['Latitude [degrees_north]']
GA03_lon = GA03['Longitude [degrees_east]']
GA03_depth = GA03['DEPTH [m]']
GA03_temp = GA03['CTDTMP [deg C]']
GA03_salinity = GA03['CTDSAL']
GA03_nitrate = GA03['NITRATE_D_CONC_BOTTLE [umol/kg]']
GA03_iron = GA03['Fe_D_CONC_BOTTLE [nmol/kg]']

GIPY05_stations = GIPY05['Station']
GIPY05_lat = GIPY05['Latitude [degrees_north]']
GIPY05_lon = GIPY05['Longitude [degrees_east]']
GIPY05_depth = GIPY05['DEPTH [m]']
GIPY05_temp = GIPY05['CTDTMP [deg C]']
GIPY05_salinity = GIPY05['CTDSAL']
GIPY05_nitrate = GIPY05['NO2+NO3_D_CONC_BOTTLE [umol/kg]']
GIPY05_iron = GIPY05['Fe_D_CONC_BOTTLE [nmol/kg]']

GP02_stations = GP02['Station']
GP02_lat = GP02['Latitude [degrees_north]']
GP02_lon = GP02['Longitude [degrees_east]']
GP02_depth = GP02['DEPTH [m]']
GP02_temp = GP02['CTDTMP [deg C]']
GP02_salinity = GP02['CTDSAL']
GP02_nitrate = GP02['NO2+NO3_D_CONC_BOTTLE [umol/kg]']
GP02_iron = GP02['Fe_D_CONC_BOTTLE [nmol/kg]']

GIPY04_stations = GIPY04['Station']
GIPY04_lat = GIPY04['Latitude [degrees_north]']
GIPY04_lon = GIPY04['Longitude [degrees_east]']
GIPY04_depth = GIPY04['DEPTH [m]']
GIPY04_temp = GIPY04['CTDTMP [deg C]']
GIPY04_salinity = GIPY04['CTDSAL']
GIPY04_nitrate = GIPY04['NITRATE_D_CONC_BOTTLE [umol/kg]']
GIPY04_iron = GIPY04['Fe_D_CONC_BOTTLE [nmol/kg]']


#'Longitude [degrees_east]'
#'Latitude [degrees_north]'
#'PRESSURE [dbar]'
#'DEPTH [m]'
#'CTDTMP [deg C]'
#'CTDSAL'
#'SALINITY_D_CONC_BOTTLE'
#'SALINITY_D_CONC_PUMP'
#'SALINITY_D_CONC_FISH'
#'SALINITY_D_CONC_UWAY'
#'NITRATE_D_CONC_BOTTLE [umol/kg]'
#'NITRATE_D_CONC_PUMP [umol/kg]'
#'NITRATE_D_CONC_FISH [umol/kg]'
#'NITRATE_D_CONC_UWAY [umol/kg]'
#'NITRATE_LL_D_CONC_BOTTLE [umol/kg]'
#'NITRATE_LL_D_CONC_FISH [umol/kg]'
#'NO2+NO3_D_CONC_BOTTLE [umol/kg]'
#'NO2+NO3_D_CONC_FISH [umol/kg]'
#'Fe_D_CONC_BOTTLE [nmol/kg]'
#'Fe_D_CONC_FISH [nmol/kg]'
#'Fe_II_D_CONC_BOTTLE [nmol/kg]'
#'Fe_II_D_CONC_FISH [nmol/kg]'
#'Fe_S_CONC_BOTTLE [nmol/kg]'
#'Fe_S_CONC_FISH [nmol/kg]'
```

```{code-cell} ipython3
### GIPY05
#A: 4 depth profiles north of 45S
#B: 4 depth profiles south of 65S


#Get all stations in desired ranges
all_A_stations = []
all_B_stations = []
for i in range(len(GIPY05_lat)):
    if (GIPY05_lat[i] >= -45):
        if len(all_A_stations) == 0 or all_A_stations[-1] != GIPY05_stations[i]:
            all_A_stations.append(GIPY05_stations[i])
    if (GIPY05_lat[i] <= -65):
        if len(all_B_stations) == 0 or all_B_stations[-1] != GIPY05_stations[i]:
            all_B_stations.append(GIPY05_stations[i])
A_stations = [all_A_stations[i] for i in (1, 3, 4, 5)]
B_stations = [all_B_stations[i] for i in (10,16,24,26)]

plt.rcParams['figure.figsize'] = [15, 5]
def plot_GIPY05_profile(data, data_type):
    plt.subplot(1, 2, 1)
    for s in A_stations:
        plt.scatter(data[GIPY05_stations == s], GIPY05_depth[GIPY05_stations == s], label=s)
    plt.xlabel(data_type)
    plt.ylabel("Depth (m)")
    plt.ylim([0, 500])
    plt.title('north of 45S')
    plt.legend()
    plt.gca().invert_yaxis()

    plt.subplot(1, 2, 2)
    for s in B_stations:
        plt.scatter(data[GIPY05_stations == s], GIPY05_depth[GIPY05_stations == s], label=s)
    plt.xlabel(data_type)
    plt.ylabel("Depth (m)")
    plt.ylim([0, 500])
    plt.title('south of 65S')
    plt.legend()
    plt.gca().invert_yaxis()
    plt.show()

plot_GIPY05_profile(GIPY05_temp, "Temperature")
plot_GIPY05_profile(GIPY05_nitrate, "Nitrate")
plot_GIPY05_profile(GIPY05_iron, "Iron")
plot_GIPY05_profile(GIPY05_salinity, "Salinity")

plt.tight_layout()
```

```{code-cell} ipython3
### GIPY05
#A: 4 depth profiles north of 45S #3 profiles from GIPY04
#B: 4 depth profiles south of 65S


#Get all stations in desired ranges
all_A_stations_04 = []
all_A_stations_05 = []
all_B_stations = []
for i in range(len(GIPY05_lat)):
    if (GIPY05_lat[i] >= -45):
        if len(all_A_stations_05) == 0 or all_A_stations_05[-1] != GIPY05_stations[i]:
            all_A_stations_05.append(GIPY05_stations[i])
    if (GIPY05_lat[i] <= -65):
        if len(all_B_stations) == 0 or all_B_stations[-1] != GIPY05_stations[i]:
            all_B_stations.append(GIPY05_stations[i])
for i in range(len(GIPY04_lat)):
    if (GIPY04_lat[i] >= -45) & (GIPY04_lat[i] <= -35):
        if len(all_A_stations_04) == 0 or all_A_stations_04[-1] != GIPY04_stations[i]:
            all_A_stations_04.append(GIPY04_stations[i])
            
A_stations_05 = [all_A_stations_05[4]]
A_stations_04 = [all_A_stations_04[i] for i in (5,18,21)]
B_stations = [all_B_stations[i] for i in (10,16,24,26)]

plt.rcParams['figure.figsize'] = [15, 5]

def plot_GIPY05_profile(data_05, data_04, data_type):
    #Temperature
    plt.subplot(1, 2, 1)
    for s in A_stations_05:
        plt.scatter(data_05[GIPY05_stations == s], GIPY05_depth[GIPY05_stations == s], label=s)
    for s in A_stations_04:
        plt.scatter(data_04[GIPY04_stations == s], GIPY04_depth[GIPY04_stations == s], label=s)
    plt.xlabel(data_type)
    plt.ylabel("Depth (m)")
    plt.ylim([0, 500])
    plt.title('north of 45S')
    plt.legend()
    plt.gca().invert_yaxis()

    plt.subplot(1, 2, 2)
    for s in B_stations:
        plt.scatter(data_05[GIPY05_stations == s], GIPY05_depth[GIPY05_stations == s], label=s)
    plt.xlabel(data_type)
    plt.ylabel("Depth (m)")
    plt.ylim([0, 500])
    plt.title('south of 65S')
    plt.legend()
    plt.gca().invert_yaxis()
    plt.show()

plot_GIPY05_profile(GIPY05_temp, GIPY04_temp, "Temperature")
plot_GIPY05_profile(GIPY05_nitrate, GIPY04_nitrate, "Nitrate")
plot_GIPY05_profile(GIPY05_iron, GIPY04_iron, "Iron")
plot_GIPY05_profile(GIPY05_salinity, GIPY04_salinity, "Salinity")

plt.tight_layout()
```

```{code-cell} ipython3
### GA03
#A: 2 depth profiles in the Sargasso Sea (~ 60-65W), and 
#B: 2 depth profiles closest to the coast on the east side (close to the Sahara Desert)


#Get all stations in desired ranges
all_A_stations = []
all_B_stations = []
for i in range(len(GA03_lon)):
    if (GA03_lon[i] <= 360-60) & (GA03_lon[i] >= 360-65):
        if len(all_A_stations) == 0 or all_A_stations[-1] != GA03_stations[i]:
            all_A_stations.append(GA03_stations[i])
    if (GA03_lon[i] <= 360) & (GA03_lon[i] >= 360-25):
        if len(all_B_stations) == 0 or all_B_stations[-1] != GA03_stations[i]:
            all_B_stations.append(GA03_stations[i])
A_stations = all_A_stations
B_stations = [all_B_stations[i] for i in (1,3)]

plt.rcParams['figure.figsize'] = [15, 5]

def plot_GA03_profile(data, data_type):
    plt.subplot(1, 2, 1)
    for s in A_stations:
        plt.scatter(data[GA03_stations == s], GA03_depth[GA03_stations == s], label=s)
    plt.xlabel(data_type)
    plt.ylabel("Depth (m)")
    plt.ylim([0, 500])
    plt.title('north of 45S')
    plt.legend()
    plt.gca().invert_yaxis()

    plt.subplot(1, 2, 2)
    for s in B_stations:
        plt.scatter(data[GA03_stations == s], GA03_depth[GA03_stations == s], label=s)
    plt.xlabel(data_type)
    plt.ylabel("Depth (m)")
    plt.ylim([0, 500])
    plt.title('south of 65S')
    plt.legend()
    plt.gca().invert_yaxis()
    plt.show()

plot_GA03_profile(GA03_temp, "Temperature")
plot_GA03_profile(GA03_nitrate, "Nitrate")
plot_GA03_profile(GA03_iron, "Iron")
plot_GA03_profile(GA03_salinity, "Salinity")

plt.tight_layout()
```

```{code-cell} ipython3
### GP02
#A: 2 depth profiles closest to the east side and 
#B: 2 depth profiles closest to the west side

#Get all stations in desired ranges
all_A_stations = []
all_B_stations = []
for i in range(len(GP02_lon)):
    if (GP02_lon[i] <= 155):
        if len(all_A_stations) == 0 or all_A_stations[-1] != GP02_stations[i]:
            all_A_stations.append(GP02_stations[i])
    if (GP02_lon[i] >= 180):
        if len(all_B_stations) == 0 or all_B_stations[-1] != GP02_stations[i]:
            all_B_stations.append(GP02_stations[i])
A_stations = [all_A_stations[i] for i in (2,3)]
B_stations = all_B_stations

plt.rcParams['figure.figsize'] = [15, 5]

def plot_GP02_profile(data, data_type):
    plt.subplot(1, 2, 1)
    for s in A_stations:
        plt.scatter(data[GP02_stations == s], GP02_depth[GP02_stations == s], label=s)
    plt.xlabel(data_type)
    plt.ylabel("Depth (m)")
    plt.ylim([0, 500])
    plt.title('north of 45S')
    plt.legend()
    plt.gca().invert_yaxis()

    plt.subplot(1, 2, 2)
    for s in B_stations:
        plt.scatter(data[GP02_stations == s], GP02_depth[GP02_stations == s], label=s)
    plt.xlabel(data_type)
    plt.ylabel("Depth (m)")
    plt.ylim([0, 500])
    plt.title('south of 65S')
    plt.legend()
    plt.gca().invert_yaxis()
    plt.show()

plot_GP02_profile(GP02_temp, "Temperature")
plot_GP02_profile(GP02_nitrate, "Nitrate")
plot_GP02_profile(GP02_iron, "Iron")
plot_GP02_profile(GP02_salinity, "Salinity")

plt.tight_layout()
```

```{code-cell} ipython3

```
