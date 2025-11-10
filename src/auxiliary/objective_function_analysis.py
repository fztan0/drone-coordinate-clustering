import sys
import time
import numpy as np

# add src directory to Python path to find modules
sys.path.append('src')
import math_utilities
import tsp_solver_benchmark_ver

def calculate_objective_function(file_path, k_values=[1, 2, 3, 4], iterations=1):
    input_data = np.loadtxt(file_path, dtype=np.float64)
    bounds = math_utilities.calcDimension(input_data)

    results = {
        'file_name': file_path.split('/')[-1],
        'n_points': len(input_data),
        'of_values': {}
    }

    for k in k_values:
        print(f"Calculating OF for K={k}...")
        start_time = time.time()

        # run core clustering
        clustering, centroids, _, _, _, total_distance = \
            tsp_solver_benchmark_ver.generate_best_k_clusterings(k, input_data, bounds, iterations)

        # calculate Objective Function (SSE)
        sse = 0.0
        for cluster_idx, cluster_points in enumerate(clustering):
            if len(cluster_points) > 0:  # Avoid empty clusters
                centroid = centroids[cluster_idx]

                # se_{K_i} = \sum_{j=1}^{m} \lVert t_{ij} - C_k \rVert^{2}
                for point in cluster_points:
                    squared_error = (point[0] - centroid[0])**2 + (point[1] - centroid[1])**2
                    sse += squared_error

        end_time = time.time()
        execution_time = end_time - start_time

        results['of_values'][k] = {
            'objective_function': sse,
            'total_distance': total_distance,
            'execution_time': execution_time
        }

        print(f"  K={k}: OF={int(sse)}, Distance={int(total_distance)}, Time={execution_time:.3f}s")

    return results

def create_table(results):
    table_output = """OF when K = 1, 2, 3, 4 for the following data sets:

Dataset Name          | K=1 OF Dist | K=2 OF Dist | K=3 OF Dist | K=4 OF Dist
----------------------|------------ |------------ |------------ |------------"""

    for result in results:
        file_name = result['file_name'].replace('.txt', '')
        n_points = result['n_points']

        row_start = f"\n{file_name:18} ({n_points:4d}) |"

        k_values = []
        for k in [1, 2, 3, 4]:
            if k in result['of_values']:
                of_val = result['of_values'][k]['objective_function']
                distance = int(result['of_values'][k]['total_distance'])
                k_values.append(f"{int(of_val):8d} {distance:4d}")

        row = row_start + " |".join([f"{val:>12}" for val in k_values]) + " |"
        table_output += row

    return table_output

def main():
    calibration_datasets = [
        "data/Almond9832.txt",
        "data/pecan1212.txt",
        "data/Walnut2621.txt"
    ]

    print("Calculating OF for K = 1, 2, 3, 4")
    print()

    all_results = []

    for dataset_path in calibration_datasets:
        print(f"\nProcessing: {dataset_path}")
        print("-" * 50)

        try:
            result = calculate_objective_function(dataset_path)
            all_results.append(result)
        except Exception as e:
            print(f"Error processing {dataset_path}: {e}")
            continue

    if all_results:
        table = create_table(all_results)
        print("\n" + table)


if __name__ == "__main__":
    main()