import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import LabelBinarizer

iris = load_iris()
target_names = iris.target_names

X, y = iris.data, iris.target
y = iris.target_names[y]
n_samples, n_features = X.shape
n_classes = len(np.unique(y))

(X_train, X_test, y_train, y_test) = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)

label_binarizer = LabelBinarizer().fit(y_train)
y_onehot_test = label_binarizer.transform(y_test)

classifier = LogisticRegression(max_iter=200)
y_score = classifier.fit(X_train, y_train).predict_proba(X_test)

tpr = dict()
fpr = dict()
roc_auc = dict()

for i in range(n_classes):
    fpr[i], tpr[i], _ = roc_curve(y_onehot_test[:, i], y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])
print(roc_auc)
import pandas
import numpy
if isinstance(y_test, pandas.core.frame.DataFrame):
    print("----***----")
    print("pandas.core.frame.DataFrame")
    print(y_test.info())
    print("***")
    print(y_test.head(3))
    print("----***----")

elif isinstance(y_test, numpy.ndarray):
    print("----***----")
    print("numpy.ndarray")
    print("dtype-"+str(y_test.dtype)+" shape-"+str(y_test.shape))
    slices = tuple(slice(0, 3) for _ in range(y_test.ndim))
    print("***")
    print(y_test[slices])
    print("----***----")

elif isinstance(y_test, list):
    print("----***----")
    print("list")
    print("length-"+str(len(y_test)))
    print("***")
    print(y_test[:3])
    print("----***----")

else:
    print("----***----")
    print(f"Type: {type(y_test).__name__}")
    print("***")
    print("Unsuported type for instrumentation")
    print("----***----")
