import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 22


paths = [
    'curated/11_7/i/iv9/iv9_v9_indian_pines_30.csv',
    'curated/11_7/p/p9/pv9_v9_paviaU_30.csv',
    'curated/11_7/s/sv9_v9_salinas_30.csv',
    "curated/v9_v9_ghisaconus_30.csv"
]

labels = ["(a)", "(b)", "(c)", "(d)"]



fig, axes = plt.subplots(2, 2, figsize=(18,8))
axes = axes.ravel()
dss = ["Indian Pines", "Pavia University", "Salinas","Ghisaconus"]
for idx, path in enumerate(paths):
    df = pd.read_csv(path)
    last_row = df.iloc[-1]
    weights = {int(col.split('_')[1]): val for col, val in last_row.items() if col.startswith('weight_')}
    sorted_weights = dict(sorted(weights.items(), key=lambda item: item[1], reverse=True)[:30])
    axes[idx].bar(range(len(sorted_weights)), sorted_weights.values())
    axes[idx].set_xticks(range(len(sorted_weights)))
    axes[idx].set_xticklabels([key + 1 for key in sorted_weights.keys()])
    axes[idx].set_title(dss[idx])
    axes[idx].set_xlabel('Band number')
    axes[idx].set_ylabel('Weight')
    axes[idx].tick_params(axis='x', rotation=90)
    ymax = axes[idx].get_ylim()[1]
    axes[idx].set_yticks(np.arange(0, ymax + 0.5, 0.5))
    axes[idx].text(0.5, -0.6, labels[idx], transform=axes[idx].transAxes,
                   ha='center', va='center')

#plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0.3)
plt.subplots_adjust(hspace=1.2)
plt.tight_layout()
plt.savefig('class_bar_sb.png')
plt.show()
