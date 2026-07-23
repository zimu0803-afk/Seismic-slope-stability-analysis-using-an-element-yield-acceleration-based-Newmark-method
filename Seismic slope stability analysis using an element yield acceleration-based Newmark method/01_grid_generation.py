import os
import ezdxf
from shapely.geometry import Polygon, box, MultiPolygon, GeometryCollection, LineString
import numpy as np
import pandas as pd

# 自动创建输出文件夹
output_dir = "./output"
os.makedirs(output_dir, exist_ok=True)

# 输入网格的横向尺寸
chicun = 1
# 定义外边界矩形
boundary = Polygon([(0, 5), (50, 5), (50, 30), (30, 30), (15, 15), (0, 15), (0, 5)])
ro = 1  # 容重

# 创建 DXF 文件
doc = ezdxf.new('R2010')
msp = doc.modelspace()

# 定义网格尺寸和范围
grid_x = np.arange(0, 60, 1)  # 每 1 个单位生成一个网格
grid_y = np.arange(0, 40, 1)

data = []
dataM = []

# 生成网格并连接到外边界
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

# 保存到 Excel (相对路径)
df = pd.DataFrame(data, columns=['M', 'X', 'Y'])
df.to_excel(os.path.join(output_dir, f'{chicun}_grid.xlsx'), index=False)

df = pd.DataFrame(dataM, columns=['M', 'X', 'Y'])
df.to_excel(os.path.join(output_dir, f'converted_seismic_force_{chicun}_grid.xlsx'), index=False)

# 保存 DXF 文件
doc.saveas(os.path.join(output_dir, f'modified_{chicun}_grid_CAD.dxf'))
print("网格已成功生成，并已保存至 ./output 目录下。")