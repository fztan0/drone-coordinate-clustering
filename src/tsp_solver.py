import math_utilities
import numpy as np
import math

"""
returning:
    1. (Updated datapoints containing (x,y,k) k representing the clustering of the data point). 
    2. Array storing the launching pad coordinates of the drones (0-indexed). There should be k elements in array
"""
# def generate_k_means_clustering(k: int , points: np.ndarray, bounds: np.array) -> tuple[np.ndarray, np.array, np.ndarray]:
def generate_k_means_clustering(k: int , points: np.ndarray, bounds: np.array) -> tuple[list[tuple[float,float]], np.ndarray]:
    converge = False
    initial_launch_pads = math_utilities.random_seed(bounds, k)
    oldClustering = initial_launch_pads
    while not converge:
        #standard np would return a float for np.zeros but need to return a int 
        clustering_assignment = np.zeros(len(points), dtype=int)
        #creates k lists inside of one global list
        #iterates through all the points
        k_cluster_group = [ [] for  _ in range(k)]
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
            #if there is no cluster for one of the centroids keep original. this will allow for algorithm to converge
            if(cluster_array.size == 0):
                new_centroid[i] = initial_launch_pads[i]
            else:
                #stack it from 1d to 2d. 
                np.vstack(cluster_array)
                x,y = math_utilities.generate_centroid(cluster_array)
                new_centroid[i] = (x,y)
        if np.array_equal(oldClustering, new_centroid):
            converge = True
        else:
            oldClustering = new_centroid
    return k_cluster_group, new_centroid
