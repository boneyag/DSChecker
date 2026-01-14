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

tpr = []
fpr = []
roc_auc = []

for i in range(n_classes):
    y_test_binarized = label_binarizer.transform(y_test)[:, i]
    fpr[i], tpr[i], thresh = roc_curve(y_test_binarized, y_score[:, i])
    roc_auc[i] = auc(fpr[i], tpr[i])
print(roc_auc)
