import file_handler

def main():
    input_data = file_handler.load_file_coordinates(file_handler.get_file_name())

    for point in input_data:
        print(point)


if __name__ == "__main__":
    main()