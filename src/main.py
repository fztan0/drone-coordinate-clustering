import file_handler
import math_utilities
import tsp_solver

def main():
    file_handler.compute_possible_solutions()
    # input_data = file_handler.load_file_coordinates(file_handler.get_file_name())
    # bounds = math_utilities.calcDimension(input_data)

    # k = 3
    # # clustering_assignment, new_centroids, iteration = tsp_solver.generate_k_means_clustering(3, input_data, bounds)
    # # print(clustering_assignment)
    # # print(new_centroids)
    # # print(iteration)
    # #clustering_assignment, new_centroids, iteration = tsp_solver.generate_k_means_clustering(k, input_data, bounds)
    # #route = tsp_solver.generate_nearestNeighbor_route(clustering_assignment, new_centroids, k)
    # clustering_assignment, new_centroids, iteration, route, cluster_distance, total_distance = tsp_solver.generate_best_k_clusterings(k+1, input_data, bounds)
    # print(total_distance)
    # print(cluster_distance)


        
if __name__ == "__main__":
    main()

