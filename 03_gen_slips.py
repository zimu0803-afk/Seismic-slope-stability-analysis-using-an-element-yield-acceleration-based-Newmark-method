import math
import random
import numpy as np
import os
from openpyxl import Workbook

output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

slope_polygon = [(0, 0), (60, 0), (60, 20), (30, 20), (20, 10), (0, 10)]
polygon_edges = [(slope_polygon[i], slope_polygon[(i + 1) % len(slope_polygon)])
                 for i in range(len(slope_polygon))]
upper_edges = [
    ((60, 20), (30, 20)),
    ((30, 20), (20, 10)),
    ((20, 10), (0, 10))
]

def is_point_in_polygon(x, y, tolerance=1e-4):
    n = len(slope_polygon)
    inside = False
    for i in range(n):
        (x1, y1), (x2, y2) = slope_polygon[i], slope_polygon[(i + 1) % n]
        cross_product = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
        if abs(cross_product) < tolerance:
            x_in_range = (min(x1, x2) - tolerance <= x <= max(x1, x2) + tolerance)
            y_in_range = (min(y1, y2) - tolerance <= y <= max(y1, y2) + tolerance)
            if x_in_range and y_in_range:
                return True
        if (y1 > y) != (y2 > y):
            with np.errstate(divide='ignore'):
                xinters = (y - y1) * (x2 - x1) / (y2 - y1 + 1e-9) + x1
            if x <= xinters + tolerance:
                inside = not inside
    return inside

def line_segment_circle_intersection(x1, y1, x2, y2, cx, cy, r):
    dx = x2 - x1
    dy = y2 - y1
    a = dx ** 2 + dy ** 2
    b = 2 * (dx * (x1 - cx) + dy * (y1 - cy))
    c = (x1 - cx) ** 2 + (y1 - cy) ** 2 - r ** 2
    discriminant = b ** 2 - 4 * a * c
    intersections = []
    if discriminant >= 0:
        sqrt_d = math.sqrt(discriminant)
        t1 = (-b - sqrt_d) / (2 * a)
        t2 = (-b + sqrt_d) / (2 * a)
        for t in [t1, t2]:
            if 0 <= t <= 1:
                intersections.append((x1 + t * dx, y1 + t * dy))
    return intersections

def generate_valid_circle(max_attempts=5000):
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        xc = random.uniform(-5, 50)
        yc = random.uniform(5, 70)
        try:
            distances = [math.hypot(x - xc, y - yc) for x, y in slope_polygon]
            min_r = max(distances[2], distances[3], distances[4]) * 0.8
            max_r = min(1.8 * max(distances), 150)
            r = random.uniform(min_r, max_r)
        except:
            continue

        intersections = []
        for (x1, y1), (x2, y2) in polygon_edges:
            pts = line_segment_circle_intersection(x1, y1, x2, y2, xc, yc, r)
            intersections.extend(pts)

        upper_pts = []
        for pt in intersections:
            for (e1, e2) in upper_edges:
                x_min, x_max = min(e1[0], e2[0]) - 0.01, max(e1[0], e2[0]) + 0.01
                y_min, y_max = min(e1[1], e2[1]) - 0.01, max(e1[1], e2[1]) + 0.01
                if (x_min <= pt[0] <= x_max) and (y_min <= pt[1] <= y_max):
                    upper_pts.append(pt)
                    break

        unique_pts = []
        seen = set()
        for pt in upper_pts:
            key = (round(pt[0], 4), round(pt[1], 4))
            if key not in seen:
                seen.add(key)
                unique_pts.append(pt)

        if len(unique_pts) < 2:
            continue

        try:
            pt1, pt2 = sorted(unique_pts, key=lambda p: math.hypot(p[0] - xc, p[1] - yc))[:2]
        except:
            continue

        theta1 = math.atan2(pt1[1] - yc, pt1[0] - xc)
        theta2 = math.atan2(pt2[1] - yc, pt2[0] - xc)
        if theta2 < theta1:
            theta2 += 2 * math.pi

        points = [(xc + r * math.cos(theta), yc + r * math.sin(theta))
                  for theta in np.linspace(theta1, theta2, 30)]
        points[0], points[-1] = pt1, pt2

        valid_count = sum(1 for x, y in points if is_point_in_polygon(x, y) or any(
            abs((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)) < 1e-4 for (x1, y1), (x2, y2) in polygon_edges))

        if valid_count >= 28:
            return (xc, yc, r, pt1, pt2)

    raise RuntimeError(f"Failed to generate valid circle within {max_attempts} attempts.")

def generate_sliding_surfaces(N):
    surfaces = []
    for slip_id in range(1, N + 1):
        success = False
        while not success:
            try:
                xc, yc, r, pt1, pt2 = generate_valid_circle()
                success = True
            except RuntimeError:
                continue

        theta1 = math.atan2(pt1[1] - yc, pt1[0] - xc)
        theta2 = math.atan2(pt2[1] - yc, pt2[0] - xc)
        if theta2 < theta1:
            theta2 += 2 * math.pi

        points = [(xc + r * math.cos(theta), yc + r * math.sin(theta))
                  for theta in np.linspace(theta1, theta2, 30)]
        points[0], points[-1] = pt1, pt2

        surfaces.append({"slip_id": slip_id, "center": (xc, yc), "radius": r, "points": points})
    return surfaces

def save_to_excels(surfaces, circle_path, points_path):
    wb_circle = Workbook()
    ws_circle = wb_circle.active
    ws_circle.append(["FullySpecifiedSlips ID", "X", "Y", "r"])

    wb_points = Workbook()
    ws_points = wb_points.active
    ws_points.append(["FullySpecifiedSlips ID", "Point ID", "X", "Y"])

    point_counter = 1
    for surface in surfaces:
        ws_circle.append([surface["slip_id"], round(surface["center"][0], 10), round(surface["center"][1], 10), round(surface["radius"], 10)])
        for x, y in surface["points"]:
            ws_points.append([surface["slip_id"], point_counter, round(x, 10), round(y, 10)])
            point_counter += 1

    wb_circle.save(circle_path)
    wb_points.save(points_path)

if __name__ == "__main__":
    N = 5
    circle_path = os.path.join(output_dir, "circle_centers.xlsx")
    points_path = os.path.join(output_dir, "point_coordinates.xlsx")

    surfaces = generate_sliding_surfaces(N)
    save_to_excels(surfaces, circle_path, points_path)
    print(f"Random slip surfaces generated successfully:\n- {circle_path}\n- {points_path}")