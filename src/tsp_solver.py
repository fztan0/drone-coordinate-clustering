import math_utilities
import numpy as np
import math

"""
returning:
    1. Returns a list of arrays. Each index represents a k (0- (k-1)) which stores array of locations to visit
    2. Converged drone launch pads that are strategically placed to have high clustering
    3. Tracks the number of iterations it took to converge
    NOTE: Clustering 
"""
# def generate_k_means_clustering(k: int , points: np.ndarray, bounds: np.array) -> tuple[np.ndarray, np.array, np.ndarray]:
def generate_k_means_clustering(k: int , points: np.ndarray, bounds: np.array) -> tuple[list[list[tuple[float,float]]], np.ndarray, int]:
    converge = False
    initial_launch_pads = math_utilities.random_seed(bounds, k)
    oldClustering = initial_launch_pads
    iteration = 0
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
            for i in range(len(oldClustering)):
                #tries to find the best launch pad to return the shortest distance between the point
                calculateDistance = math_utilities.euclidean_distance(oldClustering[i], points[j])
                if shortestDistance > calculateDistance:
                    shortestDistance = calculateDistance
                    closestDrone = i 
            #keeps track of the respective clustering for each point
            clustering_assignment[j] = closestDrone
        clustering_assignment.astype(int)
        #assigns the points to their respective clustering group
        for i in range(len(points)):
            clusteringAssignment = clustering_assignment[i]
            location = points[i]
            #need to convert each point to a tuple to allow in a later function to be able to remove points from a list (wont work if its a numpy array)
            k_cluster_group[clusteringAssignment].append(tuple(location))
        #recalculating the new centroid
        new_centroid = np.zeros((k,2))
        for i in range(k):
            cluster_array = np.array(k_cluster_group[i])
            #if there is no cluster for one of the centroids keep original. this will allow for algorithm to converge
            if(cluster_array.size == 0):
                new_centroid[i] = oldClustering[i]
            else:
                #stack it from 1d to 2d. 
                cluster_change = np.vstack(cluster_array)
                x,y = math_utilities.generate_centroid(cluster_change)
                new_centroid[i] = (x,y)
        #does a tolerance to ensure that the difference is within 1e-03 to be able to converge
        if np.allclose(oldClustering, new_centroid, atol = 1e-03):
            converge = True
        else:
            #insures you are getting an exact copy in numpy
            oldClustering = new_centroid.copy()
            iteration = iteration + 1
    return k_cluster_group, new_centroid, iteration

"""
Parameter: Route - stores all of the points with respect to their cluster (also includes the centroid)
Returns: This return returns an array (k size) that stores the total distance of each of the routes
"""
def compute_route_distance(route: list[list[tuple[float,float]]], k:int) -> np.array:
  total_cluster_distance = []
  #loop over all of the clusters and calculate the total distance for each
  for k_value in range(k):
    total_distance = 0.0
    individualRoute = route[k_value]
    for i in range(len(individualRoute) - 1):
      from_node = individualRoute[i]
      to_node = individualRoute[i + 1]
      total_distance += math_utilities.euclidean_distance(from_node,to_node)
    total_cluster_distance.append(total_distance)
  return total_cluster_distance

#note: routes wont append the launch pad at the beginning & the end
#n represents the size of the 
"""
Returns routes starting from the launch pad to all of its respective cluster than back to the launch pad. Uses nearest neighbor implementation
"""
def generate_nearestNeighbor_route(k_cluster_array: list[list[tuple[float,float]]], startingCentroid: np.ndarray, k: int) -> list[list[tuple[float,float]]]:
  routes = [ [] for  _ in range(k)]
  #get the route for all of the clusters and store it in route
  for k_value in range(k):
    #initialize the dictionary
    remaining_locations = []
    routes[k_value] = []
    cluster = k_cluster_array[k_value]
    #must convert to a tuple in order to be able to remove it from a list
    starting_pad = tuple(startingCentroid[k_value])
    #remaining_location stores all of the points that the cluster needs to visit in a list
    remaining_locations = list(cluster)
    #append the centroid since that is the starting point
    remaining_locations.append(starting_pad)
    routes[k_value].append(starting_pad)
    shortestLocation = starting_pad
    while len(remaining_locations) > 1:
      shortestNodeDist = math.inf
      selectedLocation = shortestLocation
      #remove value
      remaining_locations.remove(shortestLocation)
      #iterates through remaining locations to find the shortest distance
      for x in remaining_locations:
        if(shortestNodeDist > math_utilities.euclidean_distance(selectedLocation,x)):
          shortestNodeDist = math_utilities.euclidean_distance(selectedLocation,x)
          shortestLocation = x
      location = shortestLocation
      routes[k_value].append(location)
    #add the centroid at the end in order to do distance calculation
    routes[k_value].append(starting_pad)
  return routes

#run k_mean_clustering 10 times to get shortest total distance
def generate_best_k_clusterings(k: int , points: np.ndarray, bounds: np.array) -> tuple[list[list[tuple[float,float]]], np.ndarray, int, list[list[tuple[float,float]]], np.array, int]:
  bestDistance = math.inf
  bestRoute = []
  clustering = []
  route_distance = []
  bestIteration = 0
  centroid = []
  for i in range(10):
    clustering_assignment, new_centroids, iteration = generate_k_means_clustering(k, points, bounds)
    route = generate_nearestNeighbor_route(clustering_assignment, new_centroids, k)
    distance_each_clustering = compute_route_distance(route, k)
    #calculates the total distance 
    total_distance = np.sum(distance_each_clustering)
    if(bestDistance > total_distance):
      clustering = clustering_assignment
      centroid = new_centroids
      bestIteration = iteration
      bestRoute = route
      route_distance = distance_each_clustering
      bestDistance = total_distance
  return clustering, centroid, bestIteration, bestRoute, route_distance, total_distance  