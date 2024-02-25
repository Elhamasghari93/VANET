import traci
import matplotlib.pyplot as plt

# pip install matplotlib


# Simulation commands to open SUMO in traci
sumo_binary = "sumo-gui"
sumocfg = "sumo/2w.sumocfg"
sumo_cmd = [sumo_binary, "-c", sumocfg]

# Start the simulation
traci.start(sumo_cmd)

try:
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        # Get the list of vehicle IDs
        vehicle_ids = traci.vehicle.getIDList()
        
        # Get Instances
        
        
finally:
    # Close the TraCI connection
    traci.close()
