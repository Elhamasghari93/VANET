# Add TraCI Library
import traci
import time

# Simulation Commands to open the SUMO in TraCI
sumo_binary = "sumo-gui"
sumocfg = "sumo/2w.sumocfg"
sumo_cmd = [sumo_binary, "-c", sumocfg]

# Start the simulation
traci.start(sumo_cmd)

# Loop the simulation steps
try:
    step = 0

    # Main loop of simulation
    while step < 1000:

        traci.simulationStep()

        # Step 1: Get ID's List
        # vehicle_ids = traci.vehicle.getIDList()
        # vehicle_0__id = vehicle_ids[0]
        # vehicle_0__position = traci.vehicle.getPosition(vehicle_0__id)
        # vehicle_0__speed = traci.vehicle.getSpeed(vehicle_0__id)

        # print("-----------------------------------------------")
        # print(f"The vehicle ID: {vehicle_0__id}\nThe vehicle current position is: {vehicle_0__position}\nThe vehicle current speed is: {vehicle_0__speed}")
        # print("-----------------------------------------------")

        ######### START FROM HERE! #########

        # 1. List of vehicles
        # 2. Get 2 Instances(ID's) from the list. tip: check if exist
        # 3. Get the current position of the vehicles.
        # 4. Get the current speed of the vehicles.
        # 5. Calculate the euclidean distance between the two vehicles. tip: you can use python math library, or generate the formula yourself!
        # 6. Define two variables. alpha and betha. assign two values for weight. note: alpha + betha is always equels to 1!
        # 7. Calculate the relative speed of 0,1
        # 8. Generate this formula: p = (alpha * distance(x,y)) + (betha * speed(x,y))

        step += 1

# Close the simulation at the end
finally:
    traci.close()