# Double Star Plot Scripts

**Author**: Xinyue Wang, Stanford University Online High School

These Python scripts help astronomers plot data for double star systems, including historical, Gaia, LCO (Las Cumbres Observatory) measurements, and optional predictive data (e.g., from other research). All scripts force a **square** plot (1:1 aspect ratio) to avoid visual distortion.

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Scripts](#scripts)
   - [Script 1: `plot_double_star_three_datasets_average_lco`](#script-1-plot_double_star_three_datasets_average_lco)
   - [Script 2: `plot_double_star_three_datasets_XY`](#script-2-plot_double_star_three_datasets_xy)
   - [Script 3: `plot_double_star_with_prediction`](#script-3-plot_double_star_with_prediction)
5. [Examples](#examples)
6. [License](#license)

---

## Overview

Many double star projects gather data from multiple sources:

- **Historical observations**: Typically spanning decades or centuries, measured in either polar coordinates \((\text{PA}, \text{Sep})\) or \((X, Y)\).  
- **Gaia DR3**: High-precision astrometric data (often \(\text{PA}, \text{Sep}\), or you might convert to \((X, Y)\)).  
- **LCO measurements**: Modern measurements you make with a telescope network like Las Cumbres Observatory.  
- **Predictions / Theoretical points**: Single coordinates from orbit fits (e.g., Izmailov 2019).

These scripts streamline plotting such data in Python, ensuring:

1. **One color-coded scatter** for historical data (based on date).  
2. **Separate styling** for Gaia.  
3. **Averaging** of multiple LCO points into one marker (green “X”).  
4. **Optional** predicted or theoretical data, plotted as a distinct color/marker (light-blue “X”).  
5. An **un-distorted** plot with the same numeric range on X and Y axes.

---

## Installation

1. Clone or download this repository.  
2. Make sure you have Python 3.7+ (recommended) and the following packages:
   ```bash
   pip install numpy matplotlib
3. Run each script with python scriptname.py or import the functions into your own Python scripts/notebooks.
   
---

## Usage
You can import any of these functions into your Python code or just run the `.py` files directly.

Historical data can be either:
- **In polar form** `(PA, Sep)`  
  → Use **Script 1**.
- **Already in Cartesian form** `(X, Y)`  
  → Use **Script 2** or **Script 3** (if you need a prediction).

Gaia data can be provided in the same coordinate system (polar or Cartesian), or left out entirely (pass `None`).

LCO data is always averaged to a single point.

Predicted data is optional—only used in **Script 3**.

---

## Scripts

### Script 1: `plot_double_star_three_datasets_average_lco`

**Location:** `script_1_plot_double_star_three_datasets_average_lco.py`

### Signature

```python
plot_double_star_three_datasets_average_lco(
    hist_dates, hist_PAs, hist_Seps,
    gaia_PAs=None, gaia_Seps=None,
    lco_PAs=None, lco_Seps=None,
    gaia_label="Gaia DR3 measurement",
    lco_label="[TIME] LCO measurement (average)"
)
```

### Purpose
When your historical, Gaia, and LCO measurements are all in polar coordinates `(PA, Sep)`, this function:

**Functionality**
- Converts all polar data to `(X, Y)` under the sign convention:

  ![x = \text{Sep} \cdot \sin(\text{PA})](https://latex.codecogs.com/svg.latex?x%20%3D%20\text{Sep}%20\cdot%20\sin(\text{PA}))  

  ![y = -\text{Sep} \cdot \cos(\text{PA})](https://latex.codecogs.com/svg.latex?y%20%3D%20-\text{Sep}%20\cdot%20\cos(\text{PA}))  

  where **PA** is in degrees from **North = 0°** toward **East = 90°**.

**Plots**
- **Historical data** color-coded by date (older = lighter, newer = darker).
- **Gaia data** represented by **red circles**.
- **LCO data** represented by **one green “X”** for the average of all LCO points.
- Enforces **the same numeric range** for both axes to maintain a square plot.

---

### Script 2: `plot_double_star_three_datasets_XY`

**Location:** `script_2_plot_double_star_three_datasets_XY.py`

### Signature

```python
plot_double_star_three_datasets_XY(
    hist_x, hist_y, hist_dates,
    gaia_x=None, gaia_y=None,
    lco_x=None, lco_y=None,
    gaia_label="Gaia DR3 measurement",
    lco_label="LCO measurement (average)"
)
```

### Purpose

When you already have (X, Y) for historical, Gaia, and LCO data, this function:

- **Does not convert from polar coords; it just plots what you give it.**
- **Averages LCO data to one green “X.”**
- **Color‐codes historical data by date.**
- **Applies a 10% margin around data and fixes a 1:1 aspect ratio.**

---

### Script 3: `plot_double_star_with_prediction`
**Location:** `script_3_plot_double_star_with_prediction.py`

### Signature
```python
plot_double_star_with_prediction(
    hist_x, hist_y, hist_dates,
    gaia_x=None, gaia_y=None,
    gaia_label="Gaia DR3 measurement",
    lco_x=None, lco_y=None,
    lco_label="LCO measurement (average)",
    pred_x=None, pred_y=None,
    pred_label="Prediction"
)
```

### Purpose
When you have `(X, Y)` coordinates for **historical data, Gaia, LCO**, and an additional **predicted point** (e.g., an orbital solution or future position), this function:

- **Plots historical data** color-coded by date.
- **Plots Gaia data** as **red circles**.
- **Averages LCO data** to **one green “X”**.
- **Plots the predicted point** as a **single light-blue “X”**.
- Ensures a **1:1 aspect ratio** and **removes the bounding box** for clarity.

---

### Examples

Each script includes an `if __name__ == "__main__":` block demonstrating usage with example data. You can run these samples directly:

```bash
python script_1_plot_double_star_three_datasets_average_lco.py
```
...and a window will pop up with a sample plot.

Or **import** the functions in your own code:
```python
from script_1_plot_double_star_three_datasets_average_lco import plot_double_star_three_datasets_average_lco

# Some arrays for your data
hist_dates = [...]
hist_PAs = [...]
hist_Seps = [...]
...

plot_double_star_three_datasets_average_lco(
    hist_dates, hist_PAs, hist_Seps,
    ...
)

```

### Customize Plot Appearance

- **Labels:**  
  - `gaia_label`, `lco_label`, `pred_label` can be modified to reflect the time or data source.

- **Color Map:**  
  - By default, the script uses `plasma_r` (a reversed “plasma” colormap). You can substitute it with your preferred colormap.

- **Title:**  
  - Modify `ax.set_title(...)` to customize the plot title.

- **Axis Labels:**  
  - Change `ax.set_xlabel(...)` and `ax.set_ylabel(...)` to adjust axis descriptions as needed.
 
---

## License

**MIT License © Xinyue Wang, Stanford University**  

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

See the [MIT License](https://github.com/xinyue0221/double-star-plot-scripts?tab=MIT-1-ov-file) for the full text.

