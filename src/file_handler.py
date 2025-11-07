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

def get_user_choice(output_file_name: str, selected_distances: list[list[int]], selected_routes: list[list[tuple[float,float]]], index_route: dict) -> tuple[list, int]:
    user_choice = input("Please select your choice 1 to 4:")
    full_path = output_file_name
    file_name = os.path.basename(full_path)
    choice = int(user_choice)
    if not user_choice:
        raise ValueError("Invalid choice")
    #this returns the routes of each clustering based on the specific choice 
    pointsOrder = tsp_solver.indiciesRoute(choice, index_route, selected_routes[choice-1])
    # list containing all the solutions; easy output
    output_files = []
    distance = selected_distances[choice-1]
    for i in range(choice):
        output_files.append(f"{file_name}_{i+1}_SOLUTION_{int(distance[i])}.txt")
    for i in range(len(output_files)):
       output_path = os.path.join(os.getcwd(), "output", output_files[i])
       os.makedirs(os.path.dirname(output_path), exist_ok = True)
       try:
            with open(output_path, 'w') as file:
                for node in pointsOrder[i]:
                    file.write(f"{node}\n") #node already is 1-indexed
                # remove last newline character to match output format
                file.truncate(file.tell() - len(os.linesep))
       except Exception as e:
            print(f"Error writing to file: {e}\nAborting.")
            exit()
    return output_files, choice

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
    #for each k will store k routes
    selected_routes = [ [] for  _ in range(4)]
    for k in range(4):
        clustering_assignment, new_centroids, iteration, route, cluster_distance, total_distance = tsp_solver.generate_best_k_clusterings(k+1, input_data, bounds)
        for i in range(k+1):
            #adding the chosen distances and routes in order to access them when the user makes the choice
            #note: it is in respect to each k
            selected_distances[k].append(int(cluster_distance[i]))
            extract_route = route[i]
            #this slices the first and last element in the array
            selected_routes[k].append(extract_route[1:-1])
        print(f"{k+1}) If you use {k+1} drone(s), the total route will be {int(total_distance)} meters")
        for i in range(k+1):
            x,y = new_centroids[i]
            print(f"    {roman_numerials[i]}. Landing Pad {i+1} should be at ({int(x)},{int(y)}), serving {len(clustering_assignment[i])} locations, route is {int(cluster_distance[i])} meters")

    # "please select your choice 1 to 4:"
    index_route = indiciesList(input_data)
    file_solutions, choice = get_user_choice(output_file_name, selected_distances, selected_routes, index_route)


    #use .join to seperate each file in the list by a comma
    separator = ", "
    print(f"Writing {separator.join(file_solutions)} to disk.")

def load_file_coordinates(file_path: str) -> numpy.ndarray:
    # numpy.loadtxt() should already handle majority of error flags for us
    file_coordinate_data = numpy.loadtxt(file_path, dtype = numpy.float64)

    return file_coordinate_data

#get the indicies of the data to make a list whose key is the actual coordinate and the value the respective indicies
def indiciesList(input_data: numpy.ndarray) -> dict:
    indiciesList = {}
    for i in range(len(input_data)):
        #convert coordinates to a tuple so the coordinates act as the key
        indiciesList[tuple(input_data[i])] = i + 1
    return indiciesList

#selected_routes[k].append(extract_route[1:-1])