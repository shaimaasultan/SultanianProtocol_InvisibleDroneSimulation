import numpy as np
import matplotlib.pyplot as plt

class SultanianVessel:
    def __init__(self, R_margin=1.1, k_factor=1.0):
        self.R = R_margin   # Identity Margin
        self.k = k_factor   # Inertia Constant
        self.mass = 2.0     # 2kg Base Mass

    def calculate_visibility(self, external_phi):
        """
        Determines if the Resonant Shadow is holding.
        """
        # The Alexander Space-Constraint check
        # Visibility is a function of how far we are from the ideal R=1.1
        tuning_error = abs(self.R - 1.1)
        
        # If tuning is off or k is high, the drone 'scatters' the plenum energy
        if tuning_error < 1e-6 and self.k < 1e-5:
            return "INVISIBLE (Ghost State)", 0.001 # 0.1% signature
        else:
            # signature strength is proportional to inertia and tuning error
            signature = self.k * (1 + tuning_error * 10)
            return "VISIBLE (Metric Interaction)", min(signature, 1.0)

def run_visibility_experiment():
    # TEST 1: Ideal Protocol (Invisible)
    ghost_drone = SultanianVessel(R_margin=1.1, k_factor=1e-6)
    
    # TEST 2: Misaligned Tuning (Visible)
    misaligned_drone = SultanianVessel(R_margin=1.4, k_factor=1e-6)
    
    # TEST 3: High Inertia (Visible)
    heavy_drone = SultanianVessel(R_margin=1.1, k_factor=1.0)

    drones = [ghost_drone, misaligned_drone, heavy_drone]
    labels = ["Perfect Protocol", "Misaligned R", "High k-factor"]
    
    print(f"{'Configuration':<20} | {'Status':<25} | {'Signature'}")
    print("-" * 65)
    
    results = []
    for d, label in zip(drones, labels):
        status, signal = d.calculate_visibility(external_phi=-0.2)
        results.append(signal)
        print(f"{label:<20} | {status:<25} | {signal:.4f}")

    # Plotting the "Radar Cross Section" (Metric Signature)
    plt.figure(figsize=(8, 5))
    plt.bar(labels, results, color=['cyan', 'orange', 'red'])
    plt.ylabel("Detection Signature (Metric Wake)")
    plt.title("Sultanian Protocol: Visibility vs. Parameter Tuning")
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def calculate_signature(R, k):
    """
    Calculates the Metric Signature (Visibility).
    Perfect Shadow: R=1.1, k=1e-6 -> Signature ~ 0
    """
    # Deviation from the Alexander Space-Constraint
    tuning_error = abs(R - 1.1)
    
    # Signature is the product of mass-coupling (k) and phase-mismatch
    # We use a log-base approach to show the 'Ghosting' effect clearly
    sig = k * (1 + tuning_error * 50)
    return min(sig, 1.0)

# Setup the figure and axis
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.25)

# Initial Parameters
initial_R = 1.1
initial_k = 0.5

# Initial Calculation
sig = calculate_signature(initial_R, initial_k)
bar = ax.bar(["Drone Metric Signature"], [sig], color='cyan', edgecolor='white')
ax.set_ylim(0, 1.1)
ax.set_ylabel("Visibility / Detection Probability")
ax.set_title("Sultanian Protocol Visibility Dashboard", color='white')

# Styling for the 'Command Center' look
ax.set_facecolor('#1a1a1a')
fig.set_facecolor('#1a1a1a')
ax.tick_params(colors='white')
ax.yaxis.label.set_color('white')

# Create Sliders
ax_R = plt.axes([0.2, 0.1, 0.6, 0.03], facecolor='#333333')
ax_k = plt.axes([0.2, 0.05, 0.6, 0.03], facecolor='#333333')

s_R = Slider(ax_R, 'R (Margin)', 0.5, 2.0, valinit=initial_R, color='orange')
s_k = Slider(ax_k, 'k (Unlock)', 0.000001, 1.0, valinit=initial_k, color='lime')

def update(val):
    R = s_R.val
    k = s_k.val
    new_sig = calculate_signature(R, k)
    
    # Update bar height and color
    bar[0].set_height(new_sig)
    
    # Color logic: Cyan for Ghosting, Red for Visible
    if new_sig < 0.01:
        bar[0].set_color('cyan')
        ax.set_title("STATUS: GHOST STATE (INVISIBLE)", color='cyan')
    elif new_sig < 0.5:
        bar[0].set_color('yellow')
        ax.set_title("STATUS: METRIC SHIMMER (PARTIAL)", color='yellow')
    else:
        bar[0].set_color('red')
        ax.set_title("STATUS: HIGH VISIBILITY ( Newtonian )", color='red')
        
    fig.canvas.draw_idle()

s_R.on_changed(update)
s_k.on_changed(update)

print("Control Panel Active. Move sliders to adjust Metric Resonance.")
plt.show()

# if __name__ == "__main__":
#     run_visibility_experiment()