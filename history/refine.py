import traci


# simulation commands to open SUMO in traci
sumo_binary = "sumo-gui"
sumocfg = "sumo/2w.sumocfg"
sumo_cmd = [sumo_binary, "-c", sumocfg]

# start the simulation
traci.start(sumo_cmd)

try:
    step = 0
    while step < 1000:
        traci.simulationStep()

        vehicle_ids = traci.vehicle.getIDList()
        vehicle_0_id = vehicle_ids[0]

        # Check if there is an element at index 1 in vehicle_ids
        if len(vehicle_ids) > 1:
            vehicle_1_id = vehicle_ids[1]
        else:
            print("Not enough elements in vehicle_ids to assign vehicle_1_id")
            vehicle_1_id = None  # You can assign a default value or None if needed

        vehicle_0_position = traci.vehicle.getPosition(vehicle_0_id)
        vehicle_0_speed = traci.vehicle.getSpeed(vehicle_0_id)
        
        
        if vehicle_1_id is not None:
            vehicle_1_position = traci.vehicle.getPosition(vehicle_1_id)
            vehicle_1_speed = traci.vehicle.getSpeed(vehicle_1_id)

            distance = traci.simulation.getDistance2D(vehicle_0_position[0], vehicle_1_position[0], vehicle_0_position[1], vehicle_1_position[1])

            alpha=0.4
            betha=0.6

            relative_speed = (vehicle_0_speed / vehicle_1_speed)

            weighted_value = (alpha * distance) + (betha * relative_speed)
            print(weighted_value)

finally:
    traci.close()

# Relative Speed
# R&D: matplot
# socket messages in python: TCP Messages
