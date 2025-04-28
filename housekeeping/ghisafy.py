import numpy as np
from sklearn.preprocessing import LabelEncoder
import pandas as pd

dataset_path = f"../data/ghisaconus.csv"
df = pd.read_csv(dataset_path)
le = LabelEncoder()
df.iloc[:, -1] = le.fit_transform(df.iloc[:, -1])
df.to_csv(dataset_path, index=False)