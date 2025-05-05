import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 15

weight_file = "curated/11_7/p/p9/pv9_v9_paviaU_30.csv"
df = pd.read_csv(weight_file)
last_row = df.iloc[-1]
weights = [val for col, val in last_row.items() if col.startswith('weight_')]
weights = np.array(weights)

data = pd.read_csv("data/paviaU.csv").to_numpy()
data = data[data[:, -1] != 0]
signals = data[:, :-1]
scaler = MinMaxScaler()
signals = scaler.fit_transform(signals)

fig, axes = plt.subplots(1, 2, figsize=(10, 3))

signal = signals[90]
axes[0].plot(signal)
axes[0].set_ylabel("Normalized reflectance")
axes[0].set_xlabel("Band index\n(a)")

signal2 = signal * weights
axes[1].plot(signal2)
axes[1].set_ylabel("Recalibrated reflectance")
axes[1].set_xlabel("Band index\n(b)")

plt.tight_layout()
plt.savefig("plots2/recal_plotter.png", pad_inches=0.14, bbox_inches='tight')
plt.show()
