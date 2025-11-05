import numpy
import os

def get_file_name() -> str:
    input_file_name = input("Enter the name of file: ")

    if not input_file_name:
        raise ValueError("No file name provided")

    # input data files are placed in ./data within repo root
    input_file_name = "data/" + input_file_name

    return input_file_name

def get_user_choice(output_file_name: str) -> List[str]:
    user_choice = input("Please select your choice 1 to 4:")

    choice = int(user_choice)
    if not user_choice:
        raise ValueError("Invalid choice")
    
    # list containing all the solutions; easy output
    output_files = []
    for x in range(1, choice + 1):
        output_files.append(f"{output_file_name}_{x}_SOLUTION_{sub_distance}.txt")

    return output_files


def compute_possible_solutions() -> None:
    print(f"ComputePossibleSolutions")

    input_file_name = get_file_name()
    coordinates = load_file_coordinates(input_file_name)

    # remove .txt extension before passing to other functions for append
    input_file_name = os.path.splitext(input_file_name)[0]
    output_file_name = f"{input_file_name}"

    n = len(coordinates)
    print(f"There are {n} nodes: Solutions will be available by 7:04am")

    # distance_matrix = compute_distance_matrix(coordinates, n)

    for x in range(1,5):
        print(f"{x}) If you use {x} drone(s), the total route will be {total_distance} meters")
        for i in range(1, x + 1):
            print(f"    {i}. Landing Pad {i} should be at {location_coordinates(x)}, serving {n} locations, route is {individual_route_distance(x)} meters")

    # "please select your choice 1 to 4:"
    file_solutions = get_user_choice(output_file_name)

    # might include line 51 to be apart of save_route_to_text_file 
    print(f"Writing {file_solutions} to disk.")

def load_file_coordinates(file_path: str) -> numpy.ndarray:
    # numpy.loadtxt() should already handle majority of error flags for us
    file_coordinate_data = numpy.loadtxt(file_path, dtype = numpy.float64)

    return file_coordinate_data