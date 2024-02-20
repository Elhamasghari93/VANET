import traci
import random
import matplotlib.pyplot as plt

# Initialize simulation parameters
packet_forwarding_betha = 1.2
main_formula_lambda = 0.3
is_neighber_distance_threshold = 100

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

# Simulation functions
def simulate_delay():
    return random.uniform(min_delay, max_delay)

def simulate_packet_loss():
    return random.random() < loss_probability

def get_position(x):
    return traci.vehicle.getPosition(x)

def get_distance_2D(a, b):
    return traci.simulation.getDistance2D(
        get_position(a)[0], get_position(a)[1],
        get_position(b)[0], get_position(b)[1], False)

# Checks if the distance between to vehicles is less than a threshold
def check_distance(v1, v2):
    return get_distance_2D(v1, v2) < is_neighber_distance_threshold

def get_relative_speed(a, b):
    return abs(traci.vehicle.getSpeed(a) - traci.vehicle.getSpeed(b))

def calculate_poss(distance, velocity, trust):
    return ((weighted_distance_mult * distance) + 
            (weighted_velocity_mult * velocity) + 
            (weighted_trust_mult * trust))

def simulate_packeting():
    total_delay = 0
    number_of_dropped_packets = 0
    number_of_forwarded_packets = 0

    for m in range(1, num_messages + 1):
        if simulate_packet_loss():
            continue

        delay = simulate_delay()
        total_delay += delay
        avg_delay = total_delay / m

        if delay <= avg_delay * packet_forwarding_betha:
            number_of_forwarded_packets += 1
        else:
            number_of_dropped_packets += 1

    if num_messages == number_of_dropped_packets:
        return 0

    direct_trust = number_of_forwarded_packets / (num_messages )
    return direct_trust

# Function to calculate IndirectTrust for a vehicle
def calculate_indirect_trust(vehicle_n, vehicle_ids):
    indirect_trust = 0
    for vehicle_m in vehicle_ids:
        if vehicle_n != vehicle_m and check_distance(vehicle_n, vehicle_m):
            # Assuming that simulate_packeting calculates DirectTrust for now
            direct_trust = simulate_packeting()
            indirect_trust += direct_trust
    return indirect_trust

def calculate_trust(vehicle_n, vehicle_ids):
    direct_trust = simulate_packeting()
    indirect_trust = calculate_indirect_trust(vehicle_n, vehicle_ids)
    trust = main_formula_lambda * direct_trust + (1 - main_formula_lambda) * indirect_trust
    return trust

steps = []
pch_values = []

# Main simulation loop
traci.start(sumo_cmd)
try:
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehicle_ids = traci.vehicle.getIDList()

        for vehicle_n in vehicle_ids:
            # Calculate IndirectTrust for the current vehicle
            indirect_trust_for_n = calculate_indirect_trust(vehicle_n, vehicle_ids)
            # Here you can use the indirect_trust_for_n value for further decisions or analysis

        # Example usage of PCH calculation for two random vehicles
        if len(vehicle_ids) > 1:
            vehicle_a = vehicle_ids[0]
            vehicle_b = vehicle_ids[1]
            
            relative_distance = get_distance_2D(vehicle_a, vehicle_b)
            relative_velocity = get_relative_speed(vehicle_a, vehicle_b)
            # direct_trust = simulate_packeting()  # This should be the actual DirectTrust calculation
            trust = calculate_trust(vehicle_a, vehicle_ids)

            pch = calculate_poss(relative_distance, relative_velocity, trust)
            steps.append(step)
            pch_values.append(pch)

        step += 1

finally:
    traci.close()
    plt.plot(steps, pch_values)
    plt.xlabel('Simulation Step')
    plt.ylabel('PCH Value')
    plt.show()