import os
import traci
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

# SUMO initialization parameters
sumo_binary = "sumo-gui"  # or "sumo" for non-GUI version
sumocfg = "sumo/2w.sumocfg"
sumo_cmd = [sumo_binary, "-c", sumocfg]

# Function to initialize SUMO and TraCI
def start_simulation(sumo_cmd):
    traci.start(sumo_cmd)

# Function to perform K-Means clustering
def perform_clustering(data, n_clusters=3):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    return kmeans.fit_predict(data), kmeans

# Visualization and data storage
def plot_and_save(data, labels, step, cluster_centers, plot_dir="plots"):
    plt.figure(figsize=(10, 6))
    
    # Plot each cluster
    for label in np.unique(labels):
        cluster_data = data[labels == label]
        plt.scatter(cluster_data[:, 0], cluster_data[:, 1], label=f'Cluster {label+1}')
    
    # Plot cluster centers
    plt.scatter(cluster_centers[:, 0], cluster_centers[:, 1], s=300, c='red', marker='*', label='Centroids')
    
    plt.title(f'Step {step}: Vehicle Clustering')
    plt.xlabel('Position X')
    plt.ylabel('Position Y')
    plt.legend()
    
    # Save plot
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    plt.savefig(f"{plot_dir}/step_{step}.png")
    plt.close()

def main():
    # Start SUMO simulation
    start_simulation(sumo_cmd)

    cluster_sizes_over_steps = []  # List to store the size of each cluster at each step

    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()

        # Collect vehicle data
        vehicle_data = np.array([traci.vehicle.getPosition(vid) + (traci.vehicle.getSpeed(vid),) for vid in vehicle_ids])

        if len(vehicle_data) > 1:  # Ensure we have enough vehicles for clustering
            # Perform clustering based on current data
            labels, kmeans = perform_clustering(vehicle_data[:, :2], n_clusters=min(5, len(vehicle_ids)))

            # Plot and save current clustering state
            plot_and_save(vehicle_data[:, :2], labels, step, kmeans.cluster_centers_)

            # Count the number of vehicles in each cluster
            unique, counts = np.unique(labels, return_counts=True)
            cluster_sizes = dict(zip(unique, counts))
            cluster_sizes_over_steps.append(cluster_sizes)

        step += 1

    traci.close()

    # # Plot the number of vehicles in each cluster over time
    # plt.figure(figsize=(10, 6))
    # for cluster_id in range(min(5, len(vehicle_ids))):  # Assuming max 5 clusters or less depending on vehicle count
    #     sizes = [step.get(cluster_id, 0) for step in cluster_sizes_over_steps]
    #     plt.plot(sizes, label=f'Cluster {cluster_id + 1}')

    # plt.title('Number of Vehicles in Each Cluster Over Time')
    # plt.xlabel('Simulation Step')
    # plt.ylabel('Number of Vehicles')
    # plt.legend()
    # plt.show()

if __name__ == "__main__":
    main()
