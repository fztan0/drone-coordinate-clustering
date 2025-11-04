import numpy

# Calculate Euclidean Distance between two points in n-dimensional space
# https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
def euclidean_distance(point_a: numpy.ndarray, point_b: numpy.ndarray) -> float:
    return numpy.linalg.norm(point_a - point_b)

# Pairwise distance matrix
def generate_distance_matrix(points: numpy.ndarray) -> numpy.ndarray:
    dimensions = len(points) # if 4 points, then create 4x4 matrix

    distance_matrix = numpy.zeros((dimensions, dimensions))

    for i in range(dimensions):
        for j in range(dimensions):
            distance_matrix[i, j] = euclidean_distance(points[i], points[j])

    return distance_matrix