from vpython import *
import numpy as np
import random

scene = canvas(title="Colliding Drones with Modified Repulsion", width=800, height=600, center=vector(0, 0, 0))

radius = 1.0
mass = 1.0
num_drones = 30

drones = []

# Lennard-Jones parameters
epsilon = 1.0  # Strength of the repulsion
sigma = 3 * radius  # Distance at which potential is zero

# Time step and simulation parameters
dt = 0.005
time = 0

# Function to calculate the repulsive Lennard-Jones force
def lj_repulsive_force(r_vector, epsilon, sigma):
    r_mag = mag(r_vector)  # Magnitude of the distance vector
    if r_mag == 0:
        return vector(0, 0, 0)  # Avoid division by zero
    force_magnitude = 2 * epsilon * (sigma / r_mag)**2  # Force Magnitude
    force_vector = force_magnitude * (r_vector / r_mag)  # Force vector
    return force_vector

# Initialize drones
for i in range(num_drones):
    pos = vector(random.uniform(-50, 50), random.uniform(-50, 50), 0)
    vel = vector(random.uniform(-5, 5), random.uniform(-5, 5), 0)
    color = vector(random.random(), random.random(), random.random())
    drones.append(sphere(pos=pos, radius=radius, color=color, make_trail=True, velocity=vel))

# Main simulation loop
while time < 10:
    rate(100)  # Limit the frame rate to 100 updates per second

    # Calculate forces and update velocities for each drone
    for i in range(num_drones):
        total_force = vector(0, 0, 0)
        for j in range(num_drones):
            if i != j:
                r_vector = drones[j].pos - drones[i].pos
                r_mag = mag(r_vector)
                if r_mag < 2 * sigma:  # Only apply force if drones are close
                    force = lj_repulsive_force(r_vector, epsilon, sigma)
                    total_force += force

        drones[i].velocity += total_force / mass * dt

    # Update positions of the drones
    for i in range(num_drones):
        drones[i].pos += drones[i].velocity * dt

    time += dt