import sys
import os

from viz.dashboard import flight_control_loop, run_simulation

# Ensures the current directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.generator import Governor
from physics.engine import SultanianEngine
import numpy as np

def simulate_snap_maneuver():
    """Simulates the drone entering a high-gradient 'Scrunch' zone."""
    print("--- Sultanian Protocol Initialization ---")
    drone_mass = 2.0  # 2kg Drone
    
    gov = Governor()
    eng = SultanianEngine(drone_mass)
    
    # Simulate a Step-14 Potential Spike
    external_scrunch = -0.15 
    reactor_power = 1200 # Watts
    
    # Solve for Z0
    psi = gov.solve_instantaneous(external_scrunch, drone_mass, reactor_power)
    
    # Apply to Engine
    k = eng.apply_shroud(external_scrunch, psi)
    
    print(f"External Potential: {external_scrunch}")
    print(f"Governor Tuning (Psi): {psi:.12f}")
    print(f"Resulting Inertia (k-factor): {k}")
    
    if k < 0.01:
        print("STATUS: PHASE-LOCK ACHIEVED. DRONE IS GHOSTED.")
    else:
        print("STATUS: COHERENCE FAILED. HIGH INERTIA DETECTED.")

import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Ensure Python can find the local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.generator import Governor
from physics.engine import SultanianEngine

class SultanianDrone:
    """Wrapper to hold the drone's physical and logic components."""
    def __init__(self, mass=2.0, power=500):
        self.mass = mass
        self.reactor_power = power
        self.position = 0.0
        self.velocity = 100.0  # m/s
        self.time_step = 0.01
        self.governor = Governor()
        self.engine = SultanianEngine(mass)

def simulate_snap_maneuver():
    """Demonstrates a single point check for Ghosting."""
    print("\n--- [1] Snap Maneuver Test ---")
    drone = SultanianDrone()
    phi = -0.15
    psi = drone.governor.solve_instantaneous(phi, drone.mass, drone.reactor_power)
    k = drone.engine.apply_shroud(phi, psi)
    
    print(f"External Potential: {phi}")
    print(f"Governor Tuning (Psi): {psi:.12f}")
    print(f"Resulting Inertia (k-factor): {k}")
    
    if k < 0.01:
        status = "STATUS: PHASE-LOCK ACHIEVED. DRONE IS GHOSTED."
    else:
        status = "STATUS: COHERENCE FAILED. HIGH INERTIA DETECTED."
    #status = "PHASE-LOCK ACHIEVED" if k < 0.1 else "COHERENCE FAILED"
    print(f"Potential: {phi} | Psi: {psi:.6f} | k: {k} | Status: {status}")

def flight_control_loop():
    """Simulates movement through a varying potential field."""
    print("\n--- [2] Flight Control Loop (Active Navigation) ---")
    drone = SultanianDrone()
    # Create a path with varying 'Scrunch' gradients
    path_potentials = np.sin(np.linspace(0, np.pi, 20)) * -0.3
    
    for i, phi in enumerate(path_potentials):
        psi = drone.governor.solve_instantaneous(phi, drone.mass, drone.reactor_power)
        k = drone.engine.apply_shroud(phi, psi)
        
        if k > 0.1:
            print(f"Step {i}: CRITICAL DECOHERENCE at Phi {phi:.4f}")
            return
        
        drone.position += drone.velocity * drone.time_step
        if i % 5 == 0:
            print(f"Step {i}: Position {drone.position:.2f}m | k-factor: {k}")
    print("Flight segment complete. Shadow maintained.")

def run_simulation():
    print("\n--- [3] Running Graphical Simulation ---")
    drone = SultanianDrone()
    potentials = np.linspace(-0.5, 0.5, 100)
    
    psi_history = []
    k_history = []
    
    for phi in potentials:
        psi = drone.governor.solve_instantaneous(phi, drone.mass, drone.reactor_power)
        k = drone.engine.apply_shroud(phi, psi)
        
        psi_history.append(psi)
        k_history.append(k)
    
    # Create two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Plot 1: The Governor's Effort (Psi vs Phi)
    ax1.plot(potentials, psi_history, color='orange', label='Governor Tuning (Psi)')
    ax1.set_ylabel("Phase Offset (Psi)")
    ax1.set_title("Sultanian Governor Response")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: The Physical Result (Inertia Modulation)
    ax2.plot(potentials, k_history, color='cyan', label='Inertia (k-factor)')
    ax2.set_yscale('log')
    ax2.set_ylabel("Effective Inertia (k)")
    ax2.set_xlabel("External Metric Potential (Scrunch)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

def run_turbulence_test():
    drone = SultanianDrone()
    # Add high-frequency noise to the potential
    base_potentials = np.linspace(-0.5, 0.5, 100)
    noise = 0.05 * np.sin(np.linspace(0, 50, 100)) 
    turbulent_phi = base_potentials + noise
    
    k_results = []
    for phi in turbulent_phi:
        # Simulate a slight lag: Governor solves for base_phi, not turbulent_phi
        psi = drone.governor.solve_instantaneous(phi - 0.02, drone.mass, 500)
        k = drone.engine.apply_shroud(phi, psi)
        k_results.append(k)
        
    plt.plot(turbulent_phi, k_results, 'r.')
    plt.title("Decoherence Events in Turbulent Field")
    plt.ylabel("k-factor (1.0 = Crash/Regain Mass)")
    plt.show()


if __name__ == "__main__":
    # Run all three phases of the protocol simulation
    simulate_snap_maneuver()
    flight_control_loop()
    run_simulation()
    run_turbulence_test()