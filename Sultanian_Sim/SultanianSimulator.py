import numpy as np
import json
import csv
from datetime import datetime

class SultanianSimulator:
    def __init__(self, drone_name="Drone-Alpha"):
        self.drone_name = drone_name
        self.logs = []

    def run_simulation(self, governor, engine, environment_path):
        """
        Runs the drone through a sequence of external potentials.
        """
        print(f"--- Starting Sultanian Flight Simulation: {self.drone_name} ---")
        
        for i, phi in enumerate(environment_path):
            # 1. Recalculate Governor Tuning
            psi = governor.solve_instantaneous(phi, engine.base_mass, 1200)
            
            # 2. Engine updates the physical state
            k = engine.apply_shroud(phi, psi)
            
            # 3. Log the telemetry
            entry = {
                "step": i,
                "timestamp": datetime.now().isoformat(),
                "external_phi": round(phi, 6),
                "governor_psi": round(psi, 12),
                "k_factor": k,
                "status": "GHOSTED" if k < 0.1 else "DECOHERENT"
            }
            self.logs.append(entry)
        
        print(f"Simulation Complete. {len(self.logs)} steps recorded.")

    def export_json(self, filename="simulation_results.json"):
        with open(filename, 'w') as f:
            json.dump({"metadata": {"vessel": self.drone_name}, "data": self.logs}, f, indent=4)
        print(f"Exported to JSON: {filename}")

    def export_csv(self, filename="simulation_results.csv"):
        if not self.logs:
            return
        keys = self.logs[0].keys()
        with open(filename, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.logs)
        print(f"Exported to CSV: {filename}")

# --- Example Usage for your Paper ---
if __name__ == "__main__":
    from core.generator import Governor
    from physics.engine import SultanianEngine

    # Define the 'Scrunch' Zone path
    path = np.linspace(0, -0.9, 50).tolist() + np.linspace(-0.9, 0, 50).tolist()

    sim = SultanianSimulator(drone_name="Tactical-Drone-01")
    gov = Governor()
    eng = SultanianEngine(drone_mass=2.0)

    sim.run_simulation(gov, eng, path)
    sim.export_csv("sultanian_step14_results.csv")