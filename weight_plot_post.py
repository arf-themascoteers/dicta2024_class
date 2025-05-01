import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14


tab1 = pd.read_csv("v0_weights.csv", header=None).to_numpy()
tab2 = pd.read_csv("v9_weights.csv", header=None).to_numpy()

# print(tab1.shape)
# print(tab2.shape)
# exit(0)
epochs = np.arange(tab1.shape[0])
cv1 = np.std(tab1, axis=1) / np.mean(tab1, axis=1)
cv2 = np.std(tab2, axis=1) / np.mean(tab2, axis=1)
print(cv1[-1])
print(cv2[-1])

print(cv1)

mean1 = np.mean(tab1, axis=1)
mean2 = np.mean(tab2, axis=1)

fig, axes = plt.subplots(1, 2, figsize=(10, 5))

axes[0].plot(epochs, cv1, label="BS-Net-Classifier", color="#1f77b4")
axes[0].plot(epochs, cv2, label="Proposed SABS", color="#d62728")
#axes[0].set_title("CV of weights across the samples")
axes[0].set_xlabel("Epoch")
axes[0].set_ylabel("CV")
axes[0].legend(bbox_to_anchor=(0.26, 1.15), loc='center', ncol=1, frameon=True)
axes[0].text(0.5, -0.25, "(a)", transform=axes[0].transAxes, ha='center', va='center')

axes[1].plot(epochs, mean1, label="BS-Net-Classifier", color="#1f77b4")
axes[1].plot(epochs, mean2, label="Proposed SABS", color="#d62728")
#axes[1].set_title("Mean weight across the samples")
axes[1].set_xlabel("Epoch")
axes[1].set_ylabel("Mean weight")
axes[1].legend(bbox_to_anchor=(0.26, 1.15), loc='center', ncol=1, frameon=True)
axes[1].text(0.5, -0.25, "(b)", transform=axes[1].transAxes, ha='center', va='center')

plt.subplots_adjust(top=0.7, bottom=0.2)
plt.tight_layout()
plt.savefig("weight_plot_post.png")
plt.show()