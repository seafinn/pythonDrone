from vpython import *
import random

scene = canvas(title="Colliding Drones", width=1280, height=720, center=vector(0, 0, 0))

# Parameters
radius = 1.0  # Radius of the cylinders (corners of the cube)
mass = 1.0
num_drones = 5
box_size = 200  # Simulation box size
numCollisions = 0

# Lennard-Jones parameters
epsilon = 1.6  # Strength of the repulsion
sigma = 11 * radius  # Distance at which potential is zero

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

# Function to apply periodic boundary conditions
def apply_pbc(pos, box_size):
    # Apply PBC to x, y, z coordinates
    if pos.x > box_size / 2:
        pos.x -= box_size
    elif pos.x < -box_size / 2:
        pos.x += box_size

    if pos.y > box_size / 2:
        pos.y -= box_size
    elif pos.y < -box_size / 2:
        pos.y += box_size

    if pos.z > box_size / 2:
        pos.z -= box_size
    elif pos.z < -box_size / 2:
        pos.z += box_size

    return pos

# Function to create a drone (flat cube with cylinders on corners)
def create_drone(pos, color, landingPoint):
    # Create a flat cube (box) aligned with the x-y plane
    cube_size = vector(4, 4, 0.5)  # Flat cube dimensions (x, y, z)
    cube = box(pos=pos, size=cube_size, color=color, landingPoint=landingPoint)

    # Create cylinders on each corner of the cube, extending along the z-axis
    cylinder_length = 1.0  # Length of the cylinders
    corner_offset = vector(cube_size.x / 2, cube_size.y / 2, 0)  # Offset to corners

    # List of corner positions relative to the cube's center
    corner_positions = [
        pos + vector(corner_offset.x, corner_offset.y, 0),
        pos + vector(-corner_offset.x, corner_offset.y, 0),
        pos + vector(corner_offset.x, -corner_offset.y, 0),
        pos + vector(-corner_offset.x, -corner_offset.y, 0)
    ]

    # Create cylinders at each corner
    cylinders = []
    for corner_pos in corner_positions:
        cyl = cylinder(pos=corner_pos, axis=vector(0, 0, cylinder_length), radius=radius, color=color)
        cylinders.append(cyl)

    return cube, cylinders

# Initialize drones
drones = []
for i in range(num_drones):
    pos = vector(random.uniform(-100, 100), random.uniform(-100, 100), 0)
    takeoffPoint = pos
    landingPoint = vector(random.uniform(-100, 100), random.uniform(-100, 100), 0)
    unitVec = vector(((landingPoint.x-takeoffPoint.x)/mag(landingPoint-takeoffPoint)), ((landingPoint.y-takeoffPoint.y)/mag(landingPoint-takeoffPoint)), 0)
    vel = vector(unitVec.x, unitVec.y, 0)*-10
    color = vector(random.random(), random.random(), random.random())
    cube, cylinders = create_drone(pos, color, landingPoint)
    drones.append({'cube': cube, 'cylinders': cylinders, 'velocity': vel, 'landingPoint' : landingPoint})

# Main simulation loop
while time < 10:
    rate(100)  # Limit the frame rate to 100 updates per second
    if(drones[i]['cube'].visible == True):
        # Calculate forces and update velocities for each drone
        for i in range(num_drones):
            total_force = vector(0, 0, 0)
            for j in range(num_drones):
                if i != j:
                    r_vector = drones[j]['cube'].pos - drones[i]['cube'].pos
                    # Apply minimum image convention for PBC
                    if r_vector.x > box_size / 2:
                        r_vector.x -= box_size
                    elif r_vector.x < -box_size / 2:
                        r_vector.x += box_size

                    if r_vector.y > box_size / 2:
                        r_vector.y -= box_size
                    elif r_vector.y < -box_size / 2:
                        r_vector.y += box_size

                    if r_vector.z > box_size / 2:
                        r_vector.z -= box_size
                    elif r_vector.z < -box_size / 2:
                        r_vector.z += box_size

                    r_mag = mag(r_vector)
                    if r_mag < 2 * sigma:  # Only apply force if drones are close
                        force = lj_repulsive_force(r_vector, epsilon, sigma)
                        total_force += force

            drones[i]['velocity'] += total_force / mass * dt

        # Update positions of the drones and apply PBC
        for i in range(num_drones):
            # Update cube position
            drones[i]['cube'].pos -= drones[i]['velocity'] * dt
            drones[i]['cube'].pos = apply_pbc(drones[i]['cube'].pos, box_size)

            # Update cylinder positions (relative to the cube)
            corner_offset = vector(2, 2, 0)  # Half of cube_size.x and cube_size.y
            corner_positions = [
                drones[i]['cube'].pos + vector(corner_offset.x, corner_offset.y, 0),
                drones[i]['cube'].pos + vector(-corner_offset.x, corner_offset.y, 0),
                drones[i]['cube'].pos + vector(corner_offset.x, -corner_offset.y, 0),
                drones[i]['cube'].pos + vector(-corner_offset.x, -corner_offset.y, 0)
            ]

            for j in range(num_drones):
                if i != j:
                    if(sqrt((drones[j]['cube'].pos.x - drones[i]['cube'].pos.x)**2 + (drones[j]['cube'].pos.y - drones[i]['cube'].pos.y)**2) <= 4):
                        numCollisions += 1
                        # drones[i]['cube'].visible = False
                        # for idx, cyl in enumerate(drones[i]['cylinders']):
                        #     cyl.visible = False

            for idx, cyl in enumerate(drones[i]['cylinders']):
                cyl.pos = corner_positions[idx]
            # print("Drone ", i, " landing point: ",drones[i]['cube'].landingPoint)
            # print("Drone ", i, " current position: ", drones[i]['cube'].pos)
            # print("Drone ", i, " Distance: ", sqrt((drones[i]['cube'].landingPoint.x - drones[i]['cube'].pos.x)**2 + (drones[i]['cube'].landingPoint.y - drones[i]['cube'].pos.y)**2))
            if(sqrt((drones[i]['cube'].landingPoint.x - drones[i]['cube'].pos.x)**2 + (drones[i]['cube'].landingPoint.y - drones[i]['cube'].pos.y)**2) <= 5):
                drones[i]['cube'].visible = False
                for idx, cyl in enumerate(drones[i]['cylinders']):
                    cyl.visible = False
                continue
    else:
        continue
    time += dt 
print("Total Number of Collisions: ", numCollisions) 