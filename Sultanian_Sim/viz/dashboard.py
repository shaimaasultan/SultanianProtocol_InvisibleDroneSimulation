import matplotlib.pyplot as plt
import numpy as np
from core.generator import Governor
from physics.engine import SultanianEngine

# Proposed logic for your controller module
def flight_control_loop(drone, path_potentials):
    for phi in path_potentials:
        # The Governor must solve for the new coordinate's 'Scrunch'
        psi = drone.governor.solve_instantaneous(phi, drone.mass, drone.reactor_power)
        
        # Check if we maintained the lock
        k = drone.engine.apply_shroud(phi, psi)
        
        if k > 0.1:
            print(f"CRITICAL: Decoherence at Potential {phi}! Vessel regained mass.")
            break
        else:
            # Move the drone using low-inertia physics
            drone.position += drone.velocity * drone.time_step
            
def run_simulation():
    drone_mass = 2.0 # 2kg Drone
    gov = Governor()
    eng = SultanianEngine(drone_mass)
    
    # Simulate a transit through a high-gradient 'Scrunch' zone
    potentials = np.linspace(-0.5, 0.5, 100)
    k_history = []
    
    for phi in potentials:
        # 1. Governor solves for the current vacuum state
        psi = gov.solve_instantaneous(phi, drone_mass, 500) # 500W Reactor
        
        # 2. Engine updates the physical state of the drone
        k = eng.apply_shroud(phi, psi)
        k_history.append(k)
    
    plt.plot(potentials, k_history)
    plt.yscale('log')
    plt.title("Inertia Modulation (k-factor) during Sultanian Transit")
    plt.xlabel("External Metric Potential (Scrunch)")
    plt.ylabel("Effective Inertia (k)")
    plt.grid(True)
    plt.show()

# if __name__ == "__main__":
#     run_simulation()