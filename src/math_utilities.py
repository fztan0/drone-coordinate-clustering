import numpy
import random

# Calculate Euclidean Distance between two points in n-dimensional space
# https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
"""
NOTE: parameters can be either a tuple or an numpy array since we are converting it to numpy inside the function
"""
def euclidean_distance(point_a: numpy.ndarray, point_b: numpy.ndarray) -> float:
    a = numpy.array(point_a)
    b = numpy.array(point_b)
    return numpy.linalg.norm(a - b)

# Pairwise distance matrix
def generate_distance_matrix(points: numpy.ndarray) -> numpy.ndarray:
    dimensions = len(points) # if 4 points, then create 4x4 matrix

    distance_matrix = numpy.zeros((dimensions, dimensions))

    for i in range(dimensions):
        for j in range(dimensions):
            distance_matrix[i, j] = euclidean_distance(points[i], points[j])

    return distance_matrix

def calcDimension(input_data: numpy.ndarray) -> numpy.array:
    maxX = minX = minY = maxY = 0
    #Numpy array slicing
    #colon means selecting all of the elements(rows) and the num represents the index i want to get
    x_values = input_data[:, 0]
    y_values = input_data[:, 1]
    maxX = numpy.max(x_values)
    maxY = numpy.max(y_values)
    minX = numpy.min(x_values)
    minY = numpy.min(y_values)
    bounds = numpy.array([minX,minY,maxX, maxY])
    return bounds

def random_seed(bounds: numpy.array, k) -> numpy.array:
    minX = int(bounds[0])
    minY = int(bounds[1])
    maxX = int(bounds[2])
    maxY = int(bounds[3])
    #for each k element store (x,y) pair
    initialPad = numpy.zeros((k,2))
    for i in range(k):
        randomX = random.randint(minX, maxX)
        randomY = random.randint(minY, maxY)
        initialPad[i] = (randomX, randomY)
    return initialPad

def generate_centroid(points: numpy.array) -> tuple[int,int]:
    #axis= 1 calculate mean across the rows
    mean_xValue = numpy.mean(points[:, 0])
    mean_yValue = numpy.mean(points[:, 1])
    return int(mean_xValue), int(mean_yValue)