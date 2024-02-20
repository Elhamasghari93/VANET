import traci
import random
import matplotlib.pyplot as plt
#import sklearn.cluster.KMeans

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
        

finally:
    traci.close()