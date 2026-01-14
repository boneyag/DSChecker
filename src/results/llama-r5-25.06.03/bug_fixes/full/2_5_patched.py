import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import euclidean_distances

data = np.array(
    [
        [-0.538, -0.478, -0.374, -0.338, -0.346, 0.230, 0.246, 0.366, 0.362, 0.342],
        [0.471, 0.559, 0.411, 0.507, 0.631, 0.579, 0.467, 0.475, 0.543, 0.659],
    ]
).T


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_list(self):
        return [self.x, self.y]

    def __repr__(self):
        return (
            str(self.__class__.__name__) + "(" + str(self.x) + ", " + str(self.y) + ")"
        )


points = [Point(*xy) for xy in data]


def get_point_distance(p1, p2):
    """Returns euclidea distance"""
    return euclidean_distances([p1.to_list()], [p2.to_list()])


clustering = DBSCAN(metric=get_point_distance).fit(
    np.array([[point] for point in points])
)
