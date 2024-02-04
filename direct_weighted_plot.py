import traci
import random
import matplotlib.pyplot as plt

packet_forwarding_betha = 1.2

weighted_distance_mult = 0.1
weighted_velocity_mult = 0.1
weighted_trust_mult = 0.8

num_messages = 10
loss_probability = 0.5
min_delay = 0.3
max_delay = 0.9

sumo_binary = "sumo-gui"
sumocfg = "sumo/2w.sumocfg"
sumo_cmd = [sumo_binary, "-c", sumocfg]

def simulate_delay():
    return random.uniform(min_delay, max_delay)

def simulate_packet_loss():
    if random.random() < loss_probability:
        return True

def get_position(x):
    return traci.vehicle.getPosition(x)

def get_distance_2D(a, b):
    return traci.simulation.getDistance2D(get_position(a)[0], get_position(a)[1], get_position(b)[0], get_position(b)[1])

def get_relative_speed(a, b):
    return abs(traci.vehicle.getSpeed(a) - traci.vehicle.getSpeed(b))

def calculate_poss(distance, velocity, trust):
    return ((weighted_distance_mult * distance) + (weighted_velocity_mult * velocity) + (weighted_trust_mult * trust))

def simulate_packeting():
    total_delay = 0
    number_of_dropped_packets = 0
    number_of_forwarded_packets = 0

    for m in range(1, num_messages + 1):
        delay = simulate_delay()
        total_delay += delay
        avg_delay = total_delay / m
        if delay <= avg_delay * packet_forwarding_betha:
            number_of_forwarded_packets += 1
        else:
            number_of_dropped_packets += 1
    
    trust = number_of_forwarded_packets / num_messages
    
    return trust

# Initialize Matplotlib plot data
steps = []
pch_values = []

traci.start(sumo_cmd)

try:
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()

        if len(vehicle_ids) > 1:
            vehicle_a = vehicle_ids[0]
            vehicle_b = vehicle_ids[1]
            
            relative_distance = get_distance_2D(vehicle_a, vehicle_b)
            relative_velocity = get_relative_speed(vehicle_a, vehicle_b)
            trust = simulate_packeting()

            pch = calculate_poss(relative_distance, relative_velocity, trust)
            steps.append(step)
            pch_values.append(pch)
            step += 1

finally:
    traci.close()

# Plotting the Pch values over simulation steps
plt.figure(figsize=(10, 6))
plt.plot(steps, pch_values, marker='o', linestyle='--', color='b')
plt.title('Pch Changes Over Simulation Steps')
plt.xlabel('Simulation Step')
plt.ylabel('Pch Value')
plt.grid(True)
plt.savefig('pch_plot.png')
plt.show()
