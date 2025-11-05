import math_utilities
import numpy as np
import math

"""
returning:
    1. (Updated datapoints containing (x,y,k) k representing the clustering of the data point). 
    2. Array storing the launching pad coordinates of the drones (0-indexed). There should be k elements in array
    3. Array containing array of drone's total distance (There should be k elements in array)
"""
# def generate_k_means_clustering(k: int , points: np.ndarray, bounds: np.array) -> tuple[np.ndarray, np.array, np.ndarray]:
def generate_k_means_clustering(k: int , points: np.ndarray, bounds: np.array) -> tuple[list[tuple[float,float]], np.ndarray]:
    initial_launch_pads = math_utilities.random_seed(bounds, k)
    #standard np would return a float for np.zeros but need to return a int 
    clustering_assignment = np.zeros(len(points), dtype=int)
    #creates k lists inside of one global list
    k_cluster_group = [ [] for  _ in range(k)]
    #iterates through all the points
    for j in range(len(points)):
        closestDrone = -1
        shortestDistance = math.inf
        #iterates through all of the launch pad locations
        for i in range(len(initial_launch_pads)):
            #tries to find the best launch pad to return the shortest distance between the point
            calculateDistance = math_utilities.euclidean_distance(initial_launch_pads[i], points[j])
            if shortestDistance > calculateDistance:
                shortestDistance = calculateDistance
                closestDrone = i 
        #keeps track of the respective clustering for each point
        clustering_assignment[j] = closestDrone
    clustering_assignment.astype(int)
    for i in range(len(points)):
        clusteringAssignment = clustering_assignment[i]
        location = points[i]
        k_cluster_group[clusteringAssignment].append(location)
    #recalculating the new centroid
    new_centroid = np.zeros((k,2))
    for i in range(k):
        cluster_array = np.array(k_cluster_group[i])
        #if there is no cluster for one of the centroids create a random location and add it
        if(cluster_array.size == 0):
            initial_launch_pads = math_utilities.random_seed(bounds, k)
            #only extracts one random location
            new_centroid[i] = initial_launch_pads[0]
        else:
            #stack it from 1d to 2d. 
            np.vstack(cluster_array)
            x,y = math_utilities.generate_centroid(cluster_array)
            new_centroid[i] = (x,y)
    return k_cluster_group, new_centroid
