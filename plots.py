import numpy as np
import matplotlib.pyplot as plt

# Define the solar system data
solar_system = {
    "Sun": {"radius": 6.96e8, "x": 0, "y": 0, "color": "yellow"},
    "Mercury": {"radius": 2.44e6, "orbit_radius": 5.79e7, "color": "gray"},
    "Venus": {"radius": 6.05e6, "orbit_radius": 1.08e8, "color": "orange"},
    "Earth": {"radius": 6.37e6, "orbit_radius": 1.5e8, "color": "blue"},
    "Mars": {"radius": 3.37e6, "orbit_radius": 2.28e8, "color": "red"},
    "Moon": {"radius": 1.74e6, "orbit_radius": 3.84e7, "color": "gray", "parent": "Earth"}
}

# Create a figure and axis
fig, ax = plt.subplots()

# Set the background color
ax.set_facecolor("black")

# Calculate the maximum orbit radius
max_orbit_radius = max([data["orbit_radius"] for data in solar_system.values() if data != solar_system["Sun"]])

# Plot the orbits around the Sun (excluding the Sun)
for planet, data in solar_system.items():
    if planet != "Sun" and planet != "Moon":
        orbit_radius = data["orbit_radius"]
        theta = np.linspace(0, 2 * np.pi, 100)  # Angle values for the orbit path
        x = data["orbit_radius"] * np.cos(theta)
        y = data["orbit_radius"] * np.sin(theta)
        ax.plot(x, y, color="gray", alpha=0.3)

# Plot the Sun
sun_data = solar_system["Sun"]
sun_radius = sun_data["radius"]
sun_x = sun_data["x"]
sun_y = sun_data["y"]
sun_color = sun_data["color"]
circle = plt.Circle((sun_x, sun_y), sun_radius * 0.01, color=sun_color)  # Adjust scaling factor for Sun's radius
ax.add_patch(circle)
ax.annotate("Sun", (sun_x, sun_y + sun_radius * 0.02), color="white", ha="center", va="center")  # Adjust positioning

# Plot the planets
for planet, data in solar_system.items():
    if planet != "Sun" and planet != "Moon":
        radius = data["radius"]
        x = data["orbit_radius"] * np.cos(0)  # Start at angle 0 for x-coordinate
        y = data["orbit_radius"] * np.sin(0)  # Start at angle 0 for y-coordinate
        color = data["color"]
        circle = plt.Circle((x, y), radius, color=color)
        ax.add_patch(circle)
        ax.annotate(planet, (x, y + radius * 2.5), color="white", ha="center", va="center")


# Plot the Moon
moon_data = solar_system["Moon"]
moon_radius = moon_data["radius"]
moon_orbit_radius = moon_data["orbit_radius"]
moon_parent = moon_data["parent"]
moon_parent_data = solar_system[moon_parent]
moon_parent_x = moon_parent_data["orbit_radius"] * np.cos(0)  # Start at angle 0 for x-coordinate
moon_parent_y = moon_parent_data["orbit_radius"] * np.sin(0)  # Start at angle 0 for y-coordinate
moon_x = moon_parent_x + moon_orbit_radius * np.cos(0)  # Start at angle 0 for x-coordinate
moon_y = moon_parent_y + moon_orbit_radius * np.sin(0)  # Start at angle 0 for y-coordinate
moon_color = moon_data["color"]
circle = plt.Circle((moon_x, moon_y), moon_radius, color=moon_color)
ax.add_patch(circle)
ax.annotate("Moon", (moon_x, moon_y + moon_radius * 2.5), color="white", ha="center", va="center")

# Set the aspect ratio and axis limits
ax.set_aspect("equal")
ax.set_xlim([-max_orbit_radius * 1.2, max_orbit_radius * 1.2])  # Adjust the scaling factor for the axis limits
ax.set_ylim([-max_orbit_radius * 1.2, max_orbit_radius * 1.2])  # Adjust the scaling factor for the axis limits

# Set the title and labels
ax.set_title("Solar System Visualization")
ax.set_xlabel("X Coordinate (m)")
ax.set_ylabel("Y Coordinate (m)")

# Show the plot
plt.show()
