import traci
import random
import matplotlib.pyplot as plt
#import sklearn.cluster.KMeans
from sklearn.cluster import KMeans

sumo_binary = "sumo-gui"
sumocfg = "sumo/2w.sumocfg"
sumo_cmd = [sumo_binary, "-c", sumocfg]

traci.start(sumo_cmd)
try:
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()
        # Speed, Accel, Distance > sklearn.cluster.KMeans
         # Collect data for clustering (e.g., speed, accel, distance)
        data_points = []
        for vehicle_id in vehicle_ids:
            speed = traci.vehicle.getSpeed(vehicle_id)
            accel = traci.vehicle.getAcceleration(vehicle_id)
            distance = traci.vehicle.getLanePosition(vehicle_id)
            data_points.append([speed, accel, distance])

        # Perform KMeans clustering
        k = 3  # Number of clusters (you can adjust this)
        kmeans = KMeans(n_clusters=k)
        clusters = kmeans.fit_predict(data_points)

        # Now 'clusters' contains the cluster assignments for each data point
        

finally:
    traci.close()