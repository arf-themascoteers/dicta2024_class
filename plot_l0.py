import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 15


def get_l0(file):
    df = pd.read_csv(file)
    return df['l0_s'].tolist()

y = []

y.append(get_l0("curated/v0_lambda_v0_lambda_indian_pines_30.csv"))
y.append(get_l0("curated/v0_lambda2_v0_lambda2_indian_pines_30.csv"))
y.append(get_l0("curated/v0_lambda4_v0_lambda4_indian_pines_30.csv"))
y.append(get_l0("curated/v0_lambda3_v0_lambda3_indian_pines_30.csv"))

labels = [
r"$\beta$ = 0.0001",
r"$\beta$ = 0.1",
r"$\beta$ = 0.5",
r"$\beta$ = 1"
]


x = list(range(len(y[0])))

for i in range(len(y)):
    plt.plot(x, y[i], label=labels[i])

plt.axhline(y=30, color='gray', linestyle='--', linewidth=1, label="Target size")
plt.xlabel('Epoch')
plt.ylabel('$k_{active}$')
plt.legend(fontsize=12, loc='center right')
plt.tight_layout()
plt.savefig("l0_b.png")
plt.show()
