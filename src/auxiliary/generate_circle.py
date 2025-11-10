import numpy as np
import random

def generate_circle(center_x, center_y, radius, num_points=120):
    # generate angles from 0 to 2pi but excluding the endpoint to avoid duplicate point
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)

    # generate x, y coordinates
    x = center_x + radius * np.cos(angles)
    y = center_y + radius * np.sin(angles)

    return np.column_stack((x, y))

def generate_two_circles(plane_size=500, min_radius=20, max_radius=200, num_points=120):
    # generate random radius (same for both circles)
    radius = random.uniform(min_radius, max_radius)

    # ensure circles fit within the plane by constraining center positions
    min_center = radius
    max_center = plane_size - radius

    # generate random centers for both circles
    center1_x = random.uniform(min_center, max_center)
    center1_y = random.uniform(min_center, max_center)

    center2_x = random.uniform(min_center, max_center)
    center2_y = random.uniform(min_center, max_center)

    # generate circles from above constraints
    circle1 = generate_circle(center1_x, center1_y, radius, num_points)
    circle2 = generate_circle(center2_x, center2_y, radius, num_points)

    return circle1, circle2, radius

def save_circles(circle1, circle2, filename="data/2circles.txt"):
    with open(filename, 'w') as f:
        for point in circle1:
            f.write(f"     {point[0]:.7e}      {point[1]:.7e}\n")
        for point in circle2:
            f.write(f"     {point[0]:.7e}      {point[1]:.7e}\n")

    print(f"Both circles saved to {filename}")

# generate two circles
circle1, circle2, radius = generate_two_circles(plane_size=500, num_points=120)

# calculate actual radii from generated points to verify
center1 = circle1.mean(axis=0)
center2 = circle2.mean(axis=0)
actual_radius1 = np.mean(np.sqrt((circle1[:, 0] - center1[0])**2 + (circle1[:, 1] - center1[1])**2))
actual_radius2 = np.mean(np.sqrt((circle2[:, 0] - center2[0])**2 + (circle2[:, 1] - center2[1])**2))

save_circles(circle1, circle2)