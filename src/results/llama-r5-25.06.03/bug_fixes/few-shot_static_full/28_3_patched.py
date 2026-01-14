from sklearn import datasets
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier

iris = datasets.load_iris()

X = iris.data[:, :2]
y = iris.target

knnc = KNeighborsClassifier()
n_neighbors = [3, 4, 5, 6, 7, 8, 9]
weights = ["uniform", "distance"]
algorithm = ["auto", "ball_tree", "kd_tree", "brute"]
leaf_size = [20, 30, 40, 50]
p = [1]

param_grid = dict(
    n_neighbors=n_neighbors,
    weights=weights,
    algorithm=algorithm,
    leaf_size=leaf_size,
    p=p,
)
clf = GridSearchCV(estimator=knnc, param_grid=param_grid, cv=5, n_jobs=1)
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
estimator = clf.fit(X_train, y_train)
print(f"best: {clf.best_score_}")

y_score = estimator.best_estimator_.predict(X_test)
print(f"accuracy: {accuracy_score(y_test, y_score)}")
