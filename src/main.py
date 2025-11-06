import file_handler
import math_utilities
import tsp_solver

def main():
   file_handler.compute_possible_solutions()

        
if __name__ == "__main__":
    main()


 #input_data = file_handler.load_file_coordinates(file_handler.get_file_name())
    #ounds = math_utilities.calcDimension(input_data)


    #k = 3
    #clustering_assignment, new_centroids, iteration = tsp_solver.generate_k_means_clustering(3, input_data, bounds)
    #print(clustering_assignment)
    #print(new_centroids)
    #print(iteration)
    #clustering_assignment, new_centroids, iteration = tsp_solver.generate_k_means_clustering(k, input_data, bounds)
    #route = tsp_solver.generate_nearestNeighbor_route(clustering_assignment, new_centroids, k)
    #total_distance = tsp_solver.compute_route_distance(route, k)
    #print(total_distance)