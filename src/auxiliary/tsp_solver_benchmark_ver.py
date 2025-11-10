import math_utilities
import numpy as np
import math


def generate_k_means_clustering(k: int , points: np.ndarray, bounds: np.array) -> tuple[list[list[tuple[float,float]]], np.ndarray, int]:
    converge = False
    initial_launch_pads = math_utilities.random_seed(bounds, k)
    oldClustering = initial_launch_pads
    iteration = 0
    while not converge:
        clustering_assignment = np.zeros(len(points), dtype=int)
        k_cluster_group = [ [] for  _ in range(k)]
        for j in range(len(points)):
            closestDrone = -1
            shortestDistance = math.inf
            for i in range(len(oldClustering)):
                calculateDistance = math_utilities.euclidean_distance(oldClustering[i], points[j])
                if shortestDistance > calculateDistance:
                    shortestDistance = calculateDistance
                    closestDrone = i
            clustering_assignment[j] = closestDrone
        clustering_assignment.astype(int)
        for i in range(len(points)):
            clusteringAssignment = clustering_assignment[i]
            location = points[i]
            k_cluster_group[clusteringAssignment].append(tuple(location))
        new_centroid = np.zeros((k,2))
        for i in range(k):
            cluster_array = np.array(k_cluster_group[i])
            if(cluster_array.size == 0):
                new_centroid[i] = oldClustering[i]
            else:
                cluster_change = np.vstack(cluster_array)
                x,y = math_utilities.generate_centroid(cluster_change)
                new_centroid[i] = (x,y)
        if np.allclose(oldClustering, new_centroid, atol = 1e-03):
            converge = True
        else:
            oldClustering = new_centroid.copy()
            iteration = iteration + 1
    return k_cluster_group, new_centroid, iteration


def compute_route_distance(route: list[list[tuple[float,float]]], k:int) -> np.array:
  total_cluster_distance = []
  for k_value in range(k):
    total_distance = 0.0
    individualRoute = route[k_value]
    for i in range(len(individualRoute) - 1):
      from_node = individualRoute[i]
      to_node = individualRoute[i + 1]
      total_distance += math_utilities.euclidean_distance(from_node,to_node)
    total_cluster_distance.append(total_distance)
  return total_cluster_distance

def generate_nearestNeighbor_route(k_cluster_array: list[list[tuple[float,float]]], startingCentroid: np.ndarray, k: int) -> list[list[tuple[float,float]]]:
  routes = [ [] for  _ in range(k)]
  for k_value in range(k):
    remaining_locations = []
    routes[k_value] = []
    cluster = k_cluster_array[k_value]
    starting_pad = tuple(startingCentroid[k_value])
    remaining_locations = list(cluster)
    remaining_locations.append(starting_pad)
    routes[k_value].append(starting_pad)
    shortestLocation = starting_pad
    while len(remaining_locations) > 1:
      shortestNodeDist = math.inf
      selectedLocation = shortestLocation
      remaining_locations.remove(shortestLocation)
      for x in remaining_locations:
        euclidean_distance = 0.0
        euclidean_distance = math_utilities.euclidean_distance(selectedLocation,x)
        if(shortestNodeDist > euclidean_distance):
          shortestNodeDist = euclidean_distance
          shortestLocation = x
      location = shortestLocation
      routes[k_value].append(location)
    routes[k_value].append(starting_pad)
  return routes

def generate_best_k_clusterings(k: int , points: np.ndarray, bounds: np.array, iteration_count: int = 1) -> tuple[list[list[tuple[float,float]]], np.ndarray, int, list[list[tuple[float,float]]], np.array, int]:
  bestDistance = math.inf
  bestRoute = []
  clustering = []
  route_distance = []
  bestIteration = 0
  centroid = []
  for i in range(iteration_count):
    clustering_assignment, new_centroids, iteration = generate_k_means_clustering(k, points, bounds)
    route = generate_nearestNeighbor_route(clustering_assignment, new_centroids, k)
    distance_each_clustering = compute_route_distance(route, k)
    round_distance = 0
    round_distance = np.ceil(distance_each_clustering)
    total_distance = np.sum(round_distance)
    if(bestDistance > total_distance):
      clustering = clustering_assignment
      centroid = new_centroids
      bestIteration = iteration
      bestRoute = route
      route_distance = round_distance
      bestDistance = total_distance
  return clustering, centroid, bestIteration, bestRoute, route_distance, bestDistance

def indiciesRoute(k: int, route: dict, selected_route : list[list[tuple[float,float]]]) -> list[list[int]]:
  pointsOrder = [ [] for  _ in range(k)]
  for i in range(k):
    for coordinate in selected_route[i]:
      if coordinate in route:
        pointsOrder[i].append(route[coordinate])
  return pointsOrder