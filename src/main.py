import file_handler
import math_utilities
import tsp_solver

def main():
    input_data = file_handler.load_file_coordinates(file_handler.get_file_name())
    bounds = math_utilities.calcDimension(input_data)
    clustering_assignment, new_centroid = tsp_solver.generate_k_means_clustering(3, input_data, bounds)
    print(clustering_assignment)
    print(new_centroid)

if __name__ == "__main__":
    main()