import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 22


def get_l0(file):
    df = pd.read_csv(file)
    return df['l0_s'].tolist()

y = []


y.append(get_l0("curated/v9_ips_v9_indian_pines_30.csv"))
y.append(get_l0("curated/v9_pu_v9_paviaU_30.csv"))
y.append(get_l0("curated/v9_salinas_v9_salinas_30.csv"))
y.append(get_l0("curated/v9_v9_ghisaconus_30.csv"))
# y.append(get_l0("results/v0_lambda4_v0_lambda4_indian_pines_30.csv"))
# y.append(get_l0("results/v0_lambda3_v0_lambda3_indian_pines_30.csv"))

labels = [
"Indian Pines",
"Pavia University",
"Salinas",
"GHISACONUS",

# r"$\beta$ = 0.1",
# r"$\beta$ = 0.5",
# r"$\beta$ = 1"
]


x = list(range(len(y[0])))

plt.figure(figsize=(10,6))

for i in range(len(y)):
    plt.plot(x, y[i], label=labels[i])

plt.axhline(y=30, color='black', linestyle='--', linewidth=1, label="Target maximum size")
plt.xlabel('Epoch')
plt.ylabel('$k_{active}$')
plt.ylim([0,210])
legend = plt.legend(    bbox_to_anchor=(0.43, 1.3),loc='center',frameon=True,ncol=2,)
plt.tight_layout()
plt.savefig("l0_b_post.png", bbox_inches='tight', pad_inches=0.1)

plt.show()

