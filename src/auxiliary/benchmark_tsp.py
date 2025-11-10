import math_utilities
import numpy as np
import os
import time
import tsp_solver_benchmark_ver
from typing import List, Dict, Tuple

def load_file_coordinates(file_path: str) -> np.ndarray:
    return np.loadtxt(file_path, dtype=np.float64)

def run_benchmark_test(file_path: str, iteration_counts: List[int], k_values: List[int] = [1, 2, 3, 4]) -> Dict:
    print(f"\n{'='*60}")
    print(f"Testing file: {os.path.basename(file_path)}")
    print(f"{'='*60}")

    # load data
    input_data = load_file_coordinates(file_path)
    bounds = math_utilities.calcDimension(input_data)
    n_points = len(input_data)

    print(f"Number of points: {n_points}")



    results = {
        'file_name': os.path.basename(file_path),
        'n_points': n_points,
        'data': {}
    }

    for iteration_count in iteration_counts:
        print(f"\n--- Testing with {iteration_count} iteration(s) ---")
        iteration_start_time = time.time()

        file_results = {
            'iteration_count': iteration_count,
            'k_results': {},
            'total_time': 0,
            'best_overall_distance': float('inf')
        }

        for k in k_values:
            print(f"  Testing k={k}...")
            k_start_time = time.time()

            # run TSP solver
            clustering, centroids, iterations, route, cluster_distances, total_distance = \
                tsp_solver_benchmark_ver.generate_best_k_clusterings(k, input_data, bounds, iteration_count)

            k_end_time = time.time()
            k_time = k_end_time - k_start_time

            # store results for this k value
            file_results['k_results'][k] = {
                'total_distance': float(total_distance),
                'cluster_distances': cluster_distances.tolist(),
                'convergence_iterations': int(iterations),
                'execution_time': k_time,
                'n_clusters': len(clustering)
            }

            # update best overall distance
            if total_distance < file_results['best_overall_distance']:
                file_results['best_overall_distance'] = float(total_distance)

            print(f"    Total distance: {int(total_distance)}")
            print(f"    Convergence iterations: {iterations}")
            print(f"    Execution time: {k_time}s")

        iteration_end_time = time.time()
        file_results['total_time'] = iteration_end_time - iteration_start_time

        print(f"  Total time for {iteration_count} iterations: {file_results['total_time']}s")

        results['data'][iteration_count] = file_results

    return results

def analyze_results(all_results: List[Dict]) -> None:
    print(f"\n{'='*80}")
    print("COMPREHENSIVE BENCHMARK")
    print(f"{'='*80}")

    iteration_counts = [1, 2, 3, 4, 5, 6, 7, 10]

    print("\n1. DISTANCE COMPARISON BY ITERATION COUNT")
    print("-" * 50)

    for result in all_results:
        print(f"\nFile: {result['file_name']} ({result['n_points']} points)")
        print(f"{'Iterations':<12} {'Best Distance':<15} {'Time (s)':<12} {'Improvement':<15}")
        print("-" * 60)

        baseline_distance = None
        baseline_time = None

        for iteration_count in iteration_counts:
            if iteration_count in result['data']:
                data = result['data'][iteration_count]
                distance = int(data['best_overall_distance'])
                time_taken = data['total_time']

                if baseline_distance is None:
                    baseline_distance = distance
                    baseline_time = time_taken
                    improvement = "baseline"
                else:
                    improvement_pct = ((baseline_distance - distance) / baseline_distance) * 100
                    improvement = f"{improvement_pct:+.1f}%"

                print(f"{iteration_count:<12} {distance:<15} {time_taken:<12.3f} {improvement:<15}")

    print("\n\n2. EXECUTION TIME ANALYSIS")
    print("-" * 50)

    for result in all_results:
        print(f"\nFile: {result['file_name']}")
        print(f"{'Iterations':<12} {'Total Time (s)':<15} {'Time per k (s)':<15}")
        print("-" * 45)

        for iteration_count in iteration_counts:
            if iteration_count in result['data']:
                data = result['data'][iteration_count]
                total_time = data['total_time']
                avg_time_per_k = total_time / 4  # assuming 4 k values, COME BACK TO THIS LATER
                print(f"{iteration_count:<12} {total_time:<15.3f} {avg_time_per_k:<15.3f}")

    print("\n\n3. DETAILED CLUSTER ANALYSIS (k = 4 only)")
    print("-" * 50)

    for result in all_results:
        print(f"\nFile: {result['file_name']}")
        print(f"{'Iterations':<12} {'k=4 Distance':<15} {'Cluster Breakdown':<25}")
        print("-" * 55)

        for iteration_count in iteration_counts:
            if iteration_count in result['data']:
                data = result['data'][iteration_count]
                k4_distance = int(data['k_results'][4]['total_distance'])
                cluster_distances = [int(d) for d in data['k_results'][4]['cluster_distances']]
                breakdown = f"[{', '.join(map(str, cluster_distances))}]"
                print(f"{iteration_count:<12} {k4_distance:<15} {breakdown:<25}")

    print("\n\n4. CONVERGENCE ANALYSIS")
    print("-" * 50)

    for result in all_results:
        print(f"\nFile: {result['file_name']}")
        print(f"{'Iterations':<12} {'Avg Conv. Iter.':<18} {'Max Conv. Iter.':<18}")
        print("-" * 50)

        for iteration_count in iteration_counts:
            if iteration_count in result['data']:
                data = result['data'][iteration_count]
                conv_iterations = [data['k_results'][k]['convergence_iterations'] for k in [1, 2, 3, 4]]
                avg_conv = sum(conv_iterations) / len(conv_iterations)
                max_conv = max(conv_iterations)
                print(f"{iteration_count:<12} {avg_conv:<18.1f} {max_conv:<18}")


def main():
    # config
    data_dir = "data"
    iteration_counts = [1, 2, 3, 4, 5, 6, 7, 10]
    k_values = [1, 2, 3, 4]

    data_files = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            data_files.append(os.path.join(data_dir, filename))

    data_files.sort()

    print("TSP SOLVER BENCHMARKING")
    print("=" * 60)
    print(f"Files to test: {len(data_files)}")
    print(f"Iteration counts: {iteration_counts}")
    print(f"K values: {k_values}")









    all_results = []
    for file_path in data_files:
        try:
            result = run_benchmark_test(file_path, iteration_counts, k_values)
            all_results.append(result)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue

    if all_results:
        analyze_results(all_results)

        print(f"\n{'='*80}")
        print("BENCHMARK COMPLETE")
        print(f"{'='*80}")

if __name__ == "__main__":
    main()