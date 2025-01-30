import numpy as np
import matplotlib.pyplot as plt

def plot_double_star_three_datasets_XY(
    # ------------------------------------
    # Historical data (X, Y, Dates)
    # ------------------------------------
    hist_x,    # array-like (N)
    hist_y,    # array-like (N)
    hist_dates,# array-like (N) => for color-coding
    # ------------------------------------
    # Gaia data (X, Y)
    # ------------------------------------
    gaia_x=None,  # array-like or None
    gaia_y=None,  # array-like or None
    # ------------------------------------
    # LCO data (X, Y) - averaged
    # ------------------------------------
    lco_x=None,   # array-like or None
    lco_y=None,   # array-like or None
    # ------------------------------------
    # Plot labels
    # ------------------------------------
    gaia_label="Gaia DR3 measurement",
    lco_label="LCO measurement (average)"
):
    """
    Plots three separate data sets for a double-star system, with
    the (X, Y) positions already computed.

    1) Historical data: color-coded by observation date (hist_dates).
    2) Gaia data: red circles (gaia_x, gaia_y).
    3) LCO data: multiple points (lco_x, lco_y) averaged into one green “X”.

    The axes are forced to have the same numeric
    range and aspect ratio = 1:1.

    Parameters
    ----------
    hist_x : array-like
        X-coordinates for historical measurements.
    hist_y : array-like
        Y-coordinates for historical measurements (same length as hist_x).
    hist_dates : array-like
        Observation years for historical measurements (same length as hist_x).
    gaia_x : array-like or None
        X-coordinates for Gaia measurements (if multiple points, same length as gaia_y).
    gaia_y : array-like or None
        Y-coordinates for Gaia measurements.
    lco_x : array-like or None
        X-coordinates for LCO measurements (if multiple points, same length as lco_y).
    lco_y : array-like or None
        Y-coordinates for LCO measurements.
    gaia_label : str
        Legend label for Gaia points (default "Gaia DR3 measurement").
    lco_label : str
        Legend label for the single averaged LCO point (default "LCO measurement (average)").
    """

    # -----------------------------
    # 1) Historical Data
    # -----------------------------
    hist_x = np.asarray(hist_x)
    hist_y = np.asarray(hist_y)
    hist_dates = np.asarray(hist_dates)

    # 1.1) Check array sizes
    if not (len(hist_x) == len(hist_y) == len(hist_dates)):
        raise ValueError("Historical x, y, and dates must have the same length.")

    # -----------------------------
    # 2) Gaia Data
    # -----------------------------
    if gaia_x is not None and gaia_y is not None:
        gaia_x = np.asarray(gaia_x)
        gaia_y = np.asarray(gaia_y)
        if len(gaia_x) != len(gaia_y):
            raise ValueError("Gaia x and y arrays must have the same length.")
    else:
        gaia_x = np.array([])
        gaia_y = np.array([])

    # -----------------------------
    # 3) LCO Data => Average
    # -----------------------------
    if lco_x is not None and lco_y is not None and len(lco_x) > 0:
        lco_x = np.asarray(lco_x)
        lco_y = np.asarray(lco_y)
        if len(lco_x) != len(lco_y):
            raise ValueError("LCO x and y arrays must have the same length.")

        # Average the LCO data
        lco_x_mean = lco_x.mean()
        lco_y_mean = lco_y.mean()
    else:
        lco_x = np.array([])
        lco_y = np.array([])
        lco_x_mean = np.nan
        lco_y_mean = np.nan

    # -----------------------------
    # 4) Create the Figure
    # -----------------------------
    fig, ax = plt.subplots(figsize=(6,6))

    # 4.1) Plot historical data color‐coded by date
    sc = ax.scatter(
        hist_x, hist_y,
        c=hist_dates,
        cmap='plasma_r',  # reversed => newer = darker
        s=50,
        edgecolor='black'
    )
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Historical Observation Year")

    # 4.2) Plot Gaia data in red circles
    if gaia_x.size > 0:
        ax.scatter(
            gaia_x, gaia_y,
            c='red', marker='o',
            s=80, edgecolor='k', linewidth=1,
            label=gaia_label
        )

    # 4.3) Plot the AVERAGE LCO data as a single green “X”
    if not np.isnan(lco_x_mean):
        ax.scatter(
            [lco_x_mean], [lco_y_mean],
            marker='x', s=100, linewidths=2,
            c='green',
            label=lco_label
        )

    # -----------------------------
    # 5) Force same numeric range for X & Y
    # -----------------------------
    # Combine all data
    all_x = np.concatenate([hist_x, gaia_x, lco_x])
    all_y = np.concatenate([hist_y, gaia_y, lco_y])

    x_min, x_max = all_x.min(), all_x.max()
    y_min, y_max = all_y.min(), all_y.max()

    data_width = x_max - x_min
    data_height = y_max - y_min
    plot_range = max(data_width, data_height)

    # Add ~10% margin
    margin_factor = 0.1
    plot_range *= (1 + margin_factor)

    # Center around midpoint
    x_mid = 0.5 * (x_min + x_max)
    y_mid = 0.5 * (y_min + y_max)

    ax.set_xlim(x_mid - plot_range/2, x_mid + plot_range/2)
    ax.set_ylim(y_mid - plot_range/2, y_mid + plot_range/2)

    # Keep aspect ratio 1:1
    ax.set_aspect('equal', adjustable='box')

    # -----------------------------
    # 6) Final Labels & Show
    # -----------------------------
    ax.set_xlabel("Relative X (arcseconds of RA)")
    ax.set_ylabel("Relative Y (arcseconds of Dec)")
    ax.set_title("HJ 2532 Measurements")
    ax.legend(loc='upper right')

    plt.show()


# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":

    # HISTORICAL DATA (x, y, date)
    hist_x_example = np.array([11.49386994, 13.26094389, 11.91155053, 12.22493754, 12.46425923,
        12.39392056, 12.26163779, 12.31302846, 11.41999261, 11.73327006,
        12.12961438, 11.87187046, 12.41105884, 12.05339011, 12.26047285,
        12.24090278, 12.22725804, 12.07329955, 12.53404073, 12.21847153,
        12.21565859, 12.22456578, 12.22789811, 12.22041109, 12.22066141])
    hist_y_example = np.array([-3.448326238, -4.488581868, -4.28842207, -4.595051928, -4.809557356,
        -4.907100287, -5.382482677, -4.530312371, -4.706981289, -4.860079591,
        -5.024250784, -4.533426495, -4.838869641, -4.869885714, -4.510975672,
        -4.552350938, -4.52300009, -4.370473425, -4.537259404, -4.529449681,
        -4.52840691, -4.519093771, -4.518385088, -4.52628754, -4.525410075
        ])
    hist_dates_example = np.array([1831.19, 1832.1, 1874.17, 1906.17, 1910.872, 1911.31, 1923.5, 1925.34,
        1928.28, 1928.74, 1929.2, 1930.08, 1958.27, 1979.999, 1991.86, 1998.26,
        2002.121, 2006.059, 2008.035, 2013.159, 2014.114, 2015, 2015.157, 2015.5,
        2016])

    # GAIA DATA (x, y)
    gaia_x_example = np.array([12.2165])
    gaia_y_example = np.array([-4.52336])

    # LCO DATA (x, y) => if there are multiple points, we'll average them
    lco_x_example = np.array([12.22021293

    ])
    lco_y_example = np.array([-4.526563409
    ])

    # Call the function
    plot_double_star_three_datasets_XY(
        hist_x_example, hist_y_example, hist_dates_example,
        gaia_x=gaia_x_example, gaia_y=gaia_y_example,
        lco_x=lco_x_example,  lco_y=lco_y_example,
        gaia_label="Gaia DR3 measurement",
        lco_label="2025.04 LCO (avg)"
    )
