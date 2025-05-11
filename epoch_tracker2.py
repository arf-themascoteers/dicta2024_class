import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 18

colors = list(plt.get_cmap("tab20").colors) + list(plt.get_cmap("tab20b").colors[:5])

df = pd.read_csv('epoch_tracker/epochs2.csv')
df = df[df["epoch"]<=40]
df["epoch"] = df["epoch"]*50

print(df["selected_bands"].iloc[-1])

epochs = df['epoch']
band_lists = df['selected_bands'].apply(lambda x: list(map(int, x.split('|'))))
band_array = np.vstack(band_lists.to_numpy())

plt.figure(figsize=(10, 8))

print(band_array[-1,:])

for i in range(band_array.shape[1]-1,-1,-1):
    plt.plot(epochs, band_array[:, i], label=f'Target index {i+1}', color=colors[i])

plt.xlabel('Epoch')
plt.ylabel('Band index')
plt.legend(
    loc='center left',
    bbox_to_anchor=(1.0, 0.5),
    ncol=1,
    fontsize=16,
    columnspacing=1  # default is 2.0; reduce or increase as needed
)
#plt.text(0.5, -0.2, '(a)', transform=plt.gca().transAxes, ha='center', va='center')

plt.tight_layout()
plt.savefig('plots2/epoch_tracker_band_only.png', dpi=300, pad_inches=0.14, bbox_inches='tight')
plt.show()
