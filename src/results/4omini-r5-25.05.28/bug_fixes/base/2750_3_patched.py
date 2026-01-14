import numpy as np
from sklearn.metrics import roc_auc_score

true_labels = np.array([1, 1, 1])
predicted_scores = np.array([0.9, 0.8, 0.4])

roc_auc = roc_auc_score(true_labels, predicted_scores)
# Ensure that true_labels contains at least two classes before calculating AUC
print(roc_auc)
