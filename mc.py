import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("mc.csv")

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 22

df = pd.read_csv("mc.csv")
datasets_param = [col.replace("param_", "") for col in df.columns if col.startswith("param_")]
datasets_time = [col.replace("time_", "") for col in df.columns if col.startswith("time_")]
algorithms = df["algorithm"]

param_data = {ds: df[f"param_{ds}"].values for ds in datasets_param}
time_data = {ds: df[f"time_{ds}"].values for ds in datasets_time}

x = np.arange(len(datasets_param))
width = 0.25

fig, axs = plt.subplots(2, 1, figsize=(12, 8))

for ax, data, title in zip(axs, [param_data, time_data], ["param_DATASET", "time_DATASET"]):
    for i in range(len(algorithms)):
        values = [data[ds][i] for ds in data]
        ax.bar(x + i * width, values, width, label=algorithms[i])
    ax.set_xticks(x + width)
    ax.set_xticklabels(list(data.keys()), rotation=45, ha="right")
    ax.set_ylabel("Scale")
    ax.set_title(title)
    ax.legend()

plt.tight_layout()
plt.show()