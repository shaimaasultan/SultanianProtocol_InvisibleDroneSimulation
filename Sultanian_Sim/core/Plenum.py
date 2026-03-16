import numpy as np

class PlenumEnvironment:
    """Simulates the space as a 'Phase-Locked' energy sea."""
    def __init__(self, baseline_pressure=1.0):
        self.P0 = baseline_pressure # Vacuum potential
        self.G = 6.674e-11

    def get_local_scrunch(self, coordinates, nearby_masses):
        """Calculates the Grid-Deformation at a specific point."""
        total_phi = 0
        for mass, pos in nearby_masses:
            dist = np.linalg.norm(coordinates - pos)
            total_phi -= (self.G * mass) / dist
        return total_phi # The external 'Scrunch'