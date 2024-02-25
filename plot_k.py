import json
import matplotlib.pyplot as plt
import os
import numpy as np
import re

def read_cluster_data(json_dir="json"):
    cluster_sizes_over_time = []
    steps = []

    # Use a regular expression to match files following the "step_{step}.json" pattern
    json_files = os.listdir(json_dir)
    step_file_pattern = re.compile(r'^step_(\d+)\.json$')

    # Filter and sort files by extracting the integer step value
    json_files_sorted = sorted(
        (file for file in json_files if step_file_pattern.match(file)),
        key=lambda x: int(step_file_pattern.match(x).group(1))
    )

    for json_file in json_files_sorted:
        step = int(step_file_pattern.match(json_file).group(1))
        steps.append(step)
        with open(os.path.join(json_dir, json_file), 'r') as f:
            cluster_data = json.load(f)
            cluster_sizes = {str(cluster_id): len(vehicles) for cluster_id, vehicles in cluster_data.items()}
            cluster_sizes_over_time.append(cluster_sizes)
    return steps, cluster_sizes_over_time

def plot_cluster_sizes(steps, cluster_sizes_over_time):
    all_clusters = set()
    for sizes in cluster_sizes_over_time:
        all_clusters.update(sizes.keys())
    all_clusters = sorted(all_clusters, key=int)

    size_history = {cluster: [] for cluster in all_clusters}

    for sizes in cluster_sizes_over_time:
        for cluster in all_clusters:
            size_history[cluster].append(sizes.get(cluster, 0))

    plt.figure(figsize=(12, 6))
    for cluster, sizes in size_history.items():
        plt.plot(steps, sizes, marker='o', linestyle='-', label=f'Cluster {cluster}')

    plt.title('Number of Vehicles in Each Cluster Over Time')
    plt.xlabel('Simulation Step')
    plt.ylabel('Number of Vehicles')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def main():
    json_dir = "json"  # Ensure this matches the directory where JSON files are stored
    steps, cluster_sizes_over_time = read_cluster_data(json_dir)
    plot_cluster_sizes(steps, cluster_sizes_over_time)

if __name__ == "__main__":
    main()
