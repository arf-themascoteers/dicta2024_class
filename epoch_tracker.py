import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 18

colors = plt.get_cmap("Set1").colors

df = pd.read_csv('epoch_tracker/epochs.csv')
df["epoch"] = df["epoch"]*4

epochs = df['epoch']
oa = df['oa']
aa = df['aa']
kappa = df['k']
band_lists = df['selected_bands'].apply(lambda x: list(map(int, x.split('|'))))
band_array = np.vstack(band_lists.to_numpy())

fig, axs = plt.subplots(1, 2, figsize=(12, 10))

# Combined OA, AA, and Kappa
axs[1].plot(epochs, oa, label='OA', color=colors[0])
axs[1].plot(epochs, aa, label='AA', color=colors[1])
axs[1].plot(epochs, kappa, label='κ', color=colors[2])
#axs[1].set_title('Accuracy Metrics Over Epochs')
axs[1].set_xlabel('Epoch')
axs[1].set_ylabel('Value')
axs[1].legend(loc='upper center', bbox_to_anchor=(0.45, 1.29), ncol=3)

for i in range(band_array.shape[1]-1,-1,-1):
    axs[0].plot(epochs, band_array[:, i], label=f'Target index {i+1}', color=colors[i])
#axs[0].set_title('Band Index Evolution')
axs[0].set_xlabel('Epoch')
axs[0].set_ylabel('Band index')
axs[0].legend(loc='upper center', bbox_to_anchor=(0.5, 1.6), ncol=2)

axs[1].text(0.5, -0.3, '(b)', transform=axs[1].transAxes, ha='center', va='center')
axs[0].text(0.5, -0.3, '(a)', transform=axs[0].transAxes, ha='center', va='center')

fig.tight_layout()
plt.savefig('plots2/epoch_tracker.png', dpi=300, pad_inches=0.14, bbox_inches='tight')
plt.show()
