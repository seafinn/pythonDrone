from vpython import *
import numpy as np

scene = canvas(title="Colliding Drones with Repulsion", width=800, height=600, center=vector(0, 0, 0))

radius = 1.0
mass = 1.0
velocity1 = vector(2, 0, 0)  # Velocity of the first drone
velocity2 = vector(-2, 0, 0) # Velocity of the second drone

# Create the drones
drone1 = sphere(pos=vector(-10, 0, 0), radius=radius, color=color.red, make_trail=True)
drone2 = sphere(pos=vector(10, 0, 0), radius=radius, color=color.blue, make_trail=True)

# Lennard-Jones parameters
epsilon = 1.6  # Strength of the repulsion
sigma = 5 * radius  # Distance at which potential is zero (set to 2 * radius)

# Time step and simulation parameters
dt = 0.005
time = 0

# Function to calculate the repulsive Lennard-Jones force
def lj_repulsive_force(r_vector, epsilon, sigma):
    r_mag = mag(r_vector)  # Magnitude of the distance vector
    if r_mag == 0:
        return vector(0, 0, 0)  # Avoid division by zero
    force_magnitude = 2 * epsilon * (sigma / r_mag)**2  # Magnitude of the force
    force_vector = force_magnitude * (r_vector / r_mag)  # Force vector
    return force_vector

# Main simulation loop
while time < 10:
    rate(100)  # Limit the frame rate to 100 updates per second

    # Calculate the distance between the drones
    r_vector = drone2.pos - drone1.pos  # Vector from drone1 to drone2
    r_mag = mag(r_vector)  # Magnitude of the distance vector

    # Calculate the repulsive force
    if r_mag < 3 * sigma:  # Only apply force if drone2 are close
        force = lj_repulsive_force(r_vector, epsilon, sigma)
    else:
        force = vector(0, 0, 0)  # No force if drones are far apart

    velocity1 -= force / mass * dt
    velocity2 += force / mass * dt

    # Update positions of the drones
    drone1.pos += velocity1 * dt
    drone2.pos += velocity2 * dt

    time += dt