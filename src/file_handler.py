import numpy

def get_file_name() -> str:
    input_file_name = input("Enter the name of file: ")

    if not input_file_name:
        raise ValueError("No file name provided")

    # input data files are placed in ./data within repo root
    input_file_name = "data/" + input_file_name

    return input_file_name

def load_file_coordinates(file_path: str) -> numpy.ndarray:
    # numpy.loadtxt() should already handle majority of error flags for us
    file_coordinate_data = numpy.loadtxt(file_path, dtype = numpy.float64)

    return file_coordinate_data