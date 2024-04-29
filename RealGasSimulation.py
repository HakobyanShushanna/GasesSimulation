import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.spatial.distance import pdist, squareform

# Required functions
def maxwell_boltzmann_speed_scaled(temperature, mass, num_samples, max_speed):
    kB = 1.380649e-23
    v_avg = np.sqrt(2 * kB * temperature / mass)
    sigma = np.sqrt(kB * temperature / mass)
    speeds = np.random.normal(loc=v_avg, scale=sigma, size=num_samples)
    speeds *= max_speed / np.max(speeds)
    return speeds

# Generate masses based on particle colors
def generate_masses(num_points, colors):
    masses = np.zeros(num_points)
    for i, color in enumerate(colors):
        if color == 'r':
            masses[i] = 1.67e-27  # Red particles mass
        elif color == 'g':
            masses[i] = 2 * 1.67e-27  # Green particles mass
        elif color == 'b':
            masses[i] = 3 * 1.67e-27  # Blue particles mass
        elif color == 'm':
            masses[i] = 4 * 1.67e-27  # Purple particles mass
    return masses

# Parameters
width = float(input("Insert width in meters: "))
height = float(input("Insert height in meters: "))
depth = float(input("Insert depth in meters: "))

num_points = 100 
temperature = 295  # Room temperature in Kelvin

# Adjust the speed factor to make particles move more slowly
speed_factor = 0.5  # Adjust this value to control the speed of particles
speeds = maxwell_boltzmann_speed_scaled(temperature, 1.67e-27, num_points, speed_factor)  # Mass is initially set to nitrogen molecule mass

# Generate random initial positions
x_mid = width / 2
y_mid = height / 2
z_mid = depth / 2
std_dev = 0.4  # Standard deviation for initial positions

x_data = np.random.normal(loc=x_mid, scale=std_dev, size=num_points)
y_data = np.random.normal(loc=y_mid, scale=std_dev, size=num_points)
z_data = np.random.normal(loc=z_mid, scale=std_dev, size=num_points)

# Generate random initial directions for each point
directions = np.random.uniform(low=-1, high=1, size=(num_points, 3))

# Create figure and 3D axis
fig = plt.figure("Real Gases Simulation")
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(x_data, y_data, z_data)

# Text annotations for temperature, mass, pressure, and R
temperature_annotation = ax.text2D(0.02, 0.95, "Temperature: {} K".format(temperature), transform=ax.transAxes)
mass_annotation = ax.text2D(0.02, 0.90, "Mass: {} kg".format(1.67e-27), transform=ax.transAxes)  # Initial mass is nitrogen molecule mass
pressure_annotation = ax.text2D(0.02, 0.85, "Pressure: {} Pa".format(101325), transform=ax.transAxes)
R_annotation = ax.text2D(0.02, 0.80, "Gas Constant: {} J/(mol*K)".format(8.314), transform=ax.transAxes)

# Random colors for particles
colors = np.random.choice(['r', 'g', 'b'], size=num_points)  # Randomly choose from 3 colors

# Generate masses based on particle colors
masses = generate_masses(num_points, colors)

# Threshold distance for drawing lines between molecules
threshold_distance = 0.1  

# Initialize dictionary to store line artists
lines = {}

# Update function for animation
def update(frame):
    global x_data, y_data, z_data, directions, colors, lines, masses
    
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
    
    x_data = np.clip(x_data, 0, width)
    y_data = np.clip(y_data, 0, height)
    z_data = np.clip(z_data, 0, depth)
    
    # Calculate pairwise distances between particles
    distances = squareform(pdist(np.column_stack((x_data, y_data, z_data))))
    
    # Draw or remove lines between close particles
    for i in range(num_points):
        for j in range(i+1, num_points):
            if distances[i, j] < threshold_distance:
                if (i, j) not in lines:
                    # Draw a line if it doesn't exist
                    lines[(i, j)] = ax.plot([x_data[i], x_data[j]], [y_data[i], y_data[j]], [z_data[i], z_data[j]], color='gray', alpha=0.5)[0]
                    print(f"""{colors[i]}[{x_data[i]}, {y_data[i]}, {z_data[i]}]
                           and {colors[j]}[{x_data[j]}, {y_data[j]}, {z_data[j]}] --- line""")
                # Check for particle color changes based on reactions
                if colors[i] == 'g' and colors[j] == 'r':
                    colors[i] = colors[j] = 'm'  # purple
                elif colors[i] == 'g' and colors[j] == 'b':
                    colors[i] = 'r'
                    colors[j] = 'm'  # purple
                elif colors[i] == 'r' and colors[j] == 'b':
                    colors[i] = 'g'
                    colors[j] = 'r'
                elif colors[i] == 'm' and colors[j] == 'm':
                    colors[i] = 'b'
                    colors[j] = 'g'
            else:
                if (i, j) in lines:
                    lines[(i, j)].remove()
                    del lines[(i, j)]
    
    scatter._offsets3d = (x_data, y_data, z_data)
    scatter.set_color(colors)
    
    # Calculate and display the average mass
    average_mass = np.mean(masses)
    mass_annotation.set_text("Average Mass: {} kg".format(average_mass))
    
    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_zlim(0, depth)

    return scatter, temperature_annotation, mass_annotation, pressure_annotation, R_annotation



# Create animation
ani = FuncAnimation(fig, update, frames=100, interval=100)
plt.show()
