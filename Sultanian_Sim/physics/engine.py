class SultanianEngine:
    def __init__(self, drone_mass):
        self.base_mass = drone_mass
        self.k_factor = 1.0  # Current Inertia Scale
        self.transmissibility = 0.0 # T-factor
        # In main.py
        external_scrunch = -0.05 # Lighter gravity zone (e.g., further from a planet)
        reactor_power = 500      # Lower reactor noise

    def apply_shroud(self, ext_phi, psi):
        """
        Calculates the residual error and updates the k-factor.
        If error -> 0, the drone 'Ghosts'.
        """
        residual_error = abs(ext_phi + (psi / 1.1)) # Normalized error
        
        # The 'Sultanian Restoration' effect: 
        # Lower error leads to non-linear inertia drop
        if residual_error < 1e-8:
            self.k_factor = 1e-6  # Ghost State (Near-zero mass)
            self.transmissibility = 0.999 # Transparency
            self.is_ghosted = True
        else:
            self.k_factor = 1.0
            self.transmissibility = 0.05
            
        return self.k_factor