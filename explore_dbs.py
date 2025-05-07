import pandas as pd


df = pd.read_csv("data/indian_pines.csv")
unique_classes = sorted(df.iloc[:, -1].astype(int).unique().tolist())

print(unique_classes)
print(len(unique_classes))