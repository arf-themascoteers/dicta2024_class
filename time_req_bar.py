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
    "ghisaconus": "GHISACONUS",
    "lucas": "LUCAS"
}

dataset_labels = ["(a)", "(b)", "(c)", "(d)", "(e)"]

df_original['algorithm'] = pd.Categorical(df_original['algorithm'], categories=order, ordered=True)
df_original = df_original.sort_values('algorithm')
df_original = df_original[
    ((df_original["algorithm"].isin(order)) & (df_original["dataset"] == "lucas"))
    |
    ((df_original["algorithm"].isin(order)) & (df_original["target_size"].isin([5, 10, 15, 20, 25, 30])))
]
df_original.to_csv("temp_curated2_spa2/loc_combined_summary_sorted.csv", index=False)

metric = "time"
fig, axs = plt.subplots(2, 3, figsize=(14, 10))
axs = axs.flatten()

bar_width_linear = 2.0
bar_width_log = 0.3
offsets_linear = np.linspace(-bar_width_linear / 2, bar_width_linear / 2, num=len(order))
offsets_log = np.linspace(-bar_width_log / 2, bar_width_log / 2, num=len(order))

for idx, (dataset_key, dataset_name) in enumerate(DSS.items()):
    ax = axs[idx]
    dataset_df = df_original[df_original["dataset"] == dataset_key].copy()
    target_sizes = sorted(dataset_df["target_size"].unique())

    if dataset_key == "lucas":
        target_sizes = sorted(dataset_df["target_size"].unique())
        size_to_pos = {ts: i for i, ts in enumerate(target_sizes)}
        base_x = np.arange(len(target_sizes))
        ax.set_xticks(base_x)
        ax.set_xticklabels([str(ts) for ts in target_sizes])

    for i, alg_key in enumerate(order):
        alg_df = dataset_df[dataset_df["algorithm"] == alg_key]
        if alg_df.empty:
            continue
        y = np.array(alg_df[metric])

        if dataset_key == "lucas":
            # Align to base_x using consistent order
            x_vals = [size_to_pos[ts] for ts in alg_df["target_size"]]
            x_pos = np.array(x_vals) + offsets_log[i]
            bar_width = bar_width_log
        else:
            x = np.array(alg_df["target_size"])
            x_pos = x + offsets_linear[i]
            bar_width = bar_width_linear
            ax.set_xticks([5, 10, 15, 20, 25, 30])

        ax.bar(x_pos, y, width=bar_width, label=ALGS[alg_key], color=COLORS[alg_key])


    ax.set_xlabel(f"Target size\n{dataset_labels[idx]} {dataset_name}")
    ax.set_ylabel(r"Training time ($\log_{10}$ scale)")
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(LogLocator(base=10.0, numticks=10))
    ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs='auto', numticks=100))
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.grid(True, linestyle='--', linewidth=0.5, color='lightgray')

# Disable the unused 6th subplot
axs[-1].axis("off")

handles, labels = axs[-2].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=2, bbox_to_anchor=(0.23, 0.96))

fig.subplots_adjust(hspace=0.4)
fig.tight_layout(rect=[0, 0.03, 1, 0.92])

out_path = os.path.join(root, "classification", metric)
os.makedirs(out_path, exist_ok=True)
fig.savefig(os.path.join(out_path, "combined_time_bar.png"), dpi=300, bbox_inches='tight')
plt.show()
plt.close(fig)
