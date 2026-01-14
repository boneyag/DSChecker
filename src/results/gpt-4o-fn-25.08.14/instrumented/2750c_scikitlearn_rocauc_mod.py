import numpy as np
from sklearn.metrics import roc_auc_score

true_labels = np.array([1, 1, 1])
predicted_scores = np.array([0.9, 0.8, 0.4])

if len(np.unique(true_labels)) < 2:
    roc_auc = 0.0
else:
    roc_auc = roc_auc_score(true_labels, predicted_scores)
print(roc_auc)
import pandas
import numpy
if isinstance(true_labels, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(true_labels.info())
    print("***")
    print(true_labels.head(3))
    print("----***----")

elif isinstance(true_labels, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(true_labels.dtype)+" shape-"+str(true_labels.shape))
    slices = tuple(slice(0, 3) for _ in range(true_labels.ndim))
    print("***")
    print(true_labels[slices])
    print("----***----")

elif isinstance(true_labels, list):
    print("----***----")
    print("list")
    print("length-"+str(len(true_labels)))
    print("***")
    print(true_labels[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(true_labels).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")
