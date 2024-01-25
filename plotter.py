import traci
import matplotlib.pyplot as plt

# pip install matplotlib


# Simulation commands to open SUMO in traci
sumo_binary = "sumo-gui"
sumocfg = "sumo/2w.sumocfg"
sumo_cmd = [sumo_binary, "-c", sumocfg]

# Start the simulation
traci.start(sumo_cmd)

# Initialize lists to store time steps and vehicle speeds
time_steps = []
vehicle_speeds = []

try:
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        # Get the list of vehicle IDs
        vehicle_ids = traci.vehicle.getIDList()

        if vehicle_ids:
            # Use the first vehicle in the list
            my_vehicle = vehicle_ids[0]
            my_vehicle_speed = traci.vehicle.getSpeed(my_vehicle)

            # Append the current simulation step and vehicle speed to the lists
            time_steps.append(traci.simulation.getTime())
            vehicle_speeds.append(my_vehicle_speed)
    
    # Plotting the vehicle speed over time
    plt.plot(time_steps, vehicle_speeds)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Speed (m/s)')
    plt.title('Speed of My Vehicle Over Time')
    plt.grid(True)

    # Save the plot as a JPEG file
    plt.savefig('speed_changes.jpg', format='jpg')

    # Show the plot
    plt.show()
        
finally:
    # Close the TraCI connection
    traci.close()
