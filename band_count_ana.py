import pandas as pd


# df = pd.read_csv("temp_curated2/loc_combined_summary.csv")
#
# df = df[df["algorithm"] == "bsdr"]
#
# for _, row in df.iterrows():
#     t = row['target_size']
#     sf = len(row['selected_features'].split("|"))
#     if t!= sf:
#         print(t,row['dataset'],sf)

# df = pd.read_csv("epoch_tracker/epochs2.csv")
# for _, row in df.iterrows():
#     t = 20
#     sb = row['selected_bands'].split("|")
#     sb = list(dict.fromkeys(sb))
#     sf = len(sb)
#     if t!= sf:
#         print(row['epoch'])

df = pd.read_csv("epoch_tracker/epochs2.csv")
df = df[df["epoch"] == 40]
t = 20
sb =  df['selected_bands'].iloc[0].split("|")
print(sb)
sb = list(dict.fromkeys(sb))
print(sb)