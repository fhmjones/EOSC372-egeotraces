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

GA03 = pd.read_csv("./data/GA03_w.csv")
GIPY05 = pd.read_csv("./data/GIPY_05e.csv")
GP02 = pd.read_csv("./data/GP02_w.csv")

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
#'Longitude [degrees_east]'
#'Latitude [degrees_north]'
#'PRESSURE [dbar]'
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
A_stations = all_A_stations
B_stations = [all_B_stations[i] for i in (10,16,24,26)]

#Temperature
plt.rcParams['figure.figsize'] = [15, 5]
plt.subplot(1, 2, 1)
plt.scatter(GIPY05_temp[GIPY05_lat >= -45], GIPY05_depth[GIPY05_lat >= -45])
plt.xlabel("Temperature")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('north of 45S')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GIPY05_temp[GIPY05_stations == s], GIPY05_depth[GIPY05_stations == s], label=s)
plt.xlabel("Temperature")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('south of 65S')
plt.legend()
plt.show()

#Nitrate
plt.subplot(1, 2, 1)
plt.scatter(GIPY05_nitrate[GIPY05_lat >= -45], GIPY05_depth[GIPY05_lat >= -45])
plt.xlabel("Nitrate")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('north of 45S')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GIPY05_nitrate[GIPY05_stations == s], GIPY05_depth[GIPY05_stations == s], label=s)
plt.xlabel("Nitrate")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('south of 65S')
plt.legend()
plt.show()

#Iron
plt.subplot(1, 2, 1)
plt.scatter(GIPY05_iron[GIPY05_lat >= -45], GIPY05_depth[GIPY05_lat >= -45])
plt.xlabel("Iron")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('north of 45S')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GIPY05_iron[GIPY05_stations == s], GIPY05_depth[GIPY05_stations == s], label=s)
plt.xlabel("Iron")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('south of 65S')
plt.legend()
plt.show()

#Salinity
plt.subplot(1, 2, 1)
plt.scatter(GIPY05_salinity[GIPY05_lat >= -45], GIPY05_depth[GIPY05_lat >= -45])
plt.xlabel("Salinity")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('north of 45S')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GIPY05_salinity[GIPY05_stations == s], GIPY05_depth[GIPY05_stations == s], label=s)
plt.xlabel("Salinity")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('south of 65S')
plt.legend()
plt.show()

plt.tight_layout()
```

```{code-cell} ipython3
### GA03
#A: 2 depth profiles in the Sargasso Sea (~ 60-65W), and 
#B: 2 depth profiles closest to the coast on the east side (close to the Sahara Desert)


#DUPLICATE STATIONS
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


#Temperature
plt.rcParams['figure.figsize'] = [15, 5]
plt.subplot(1, 2, 1)
for s in A_stations:
    plt.scatter(GA03_temp[GA03_stations == s], GA03_depth[GA03_stations == s], label=s)
plt.xlabel("Temperature")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.legend()
plt.title('60-65W')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GA03_temp[GA03_stations == s], GA03_depth[GA03_stations == s], label=s)
plt.xlabel("Temperature")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('0-25W')
plt.legend()
plt.show()

#Nitrate
plt.subplot(1, 2, 1)
for s in A_stations:
    plt.scatter(GA03_nitrate[GA03_stations == s], GA03_depth[GA03_stations == s], label=s)
plt.xlabel("Nitrate")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.legend()
plt.title('60-65W')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GA03_nitrate[GA03_stations == s], GA03_depth[GA03_stations == s], label=s)
plt.xlabel("Nitrate")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('0-25W')
plt.legend()
plt.show()

#Iron
plt.subplot(1, 2, 1)
for s in A_stations:
    plt.scatter(GA03_iron[GA03_stations == s], GA03_depth[GA03_stations == s], label=s)
plt.xlabel("Iron")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.legend()
plt.title('60-65W')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GA03_iron[GA03_stations == s], GA03_depth[GA03_stations == s], label=s)
plt.xlabel("Iron")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('0-25W')
plt.legend()
plt.show()

#Salinity
plt.subplot(1, 2, 1)
for s in A_stations:
    plt.scatter(GA03_salinity[GA03_stations == s], GA03_depth[GA03_stations == s], label=s)
plt.xlabel("Salinity")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.legend()
plt.title('60-65W')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GA03_salinity[GA03_stations == s], GA03_depth[GA03_stations == s], label=s)
plt.xlabel("Salinity")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('0-25W')
plt.legend()
plt.show()

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

#Temperature
plt.rcParams['figure.figsize'] = [15, 5]
plt.subplot(1, 2, 1)
for s in A_stations:
    plt.scatter(GP02_temp[GP02_stations == s], GP02_depth[GP02_stations == s], label=s)
plt.xlabel("Temperature")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.legend()
plt.title('East side (<155E)')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GP02_temp[GP02_stations == s], GP02_depth[GP02_stations == s], label=s)
plt.xlabel("Temperature")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('West side (>180E)')
plt.legend()
plt.show()

#Nitrate
plt.subplot(1, 2, 1)
for s in A_stations:
    plt.scatter(GP02_nitrate[GP02_stations == s], GP02_depth[GP02_stations == s], label=s)
plt.xlabel("Nitrate")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.legend()
plt.title('East side (<155E)')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GP02_nitrate[GP02_stations == s], GP02_depth[GP02_stations == s], label=s)
plt.xlabel("Nitrate")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('West side (>180E)')
plt.legend()
plt.show()

#Iron
plt.subplot(1, 2, 1)
for s in A_stations:
    plt.scatter(GP02_iron[GP02_stations == s], GP02_depth[GP02_stations == s], label=s)
plt.xlabel("Iron")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.legend()
plt.title('East side (<155E)')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GP02_iron[GP02_stations == s], GP02_depth[GP02_stations == s], label=s)
plt.xlabel("Iron")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('West side (>180E)')
plt.legend()
plt.show()

#Salinity
plt.subplot(1, 2, 1)
for s in A_stations:
    plt.scatter(GP02_salinity[GP02_stations == s], GP02_depth[GP02_stations == s], label=s)
plt.xlabel("Salinity")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.legend()
plt.title('East side (<155E)')

plt.subplot(1, 2, 2)
for s in B_stations:
    plt.scatter(GP02_salinity[GP02_stations == s], GP02_depth[GP02_stations == s], label=s)
plt.xlabel("Salinity")
plt.ylabel("Depth (m)")
plt.ylim([0, 500])
plt.title('West side (>180E)')
plt.legend()
plt.show()

plt.tight_layout()
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
