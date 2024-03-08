import os
import sys
import traci
import random
import matplotlib.pyplot as plt

# Adjust these paths according to your SUMO installation and simulation files
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")

sumoBinary = "sumo-gui"  # Use "sumo" for headless simulation
sumoCmd = [sumoBinary, "-c", "sumo/2w.sumocfg"]

# Define simulation parameters
min_delay = 0.00001  # Minimum packet delay in seconds
max_delay = 0.00050  # Maximum packet delay in seconds
num_messages_range = range(1, 100)  # Number of messages to simulate

# Start SUMO with TraCI
traci.start(sumoCmd)

# Lists to store simulation results
total_delays = []

# Main simulation loop
for num_messages in num_messages_range:
    total_delay_ms = 0
    for _ in range(num_messages):
        # Simulate message exchange between two vehicles with random delays
        delay = random.uniform(min_delay, max_delay)
        total_delay_ms += delay * 1000
        # In a real scenario, here you would trigger actions based on message receipt, 
        # adjust vehicle behavior, etc.

    total_delays.append(total_delay_ms)

    # Advance the simulation to reflect time passage
    traci.simulationStep()

# End the simulation
traci.close()

# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(list(num_messages_range), total_delays, '-o', label='Total Delay')
plt.xlabel('Packets sent from vehicle 0 to vehicle 1')
plt.ylabel('Total Delay (milliseconds)')
plt.legend()
plt.grid(False)
plt.show()
