#!/usr/bin/env python
from __future__ import annotations
import json
import os
import numpy as np
import matplotlib.pyplot as plt

metrics_path = os.path.join(os.path.dirname(__file__), 'models', 'ml_metrics.json')
with open(metrics_path, 'r', encoding='utf-8') as f:
    metrics = json.load(f)

survival_knn = np.array(metrics['survival']['knn']['confusion'])
survival_nb = np.array(metrics['survival']['nb']['confusion'])
risk_knn = np.array(metrics['risk']['knn']['confusion'])
risk_nb = np.array(metrics['risk']['nb']['confusion'])

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

for ax, matrix, title, cmap in [
    (axs[0,0], survival_knn, 'Survival kNN Confusion Matrix', 'Blues'),
    (axs[0,1], survival_nb, 'Survival Naive Bayes Confusion Matrix', 'Blues'),
    (axs[1,0], risk_knn, 'Risk kNN Confusion Matrix', 'Oranges'),
    (axs[1,1], risk_nb, 'Risk Naive Bayes Confusion Matrix', 'Oranges'),
]:
    im = ax.imshow(matrix, cmap=cmap, interpolation='nearest')
    ax.set_title(title)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    ax.set_xticks(range(matrix.shape[1]))
    ax.set_yticks(range(matrix.shape[0]))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            ax.text(j, i, int(matrix[i,j]), ha='center', va='center', color='black')
    fig.colorbar(im, ax=ax)

fig.tight_layout(pad=3.0)
output_dir = os.path.join(os.path.dirname(__file__), 'results')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'confusion_matrices.png')
plt.savefig(output_path, dpi=200)
print(output_path)
