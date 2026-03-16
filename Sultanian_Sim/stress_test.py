import numpy as np
import time

class StressTestDrone:
    def __init__(self, compute_frequency_hz):
        self.mass = 2.0
        self.R = 1.1
        # Logic-gate lag is 1 / compute_frequency
        self.latency = 1.0 / compute_frequency_hz 
        self.is_destroyed = False

    def governor_response(self, current_phi):
        """Simulates the 10^-15s logic gate delay."""
        # The 'Lag' means the Governor is always solving for 
        # the potential from one latency-step ago.
        return -(current_phi * self.R)

    def check_coherence(self, actual_phi, applied_psi):
        """The Alexander Space-Constraint Check."""
        # If the discrepancy is too high, the shroud 'shimmers' and fails.
        residual = abs(actual_phi + (applied_psi / self.R))
        if residual > 0.05: # Threshold for structural failure
            self.is_destroyed = True
        return residual

def run_velocity_test(velocity_mps):
    # Standard Tactical Governor (5.2 THz)
    drone = StressTestDrone(compute_frequency_hz=5.2e12)
    
    # Define a 'Scrunch' Zone (sine wave of gravity)
    distance = 1000  # meters
    dt = 0.0001      # simulation step
    t_max = distance / velocity_mps
    
    print(f"\n--- Testing Velocity: {velocity_mps} m/s ---")
    
    last_phi = 0
    for t in np.arange(0, t_max, dt):
        # Current position in the fluctuating field
        pos = velocity_mps * t
        current_phi = -0.5 * np.sin(0.01 * pos) # The 'Grid Scrunch'
        
        # The Governor tries to keep up, but it has 'Latency'
        # It applies the PSI calculated from the 'last' known state
        applied_psi = drone.governor_response(last_phi)
        
        error = drone.check_coherence(current_phi, applied_psi)
        last_phi = current_phi # Update for next cycle
        
        if drone.is_destroyed:
            print(f"CRASH DETECTED at {pos:.2f}m! Shimmer residual: {error:.4f}")
            print("STATUS: LOGIC-GATE LAG EXCEEDED TOLERANCE.")
            return False
            
    print("STATUS: TRANSIT SUCCESSFUL. COHERENCE MAINTAINED.")
    return True

if __name__ == "__main__":
    # Test different speeds
    velocities = [100, 1000, 10000, 50000]
    for v in velocities:
        if not run_velocity_test(v):
            break