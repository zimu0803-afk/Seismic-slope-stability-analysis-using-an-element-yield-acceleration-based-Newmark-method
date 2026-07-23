Markdown

```
# Seismic Slope Stability Analysis Using an Element Yield Acceleration-Based Newmark Method

This repository contains the official Python implementation for the research paper:

> **Seismic slope stability analysis using an element yield acceleration-based Newmark method**

---

## 📌 Abstract & Overview

This project provides an automated and integrated workflow for evaluating seismic slope stability by combining geometric meshing, circle arc slip surface generation, automated GeoStudio (SLOPE/W) batch interaction, element-wise yield acceleration mapping, and permanent seismic displacement integration.

The workflow consists of 7 sequential Python scripts:

1. **`01_grid_generation.py`**: Generates 2D mesh, exports CAD (.dxf) geometries, and computes grid centroids and masses.
2. **`02_get_slip_points.py`**: Batch extracts slip surface point coordinates from GeoStudio simulation output files.
3. **`03_gen_slips.py`**: Generates random circular slip surfaces bounded by the slope geometry.
4. **`04_calc_yield_acc.py`**: Implements a bisection search algorithm interfacing with GeoStudio to calculate critical yield acceleration ($k_y$) corresponding to Factor of Safety (FoS) = 1.0.
5. **`05_export_slips.py`**: Extracts and exports slip surface centers and radii.
6. **`06_assign_yield_acc.py`**: Maps slip surfaces to mesh nodes and assigns element-wise yield acceleration ($a_y$).
7. **`07_calc_displacement.py`**: Computes permanent seismic displacements via double integration of acceleration time histories.

---

## 🛠️ Environment & Requirements

### Software Required
- **Python**: 3.8 or higher
- **GeoStudio (GeoSlope / SLOPE/W)**: Required for limit equilibrium analysis (used in `04_calc_yield_acc.py`).

### Dependencies
Install the required Python packages:

```bash
pip install numpy pandas shapely ezdxf openpyxl
```

## 📂 Project Structure

Plaintext

```
.
├── 01_grid_generation.py
├── 02_get_slip_points.py
├── 03_gen_slips.py
├── 04_calc_yield_acc.py
├── 05_export_slips.py
├── 06_assign_yield_acc.py
├── 07_calc_displacement.py
└── README.md
```

## 🚀 Execution Sequence

Run the scripts in order:

Bash

```
python 01_grid_generation.py
python 02_get_slip_points.py
python 03_gen_slips.py
python 04_calc_yield_acc.py
python 05_export_slips.py
python 06_assign_yield_acc.py
python 07_calc_displacement.py
```

*Note: Output files (Excel tables, CAD drawings, text logs) will automatically be saved to the `./output/` directory upon execution.*

## 📩 Contact & Citation

If you use this code in your research, please cite our paper:

- **Paper Title**: *Seismic slope stability analysis using an element yield acceleration-based Newmark method*
- **Contact**: jiakunliu770@gmail.com