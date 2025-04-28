import pandas as pd

dss = [
            "indian_pines",
            "paviaU",
            "salinas",
            "ghisaconus"
        ]

for ds in dss:
    dataset_path = f"../data/{ds}.csv"
    df = pd.read_csv(dataset_path)
    print(f"{ds}: {df.iloc[:,-1].nunique()}")