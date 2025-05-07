import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, LogLocator, NullFormatter

root = "time_figs"
os.makedirs(root, exist_ok=True)
df_original = pd.read_csv("temp_curated2_spa2/loc_combined_summary.csv")

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 18

order = ["spa2", "bsdr"]
ALGS = {
    "spa2": "SPA",
    "bsdr": "Proposed BSDR"
}
COLORS = {
    "spa2": "green",
    "bsdr": "purple",
}
DSS = {
    "indian_pines": "Indian Pines",
    "paviaU": "Pavia University",
    "salinas": "Salinas",
    "ghisaconus": "GHISACONUS"
}

df_original['algorithm'] = pd.Categorical(df_original['algorithm'], categories=order, ordered=True)
df_original = df_original.sort_values('algorithm')
df_original = df_original[(df_original["algorithm"].isin(order)) & (df_original["target_size"].isin([5, 10, 15, 20, 25, 30]))]
df_original.to_csv("temp_curated2_spa2/loc_combined_summary_sorted.csv", index=False)

metric = "time"
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
axs = axs.flatten()

for idx, (dataset_key, dataset_name) in enumerate(DSS.items()):
    dataset_df = df_original[df_original["dataset"] == dataset_key].copy()
    dataset_df = dataset_df.sort_values(by="target_size")
    ax = axs[idx]

    for alg_key in order:
        alg_df = dataset_df[dataset_df["algorithm"] == alg_key]
        if alg_df.empty:
            continue
        x = alg_df["target_size"]
        y = alg_df[metric]
        label = ALGS[alg_key]
        color = COLORS[alg_key]
        ax.plot(x, y, label=label, color=color, marker='o', linestyle='-')

    ax.set_title(dataset_name)
    ax.set_xlabel("Target size")
    ax.set_yscale("log")
    ax.set_ylabel(r"Training time ($\log_{10}$ scale)")
    ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=10))
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=100))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.grid(True, linestyle='-', alpha=0.6)

handles, labels = axs[-1].get_legend_handles_labels()
fig.legend(
    handles, labels,
    loc='upper center',
    ncol=2,
    bbox_to_anchor=(0.27, 1.01)
)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])

out_path = os.path.join(root, "classification", metric)
os.makedirs(out_path, exist_ok=True)
fig.savefig(os.path.join(out_path, "combined_2x2.png"), dpi=300, bbox_inches='tight')
plt.show()
plt.close(fig)
