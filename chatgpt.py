import os
import traci
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import json


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

    cluster_membership_history = []
    num_clusters_history = []

    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()

        # Collect vehicle data
        vehicle_data = np.array([traci.vehicle.getPosition(vid) + (traci.vehicle.getSpeed(vid),) for vid in vehicle_ids])

        if len(vehicle_data) > 1:  # Ensure we have enough vehicles for clustering
            # Perform clustering based on current data
            labels, kmeans = perform_clustering(vehicle_data[:, :2], n_clusters=min(5, len(vehicle_ids)))

            # Store cluster membership and number of clusters for history
            cluster_membership_history.append(labels)
            num_clusters_history.append(len(np.unique(labels)))

            # Plot and save current clustering state
            plot_and_save(vehicle_data[:, :2], labels, step, kmeans.cluster_centers_)

        step += 1

    traci.close()

    # Plot the history of cluster memberships and number of clusters
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(num_clusters_history)
    plt.title('Number of Clusters Over Time')
    plt.xlabel('Step')
    plt.ylabel('Number of Clusters')

    plt.subplot(1, 2, 2)
    plt.plot([len(np.unique(cm)) for cm in cluster_membership_history])
    plt.title('Unique Cluster Memberships Over Time')
    plt.xlabel('Step')
    plt.ylabel('Unique Memberships')
    
    plt.tight_layout()
    plt.savefig("plots/cluster_history.png")
    plt.show()

if __name__ == "__main__":
    main()