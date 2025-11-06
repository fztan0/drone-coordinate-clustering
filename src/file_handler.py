import numpy
import os
import math_utilities
import tsp_solver

def get_file_name() -> str:
    input_file_name = input("Enter the name of file: ")

    if not input_file_name:
        raise ValueError("No file name provided")

    # input data files are placed in ./data within repo root
    input_file_name = "data/" + input_file_name

    return input_file_name

# def get_user_choice(output_file_name: str) -> numpy:
#     user_choice = input("Please select your choice 1 to 4:")

#     choice = int(user_choice)
#     if not user_choice:
#         raise ValueError("Invalid choice")
    
#     # list containing all the solutions; easy output
#     output_files = []
#     for x in range(1, choice + 1):
#         output_files.append(f"{output_file_name}_{x}_SOLUTION_{sub_distance}.txt")

#     return output_files


def compute_possible_solutions() -> None:
    print(f"ComputePossibleSolutions")

    input_file_name = get_file_name()
    input_data = load_file_coordinates(input_file_name)
    bounds = math_utilities.calcDimension(input_data)
    # remove .txt extension before passing to other functions for append
    input_file_name = os.path.splitext(input_file_name)[0]
    output_file_name = f"{input_file_name}"

    n = len(input_data)
    print(f"There are {n} nodes: Solutions will be available by 7:04am")

    roman_numerials = ["i", "ii","iii", "iv"]
    selected_distances = [ [] for  _ in range(4)]
    selected_routes = [ [] for  _ in range(4)]
    for k in range(4):
        clustering_assignment, new_centroids, iteration, route, cluster_distance, total_distance = tsp_solver.generate_best_k_clusterings(k+1, input_data, bounds)
        for i in range(k+1):
            #adding the chosen distances and routes in order to access them when the user makes the choice
            selected_distances[k].append(cluster_distance[i])
            selected_routes[k].append(route[i])
        print(f"{k+1}) If you use {k+1} drone(s), the total route will be {total_distance} meters")
        for i in range(k+1):
            print(f"    {roman_numerials[i]}. Landing Pad {i+1} should be at {new_centroids[i]}, serving {len(clustering_assignment[i])} locations, route is {cluster_distance[i]} meters")

    # "please select your choice 1 to 4:"
    #file_solutions = get_user_choice(output_file_name)

    # might include line 51 to be apart of save_route_to_text_file 
    #print(f"Writing {file_solutions} to disk.")

def load_file_coordinates(file_path: str) -> numpy.ndarray:
    # numpy.loadtxt() should already handle majority of error flags for us
    file_coordinate_data = numpy.loadtxt(file_path, dtype = numpy.float64)

    return file_coordinate_data