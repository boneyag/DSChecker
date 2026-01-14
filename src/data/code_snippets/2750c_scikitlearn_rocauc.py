import numpy as np
from sklearn.metrics import roc_auc_score

true_labels = np.array([1, 1, 1])
predicted_scores = np.array([0.9, 0.8, 0.4])

if len(np.unique(true_labels)) < 2:
    roc_auc = 0.0
else:
    roc_auc = roc_auc_score(true_labels, predicted_scores)
print(roc_auc)
