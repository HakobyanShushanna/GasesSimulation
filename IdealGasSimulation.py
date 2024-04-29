import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Required functions
def maxwell_boltzmann_speed_scaled(temperature, mass, num_samples, max_speed):
    kB = 1.380649e-23
    v_avg = np.sqrt(2 * kB * temperature / mass)
    sigma = np.sqrt(kB * temperature / mass)
    speeds = np.random.normal(loc=v_avg, scale=sigma, size=num_samples)
    speeds *= max_speed / np.max(speeds)
    return speeds

# Parameters
width = float(input("Insert width in meters: "))
height = float(input("Insert height in meters: "))
depth = float(input("Insert depth in meters: "))

num_points = 100 
temperature = 295  # Room temperature in Kelvin
mass = 1.67e-27  # nitrogen molecule mass
speeds = maxwell_boltzmann_speed_scaled(temperature, mass, num_points, 1)

# Generate random initial positions
x_mid = width / 2
y_mid = height / 2
z_mid = depth / 2
std_dev = 0.1  # Standard deviation for initial positions

x_data = np.random.normal(loc=x_mid, scale=std_dev, size=num_points)
y_data = np.random.normal(loc=y_mid, scale=std_dev, size=num_points)
z_data = np.random.normal(loc=z_mid, scale=std_dev, size=num_points)

# Generate random initial directions for each point
directions = np.random.uniform(low=-1, high=1, size=(num_points, 3))

# Create figure and 3D axis
fig = plt.figure("Ideal Gases Simulation")
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(x_data, y_data, z_data)

# Text annotations for temperature, mass, pressure, and R
temperature_annotation = ax.text2D(0.02, 0.95, "Temperature: {} K".format(temperature), transform=ax.transAxes)
mass_annotation = ax.text2D(0.02, 0.90, "Mass: {} kg".format(mass), transform=ax.transAxes)
pressure_annotation = ax.text2D(0.02, 0.85, "Pressure: {} Pa".format(101325), transform=ax.transAxes)
R_annotation = ax.text2D(0.02, 0.80, "Gas Constant: {} J/(mol*K)".format(8.314), transform=ax.transAxes)

# Update function for animation
def update(frame):
    global x_data, y_data, z_data, directions
    
    # Update positions based on current directions and speeds
    x_data += 0.01 * speeds * directions[:, 0]
    y_data += 0.01 * speeds * directions[:, 1]
    z_data += 0.01 * speeds * directions[:, 2]
    
    # Check for collisions with walls and update directions accordingly
    for i in range(num_points):
        if x_data[i] < 0 or x_data[i] > width:
            directions[i, 0] *= -1
        if y_data[i] < 0 or y_data[i] > height:
            directions[i, 1] *= -1
        if z_data[i] < 0 or z_data[i] > depth:
            directions[i, 2] *= -1
    
    # Clip positions to remain within the boundaries of the box
    x_data = np.clip(x_data, 0, width)
    y_data = np.clip(y_data, 0, height)
    z_data = np.clip(z_data, 0, depth)
    
    scatter._offsets3d = (x_data, y_data, z_data)
    
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_zlim(0, depth)

    return scatter, temperature_annotation, mass_annotation, pressure_annotation, R_annotation

# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=100)
plt.show()