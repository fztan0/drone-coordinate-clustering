import file_handler
import math_utilities

def main():
    input_data = file_handler.load_file_coordinates(file_handler.get_file_name())

    distance_matrix = math_utilities.generate_distance_matrix(input_data)
    print(distance_matrix)

if __name__ == "__main__":
    main()