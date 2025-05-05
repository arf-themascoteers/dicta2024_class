import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 18

order = [
    "all",
    "pcal",
    "mcuve",
    "spa2",
    "bsnet",
    "v0",
    "v1",#V1
    "v2",#V2
    "v9",#V3
    "v9",#SABS
    "bsdr"#BSDR
]
ALGS = {
    "all": "All Bands",
    "pcal": "PCAL",
    "mcuve": "MCUVE",
    "spa2": "SPA",
    "bsnet": "BS_Net-FC",
    "v0": "BS-Net-Classifier",
    "v1": "V1: BS-Net-Classifier + FCNN",
    "v2": "V2: V1 + improved aggregation",
    "v6": "V3: V2 + absolute value activation",
    "v9": "Proposed SABS",
    "bsdr": "Proposed BSDR"
}

COLORS = {
    "all": "black",
    "pcal": "#008080",
    "mcuve": "orange",
    "spa2": "green",
    "bsnet": "#8B4513",
    "v0": "cyan",
    "v1": "blue",
    "v2": "orange",
    "v6": "green",
    "v9": "red",
    "bsdr": "purple",
}

DSS = {
    "indian_pines": "Indian Pines",
    # "paviaU": "Pavia University",
    # "salinas": "Salinas",
    # "ghisaconus": "GHISACONUS"
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

def plot_ablation(source, plot_type, exclude=None, include=None):
    loc = "plots2"
    os.makedirs(loc, exist_ok=True)
    dest = os.path.join(loc, f"{plot_type}.png")

    num_rows = len(DSS)
    num_cols = 3
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(18, 5), sharex=False)
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
        order = ["all", "pcal", "mcuve", "bsnet", "v0", "v1", "v2", "v3", "v35", "v4","v9","bsdr"]

        df["sort_order"] = df["algorithm"].apply(lambda x: order.index(x) if x in order else len(order) + ord(x[0]))
        df = df.sort_values("sort_order").drop(columns=["sort_order"])
        os.makedirs("refined",exist_ok=True)
        df.to_csv(f"refined/refined_{dataset_key}.csv",index=False)
        df = df[(df["algorithm"] == "all") | (df["target_size"].isin([5, 10, 15, 20, 25, 30]))]
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
            ax = axes[col_index]
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

            #ax.set_ylim(min_lim, max_lim)
            ax.set_xlim(5, 30)
            ax.grid(True, linestyle='-', alpha=0.6)
            ax.set_xlabel("Target size")
            # if row_index == num_rows - 1:
            #     ax.set_xlabel("Target size")
            if col_index == 0:
                ax.set_ylabel(metric_names[col_index])
            if col_index == 1:
                ax.set_ylabel(metric_names[col_index])
                #ax.text(0.5, -0.35, f"{subplot_labels[row_index]} {dataset_label}",
                        #transform=ax.transAxes, ha='center', va='top')
            if col_index == 2:
                ax.set_ylabel(metric_names[col_index])
            #if col_index == 0:
                #ax.set_title(f"{subplot_labels[row_index]} {dataset_label}", loc='left')

    fig.legend(handles_all, labels_all, loc='upper center',
               ncol=3,
               bbox_to_anchor=(0.39, 1.15), frameon=True)
    fig.tight_layout(rect=[0, 0, 1, 0.98])
    plt.savefig(dest, bbox_inches='tight')
    plt.close(fig)


def create_plot(plot_type="ablation_sabs_cl"):
    plot_ablation(
        get_summaries_rec("temp_curated2"),
        plot_type,
        include=[
            "all",
            "v0",
            "v1",
            "v2",
            "v6",
            "v9"
        ]
    )


if __name__ == "__main__":
    create_plot("ablation_sabs_cl")
