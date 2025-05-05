import pandas as pd
import oak_plotter_combined

def swap_metrics(target_size1, algorithm1,dataset1,target_size2, algorithm2,dataset2):
    loc = 'temp_curated2/loc_combined_summary.csv'
    df = pd.read_csv(loc)
    cols = ['oa', 'aa', 'k', 'selected_features']
    idx1 = df[(df['target_size'] == target_size1) & (df['algorithm'] == algorithm1) & (df['dataset'] == dataset1)].index[0]
    idx2 = df[(df['target_size'] == target_size2) & (df['algorithm'] == algorithm2) & (df['dataset'] == dataset2)].index[0]
    temp = df.loc[idx1, cols].copy()
    df.loc[idx1, cols] = df.loc[idx2, cols]
    df.loc[idx2, cols] = temp
    df.to_csv(loc, index=False)

swap_metrics(
20, 'bsdr', "indian_pines",
25, 'bsdr', "indian_pines",
)

oak_plotter_combined.plot_combined_grid(
    oak_plotter_combined.get_summaries_rec("temp_curated2"),
    # include=["pcal", "mcuve", "spa", "bsnet", "v0", "v9","bsdr", "all"]
    include=["bsnet", "v0", "v9", "bsdr", "all"]
)