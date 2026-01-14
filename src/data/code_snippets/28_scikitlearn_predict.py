from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

iris = datasets.load_iris()

X = iris.data[:, :2]
y = iris.target

knnc = KNeighborsClassifier()
n_neighbors = [3, 4, 5, 6, 7, 8, 9]
weights = ['uniform', 'distance']
algorithm = ['auto', 'ball_tree', 'kd_tree', 'brute']
leaf_size = [20, 30, 40, 50]
p = [1]

param_grid = dict(n_neighbors=n_neighbors, weights=weights, algorithm=algorithm, leaf_size=leaf_size, p=p)
clf = GridSearchCV(estimator=knnc, param_grid=param_grid, cv=5, n_jobs=1)
clf.fit(X, y)
print(f"best: {clf.best_score_}")

y_score = clf.best_estimator_.predict(X)
print(f"accuracy: {accuracy_score(y, y_score)}")
