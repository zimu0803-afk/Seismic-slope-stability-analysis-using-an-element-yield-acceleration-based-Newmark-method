import os
import ezdxf
from shapely.geometry import Polygon, box, MultiPolygon, GeometryCollection, LineString
import numpy as np
import pandas as pd

# Automatically create output directory
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

# Grid horizontal dimension
chicun = 1
# Define outer boundary polygon
boundary = Polygon([(0, 5), (50, 5), (50, 30), (30, 30), (15, 15), (0, 15), (0, 5)])
ro = 1  # Unit weight / density

# Create DXF document
doc = ezdxf.new('R2010')
msp = doc.modelspace()

# Define grid size and dimensions
grid_x = np.arange(0, 60, 1)  # Grid interval = 1 unit
grid_y = np.arange(0, 40, 1)

data = []
dataM = []

# Generate grid cells and compute intersection with boundary
for x1, x2 in zip(grid_x[:-1], grid_x[1:]):
    for y1, y2 in zip(grid_y[:-1], grid_y[1:]):
        grid_cell = box(x1, y1, x2, y2)
        intersection = boundary.intersection(grid_cell)

        if not intersection.is_empty:
            if isinstance(intersection, Polygon):
                msp.add_lwpolyline(list(intersection.exterior.coords), dxfattribs={'layer': 'GridToBoundary'})
                area = intersection.area * ro
                centroid = intersection.centroid
                data.append([area, centroid.x, centroid.y])
                dataM.append([area, centroid.x, abs(centroid.y - 30)])
            elif isinstance(intersection, MultiPolygon):
                for poly in intersection.geoms:
                    msp.add_lwpolyline(list(poly.exterior.coords), dxfattribs={'layer': 'GridToBoundary'})
                    area = poly.area * ro
                    centroid = poly.centroid
                    data.append([area, centroid.x, centroid.y])
                    dataM.append([area, centroid.x, abs(centroid.y - 30)])
            elif isinstance(intersection, LineString):
                msp.add_lwpolyline(list(intersection.coords), dxfattribs={'layer': 'GridToBoundary'})
            elif isinstance(intersection, GeometryCollection):
                for geom in intersection.geoms:
                    if isinstance(geom, Polygon):
                        msp.add_lwpolyline(list(geom.exterior.coords), dxfattribs={'layer': 'GridToBoundary'})
                        area = geom.area * ro
                        centroid = geom.centroid
                        data.append([area, centroid.x, centroid.y])
                        dataM.append([area, centroid.x, abs(centroid.y - 30)])
                    elif isinstance(geom, LineString):
                        msp.add_lwpolyline(list(geom.coords), dxfattribs={'layer': 'GridToBoundary'})

# Save results to Excel files (relative paths)
df = pd.DataFrame(data, columns=['M', 'X', 'Y'])
df.to_excel(os.path.join(output_dir, f'{chicun}_grid.xlsx'), index=False)

df = pd.DataFrame(dataM, columns=['M', 'X', 'Y'])
df.to_excel(os.path.join(output_dir, f'converted_seismic_force_{chicun}_grid.xlsx'), index=False)

# Save DXF geometry file
doc.saveas(os.path.join(output_dir, f'modified_{chicun}_grid_CAD.dxf'))
print("Grid generation completed successfully. Output files saved in ./output directory.")