import file_handler
import math_utilities
import time
import tsp_solver

def main():
    print("starting algorithm execution...")
    start_time = time.time()

    try:
        file_handler.compute_possible_solutions()

        end_time = time.time()
        total_runtime = end_time - start_time

        print(f"total runtime: {total_runtime:.1f} seconds")

        # also show in minutes and seconds if long runtime
        if total_runtime >= 60:
            minutes = int(total_runtime // 60)
            seconds = total_runtime % 60
            print(f"total runtime: {minutes} minutes and {seconds:.1f} seconds")

    except Exception as e:
        print(f"\n=== something screwed up somewhere ===")
        end_time = time.time()
        total_runtime = end_time - start_time

if __name__ == "__main__":
    main()
