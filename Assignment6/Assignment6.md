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

### QUESTION 1
NO3_1A = pd.read_csv("./data/1ANO3.csv", skiprows=10)
NO3_1B = pd.read_csv("./data/1BNO3.csv", skiprows=10)
P_1A = pd.read_csv("./data/1AP.csv", skiprows=10)
P_1B = pd.read_csv("./data/1BP.csv", skiprows=10)
Si_1A = pd.read_csv("./data/1ASi.csv", skiprows=10)
Si_1B = pd.read_csv("./data/1BSi.csv", skiprows=10)
T_1A = pd.read_csv("./data/1AT.csv", skiprows=10)
T_1B = pd.read_csv("./data/1BT.csv", skiprows=10)

plt.rcParams['figure.figsize'] = [15, 5]

def plot_q1(data_A, data_B, data_type, data_name):
    plt.subplot(1, 2, 1)
    plt.plot(pd.to_datetime(data_A['DATETIME']).dt.month_name().str.slice(stop=3), data_A[data_name])
    plt.grid()
    plt.ylabel(data_type)
    plt.title("Location A, " + data_type)

    plt.subplot(1, 2, 2)
    plt.plot(pd.to_datetime(data_B['DATETIME']).dt.month_name().str.slice(stop=3), data_B[data_name])
    plt.grid()
    plt.ylabel(data_type)
    plt.title("Location B, " + data_type)
    plt.show()

plot_q1(T_1A, T_1B, "Temperature", 'T0112AN1')
plot_q1(NO3_1A, NO3_1B, "Nitrate", 'N0112AN1')
plot_q1(P_1A, P_1B, "Phosphate", 'P0112AN1')
plot_q1(Si_1A, Si_1B, "Silicate", 'I0112AN1')
```

```{code-cell} ipython3
import matplotlib.pyplot as plt
import pandas as pd

### QUESTION 2
NO3_2A = pd.read_csv("./data/2ANO3.csv", skiprows=10)
NO3_2B = pd.read_csv("./data/2BNO3.csv", skiprows=9)
P_2A = pd.read_csv("./data/2AP.csv", skiprows=10)
P_2B = pd.read_csv("./data/2BP.csv", skiprows=10)
Si_2A = pd.read_csv("./data/2ASi.csv", skiprows=10)
Si_2B = pd.read_csv("./data/2BSi.csv", skiprows=10)
T_2A = pd.read_csv("./data/2AT.csv", skiprows=10)
T_2B = pd.read_csv("./data/2BT.csv", skiprows=10)

plt.rcParams['figure.figsize'] = [15, 5]

def plot_q2(data_A, data_B, data_type, data_name):
    plt.subplot(1, 2, 1)
    plt.tricontourf(data_A['TIME'], -data_A['DEP'], data_A[data_name], 12)
    plt.colorbar()
    plt.ylabel("Depth")
    plt.title("Location A, " + data_type)
    old_labels = data_A['TIME'].values.reshape(12, 12)[:,1]
    new_labels = pd.to_datetime(data_A['DATETIME']).dt.month_name().str.slice(stop=3).values.reshape(12, 12)[:,1]
    plt.xticks(old_labels, new_labels)

    plt.subplot(1, 2, 2)
    plt.tricontourf(data_B['TIME'], -data_B['DEP'], data_B[data_name], 12)
    plt.colorbar()
    plt.ylabel("Depth")
    plt.title("Location B, " + data_type)
    old_labels = T_2B['TIME'].values.reshape(12, 12)[:,1]
    new_labels = pd.to_datetime(data_B['DATETIME']).dt.month_name().str.slice(stop=3).values.reshape(12, 12)[:,1]
    plt.xticks(old_labels, new_labels)
    plt.show()

plot_q2(T_2A, T_2B, "Temperature", 'T0112AN1')
plot_q2(NO3_2A, NO3_2B, "Nitrate", 'N0112AN1')
plot_q2(P_2A, P_2B, "Phosphate", 'P0112AN1')
plot_q2(Si_2A, Si_2B, "Silicate", 'I0112AN1')
```

```{code-cell} ipython3
import matplotlib.pyplot as plt
import pandas as pd

### QUESTION 3
NO3_3 = pd.read_csv("./data/3NO3.csv", skiprows=10)
T_3 = pd.read_csv("./data/3T.csv", skiprows=10)

plt.rcParams['figure.figsize'] = [15, 5]
plt.subplot(1, 2, 1)
plt.tricontourf(NO3_3['LON'], NO3_3['TIME'], NO3_3['N0112AN1'], 12)
plt.colorbar()
plt.xlabel("Longitude")
plt.title("Nitrate")
old_labels = NO3_3['TIME'].values.reshape(12, 26)[:,1]
new_labels = pd.to_datetime(NO3_3['DATETIME']).dt.month_name().str.slice(stop=3).values.reshape(12, 26)[:,1]
plt.yticks(old_labels, new_labels)

plt.subplot(1, 2, 2)
plt.tricontourf(T_3['LON'], T_3['TIME'], T_3['T0112AN1'], 12)
plt.colorbar()
plt.xlabel("Longitude")
plt.title("Temperature")
old_labels = T_3['TIME'].values.reshape(12, 26)[:,1]
new_labels = pd.to_datetime(T_3['DATETIME']).dt.month_name().str.slice(stop=3).values.reshape(12, 26)[:,1]
plt.yticks(old_labels, new_labels)
plt.show()

plt.tight_layout()
```

```{code-cell} ipython3

```
