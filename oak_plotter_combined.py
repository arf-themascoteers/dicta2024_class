import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 18

ALGS = {
    "v0": "BS-Net-Classifier",
    "v9": "Proposed SABS",
    "all": "All Bands",
    "mcuve": "MCUVE",
    "spa": "SPA",
    "bsnet": "BS-Net-FC",
    "pcal": "PCAL",
}

DSS = {
    "indian_pines": "Indian Pines",
    "paviaU": "Pavia University",
    "salinas": "Salinas",
    "ghisaconus": "GHISACONUS"
}

COLORS = {
    "v0": "#1f77b4",
    "all": "#2ca02c",
    "mcuve": "#ff7f0e",
    "spa": "#00CED1",
    "bsnet": "#008000",
    "pcal": "#9467bd",
    "v9": "#d62728",
}

def sanitize_df(df):
    if "algorithm" not in df.columns:
        df['target_size'] = 0
        df['algorithm'] = 'all'
        df['time'] = 0
        df['selected_features'] = ''
    return df

def get_summaries_rec(d):
    files = os.listdir(d)
    paths = [os.path.join(d, f) for f in files if f.endswith("_summary.csv")]
    paths = [p for p in paths if not os.path.isdir(p)]

    children = [os.path.join(d, f) for f in files if os.path.isdir(os.path.join(d, f))]
    for child in children:
        cpaths = get_summaries_rec(child)
        paths = paths + cpaths

    return paths

def plot_combined_grid(source, exclude=None, include=None, out_dir="plots"):
    os.makedirs(out_dir, exist_ok=True)

    num_rows = 4
    num_cols = 3
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(18, 16), sharex=False)
    subplot_labels = ['(a)', '(b)', '(c)', '(d)']
    metric_names = ["OA", "AA", r"$\kappa$"]
    metric_keys = ["oa", "aa", "k"]
    handles_all = []
    labels_all = []

    for row_index, (dataset_key, dataset_label) in enumerate(DSS.items()):
        if exclude is None:
            exclude = []
        if isinstance(source, str):
            df = sanitize_df(pd.read_csv(source))
        else:
            df = [sanitize_df(pd.read_csv(loc)) for loc in source]
            df = [d for d in df if len(d) != 0]
            df = pd.concat(df, axis=0, ignore_index=True)

        df = df[df["dataset"] == dataset_key]
        if len(df) == 0:
            continue

        colors = list(COLORS.values())
        markers = ['s', 'P', 'D', '^', 'o', '*', '.', 's', 'P', 'D', '^', 'o', '*', '.']
        order = ["all", "pcal", "mcuve", "bsnet", "v0", "v1", "v2", "v3", "v35", "v4"]

        df["sort_order"] = df["algorithm"].apply(lambda x: order.index(x) if x in order else len(order) + ord(x[0]))
        df = df.sort_values("sort_order").drop(columns=["sort_order"])
        os.makedirs("refined",exist_ok=True)
        df.to_csv(f"refined/refined_{dataset_key}.csv",index=False)
        algorithms = df["algorithm"].unique()
        if include is None:
            include = algorithms
        include = [x for x in include if x not in exclude]
        if len(include) == 0:
            include = df["algorithm"].unique()
        else:
            df = df[df["algorithm"].isin(include)]

        min_lim = min(df["oa"].min(), df["aa"].min(), df["k"].min()) - 0.02
        max_lim = max(df["oa"].max(), df["aa"].max(), df["k"].max()) + 0.02

        algorithm_counter = 0
        for col_index, metric in enumerate(metric_keys):
            ax = axes[row_index][col_index]
            for algorithm in include:
                algorithm_label = ALGS.get(algorithm, algorithm)
                alg_df = df[df["algorithm"] == algorithm].sort_values(by='target_size')

                linestyle = "-"
                #marker = markers[algorithm_counter]
                color = COLORS[algorithm]

                if algorithm == "all":
                    m_val = alg_df.iloc[0][metric]
                    alg_df = pd.DataFrame({'target_size': range(5, 31), metric: [m_val] * 26})
                    linestyle = "--"
                    color = "#000000"
                    marker = None
                else:
                    algorithm_counter += 1

                l, = ax.plot(alg_df['target_size'], alg_df[metric],
                             label=algorithm_label,
                             color=color,
                             fillstyle='none', markersize=6, linewidth=2, linestyle=linestyle)

                if row_index == 0 and col_index == 0:
                    handles_all.append(l)
                    labels_all.append(algorithm_label)

            ax.set_ylim(min_lim, max_lim)
            ax.grid(True, linestyle='-', alpha=0.6)
            ax.set_xlabel("Target size")
            # if row_index == num_rows - 1:
            #     ax.set_xlabel("Target size")
            if col_index == 0:
                ax.set_ylabel(metric_names[col_index])
            if col_index == 1:
                ax.set_ylabel(metric_names[col_index])
                ax.text(0.5, -0.35, f"{subplot_labels[row_index]} {dataset_label}",
                        transform=ax.transAxes, ha='center', va='top')
            if col_index == 2:
                ax.set_ylabel(metric_names[col_index])
            #if col_index == 0:
                #ax.set_title(f"{subplot_labels[row_index]} {dataset_label}", loc='left')

    fig.legend(handles_all, labels_all, loc='upper center', ncol=7, bbox_to_anchor=(0.5, 1.02), frameon=True)
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig(os.path.join(out_dir, "oak_combined_grid.png"), bbox_inches='tight')
    plt.close(fig)

if __name__ == "__main__":
    plot_combined_grid(
        get_summaries_rec("curated"),
        include=["pcal", "mcuve", "spa", "bsnet", "v0", "v9", "all"]
    )
