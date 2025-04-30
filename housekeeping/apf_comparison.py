import pandas as pd
import os

folder = "../refined"
files = [f for f in os.listdir(folder) if f.endswith(".csv")]
df = pd.concat([pd.read_csv(os.path.join(folder, f)) for f in files], ignore_index=True)



result_df = pd.DataFrame(columns=["dataset", "algorithm", "min_target_size_surpassing_apf"])
for (dataset, algorithm), group in df[df["algorithm"] != "all"].groupby(["dataset", "algorithm"]):
    apf = df[(df["algorithm"] == "all") & (df["dataset"] == dataset)]
    threshold = df.iloc[0]["oa"]
    print(dataset, threshold)
    surpass = group[group["oa"] > threshold]
    if not surpass.empty:
        min_ts = surpass["target_size"].min()
    else:
        min_ts = "-"
    result_df.loc[len(result_df)] = [dataset, algorithm, min_ts]

result_df = pd.DataFrame(results, columns=["dataset", "algorithm", "min_target_size_surpassing_apf"])
print(result_df)
