import pandas as pd
import os

folder = "../refined"
files = [f for f in os.listdir(folder) if f.endswith(".csv")]
df = pd.concat([pd.read_csv(os.path.join(folder, f)) for f in files], ignore_index=True)
dbs = ["pcal", "mcuve", "spa", "bsnet", "v0", "v9", "all"]
df = df[df["algorithm"].isin(dbs)]

ALGS = {
    "v0": "BS-Net-Classifier",
    "v9": "Proposed SABS",
    "all": "All Bands",
    "mcuve": "MCUVE",
    "spa": "SPA",
    "bsnet": "BS-Net-FC",
    "pcal": "PCAL",
}

order = ["all", "pcal", "mcuve","spa", "bsnet", "v0", "v9"]
df["sort_order"] = df["algorithm"].apply(lambda x: order.index(x) if x in order else len(order) + ord(x[0]))
df = df.sort_values("sort_order").drop(columns=["sort_order"])

results = []
for (dataset, algorithm), group in df[df["algorithm"] != "all"].groupby(["dataset", "algorithm"]):
    apf = df[(df["algorithm"] == "all") & (df["dataset"] == dataset)]
    threshold = apf.iloc[0]["oa"]

    surpass = group[group["oa"] > threshold]
    min_target_size_surpassing = surpass["target_size"].min() if not surpass.empty else "-"

    max_row = group.loc[group["oa"].idxmax()]
    max_oa = max_row["oa"]
    max_oa_ts = max_row["target_size"]

    diff_percent = ((max_oa - threshold) / threshold) * 100
    diff_percent = f"{'+' if diff_percent >= 0 else ''}{diff_percent:.2f}%"

    results.append((dataset, ALGS[algorithm], min_target_size_surpassing, round(max_oa,2), max_oa_ts, diff_percent))

result_df = pd.DataFrame(results, columns=[
    "dataset",
    "algorithm",
    "count_surpassing_apf",
    "max_oa",
    "target_size_at_max_oa",
    "oa_diff_percent"
])

result_df.to_csv("apf_comparison.csv", index=False)
