import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 22

def get_l0(file):
    df = pd.read_csv(file)
    return df['l0_s'].tolist()

files_cls = [
    "curated/v9_ips_v9_indian_pines_30.csv",
    "curated/v9_pu_v9_paviaU_30.csv",
    "curated/v9_salinas_v9_salinas_30.csv",
    "curated/v9_v9_ghisaconus_30.csv"
]
labels_cls = ["Indian Pines", "Pavia University", "Salinas", "GHISACONUS"]
y_cls = [get_l0(f) for f in files_cls]
x_cls = list(range(len(y_cls[0])))

file_lucas = r"D:\src\dicta2024_reg\lucas_results\v9_lucas_v9_lucas_512.csv"
y_lucas = [get_l0(file_lucas)]
x_lucas = list(range(len(y_lucas[0])))
labels_lucas = ["LUCAS"]

fig, axes = plt.subplots(1, 2, figsize=(18, 8))

for i in range(len(y_cls)):
    axes[0].plot(x_cls, y_cls[i], label=labels_cls[i])
axes[0].axhline(y=30, color='black', linestyle='--', linewidth=1, label="Target size")
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('$k_{active}$')
axes[0].set_ylim([0, 210])
axes[0].legend(
    bbox_to_anchor=(0.5, 1.3),
    loc='center',
    frameon=True,
    ncol=2,
    columnspacing=1.2,
    handletextpad=0.8
)
#axes[0].text(0.5, -0.35, "(a)", transform=axes[0].transAxes, ha='center', va='center')

#axes[0].set_title("Classification Datasets")

for i in range(len(y_lucas)):
    axes[1].plot(x_lucas, y_lucas[i], label=labels_lucas[i], color='purple')
axes[1].axhline(y=512, color='black', linestyle='--', linewidth=1, label="Target size")
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('$k_{active}$')
axes[1].set_ylim([0, 4300])
axes[1].legend(
    bbox_to_anchor=(0.35, 1.15),
    loc='center',
    frameon=True,
    ncol=2,
    columnspacing=0.5,
    handletextpad=0.8
)
#axes[1].text(0.5, -0.35, "(b)", transform=axes[1].transAxes, ha='center', va='center')

#axes[1].set_title("Regression Dataset (LUCAS)")

axes[0].text(0.5, -0.4, "(a)", transform=axes[0].transAxes, ha='center', va='center')
axes[1].text(0.5, -0.4, "(b)", transform=axes[1].transAxes, ha='center', va='center')

plt.subplots_adjust(top=0.65, bottom=0.3, left=0.1, wspace=0.3)
#plt.tight_layout()
plt.savefig("l0_b_post_combined.png", bbox_inches='tight', pad_inches=0.1)
plt.show()
