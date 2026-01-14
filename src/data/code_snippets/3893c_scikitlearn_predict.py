from sklearn.dummy import DummyClassifier
import numpy as np

X = [[0], [0], [0], [0], [0]]
y = [1, 2, 1, 1, 2]

clf = DummyClassifier(strategy="most_frequent", random_state=0)
clf.fit(X, y)

predictions = clf.predict(X)
print(predictions == np.ones(len(y)))
