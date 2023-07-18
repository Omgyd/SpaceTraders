import numpy as np
import matplotlib.pyplot as plt

# Define the solar system data with x, y coordinates and orbit radii
solar_system = {
    "Sun": {"radius": 6.96e8, "x": 0, "y": 0, "color": "yellow"},
    "Mercury": {"radius": 2.44e6, "x": 5.79e7, "y": 0, "color": "gray", "orbit_radius": 5.79e7},
    "Venus": {"radius": 6.05e6, "x": 1.08e8, "y": 0, "color": "orange", "orbit_radius": 1.08e8},
    "Earth": {"radius": 6.37e6, "x": 1.5e8, "y": 0, "color": "blue", "orbit_radius": 1.5e8},
    "Mars": {"radius": 3.37e6, "x": 2.28e8, "y": 0, "color": "red", "orbit_radius": 2.28e8},
    "Moon": {"radius": 1.74e6, "x": 1.5e8 + 3.84e7, "y": 0, "color": "gray", "orbit_radius": 3.84e7}
}

# Create a figure and axis
fig, ax = plt.subplots()

# Set the background color
ax.set_facecolor("black")

# Plot the orbits around the Sun
for planet, data in solar_system.items():
    if planet != "Sun" and planet != "Moon":
        orbit_radius = data["orbit_radius"]
        theta = np.linspace(0, 2 * np.pi, 100)  # Angle values for the orbit path
        x = orbit_radius * np.cos(theta)
        y = orbit_radius * np.sin(theta)
        ax.plot(x, y, color="gray", alpha=0.3)

# Plot the Sun
sun_data = solar_system["Sun"]
sun_radius = sun_data["radius"]
sun_x = sun_data["x"]
sun_y = sun_data["y"]
sun_color = sun_data["color"]
circle = plt.Circle((sun_x, sun_y), sun_radius * 0.01, color=sun_color)
ax.add_patch(circle)
ax.annotate("Sun", (sun_x, sun_y + sun_radius * 0.02), color="white", ha="center", va="center")

# Plot the planets
for planet, data in solar_system.items():
    if planet != "Sun":
        radius = data["radius"]
        x = data["x"]
        y = data["y"]
        color = data["color"]
        circle = plt.Circle((x, y), radius, color=color)
        ax.add_patch(circle)
        ax.annotate(planet, (x, y + radius * 2.5), color="white", ha="center", va="center")

# Set the aspect ratio and axis limits
ax.set_aspect("equal")
ax.set_xlim([-3e8, 3e8])
ax.set_ylim([-3e8, 3e8])

# Set the title and labels
ax.set_title("Solar System Visualization")
ax.set_xlabel("X Coordinate (m)")
ax.set_ylabel("Y Coordinate (m)")

# Show the plot
plt.show()
