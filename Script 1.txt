import numpy as np
import matplotlib.pyplot as plt

def plot_double_star_three_datasets_average_lco(
    # --------------------------------
    # Historical data
    # --------------------------------
    hist_dates,   # array-like (N)
    hist_PAs,     # array-like (N)
    hist_Seps,    # array-like (N)
    # --------------------------------
    # Gaia data
    # --------------------------------
    gaia_PAs=None,    # array-like or None
    gaia_Seps=None,   # array-like or None
    # --------------------------------
    # LCO data (AVERAGED)
    # --------------------------------
    lco_PAs=None,     # array-like or None
    lco_Seps=None,    # array-like or None
    # --------------------------------
    # Plot labels
    # --------------------------------
    gaia_label="Gaia DR3 measurement",
    lco_label="[TIME] LCO measurement (average)"
):
    """
    Plots three separate data sets for a double-star system:

    1) Historical data: color-coded by date.
    2) Gaia data: separate array, single color (red).
    3) LCO data: averaged into a single (X, Y) point with a green 'X'.

    Sign convention:
        x = Sep * sin(PA)
        y = -Sep * cos(PA)
    with PA in degrees from North (0°) to East (90°).

    Parameters
    ----------
    hist_dates : array-like
        Observation years for historical measurements.
    hist_PAs : array-like
        Position angles (degrees) for historical measurements (same length as hist_dates).
    hist_Seps : array-like
        Separations (arcseconds) for historical measurements (same length as hist_dates).
    gaia_PAs : array-like or None
        Position angles (degrees) for Gaia points.
    gaia_Seps : array-like or None
        Separations (arcseconds) for Gaia points (same length as gaia_PAs).
    lco_PAs : array-like or None
        Position angles (degrees) for LCO data.
    lco_Seps : array-like or None
        Separations (arcseconds) for LCO data (same length as lco_PAs).
    gaia_label : str
        Legend label for Gaia points (default: "Gaia DR3 measurement")
    lco_label : str
        Legend label for the single averaged LCO point (default: "LCO measurement (average)")
    """

    # -----------------------------
    # 1) Convert Historical (PA, Sep) => (X, Y)
    # -----------------------------
    hist_PAs_rad = np.radians(hist_PAs)
    hist_X = hist_Seps * np.sin(hist_PAs_rad)
    hist_Y = -hist_Seps * np.cos(hist_PAs_rad)

    # -----------------------------
    # 2) Gaia data => arrays of (X, Y) if present
    # -----------------------------
    if gaia_PAs is not None and gaia_Seps is not None:
        gaia_PAs_rad = np.radians(gaia_PAs)
        gaia_X_array = gaia_Seps * np.sin(gaia_PAs_rad)
        gaia_Y_array = -gaia_Seps * np.cos(gaia_PAs_rad)
    else:
        gaia_X_array = np.array([])
        gaia_Y_array = np.array([])

    # -----------------------------
    # 3) LCO data => average (X, Y) if present
    # -----------------------------
    if lco_PAs is not None and lco_Seps is not None and len(lco_PAs) > 0:
        lco_PAs_rad = np.radians(lco_PAs)
        lco_X_array = lco_Seps * np.sin(lco_PAs_rad)
        lco_Y_array = -lco_Seps * np.cos(lco_PAs_rad)

        # Compute average of all LCO points
        lco_X = lco_X_array.mean()
        lco_Y = lco_Y_array.mean()
    else:
        # No LCO data
        lco_X_array = np.array([])
        lco_Y_array = np.array([])
        lco_X = np.nan
        lco_Y = np.nan

    # -----------------------------
    # 4) Create the Figure
    # -----------------------------
    fig, ax = plt.subplots(figsize=(6, 6))

    # 4.1) Plot Historical data color‐coded by date
    sc = ax.scatter(
        hist_X, hist_Y,
        c=hist_dates,
        cmap='plasma_r',   # reversed “plasma” => older = lighter, newer = darker
        s=50,
        edgecolors='black'
    )
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Historical Observation Year")

    # 4.2) Plot Gaia data in red (if any)
    if gaia_X_array.size > 0:
        ax.scatter(
            gaia_X_array, gaia_Y_array,
            c='red', marker='o',
            s=80, edgecolor='k', linewidth=1,
            label=gaia_label
        )

    # 4.3) Plot the AVERAGE LCO data as a single green X
    #     (only if we actually have LCO data)
    if not np.isnan(lco_X):
        ax.scatter(
            [lco_X], [lco_Y],
            marker='x', s=100, linewidths=2,
            c='green',
            label=lco_label
        )

    # -----------------------------
    # 5) Force same numeric range for X & Y
    # -----------------------------
    # Combine all X & Y from historical + Gaia + LCO arrays
    all_X = np.concatenate([hist_X, gaia_X_array, lco_X_array]) if lco_X_array.size else np.concatenate([hist_X, gaia_X_array])
    all_Y = np.concatenate([hist_Y, gaia_Y_array, lco_Y_array]) if lco_Y_array.size else np.concatenate([hist_Y, gaia_Y_array])

    x_min, x_max = all_X.min(), all_X.max()
    y_min, y_max = all_Y.min(), all_Y.max()

    data_width = x_max - x_min
    data_height = y_max - y_min
    plot_range = max(data_width, data_height)

    # 10% margin
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
    ax.set_title("HLD 75 Measurements\nExample Double Star Plot")   # add "\n" if you want to start a new line
    ax.legend(loc='upper right')

    plt.show()


# ----------------------------------------------------------------------
# Example usage
# ----------------------------------------------------------------------
if __name__ == "__main__":

    # 1) Example Historical data (with or without the outlier if any)
    hist_dates_example = np.array([
        1888.326, 1896.1, 1896.1,
        1908.987, 1909.756, 1913.05,1933.13,
        1991.71,  1999.77,  1999.95,2008.86,
        2014.049, 2014.846, 2016.0, 2017.157,
        2018.975
    ])

    hist_PAs_example = np.array([
        89.8,  90.6,  90.4,
        87.2,   87.4,  88.4,  87.6,
        88.5,   89.4,  89.4,  88.1,
        89.12,  89.63, 89.16, 89.1,
        89.1
    ])

    hist_Seps_example = np.array([
        6.27,  6.50,  6.538,
        6.29,  6.40,  6.48,  6.47,
        6.329, 6.26,  6.302, 6.42,
        6.26,  6.224, 6.27191, 6.235,
        6.248
    ])

    # 2) Gaia data (could be multiple points)
    gaia_PAs_example = np.array([89.161])
    gaia_Seps_example = np.array([6.272])

    # 3) LCO data (multiple points, but we want an AVERAGE)
    lco_PAs_example = np.array([
        89.207, 89.14,  89.099, 89.06,  89.081,
        89.049, 88.994, 89.219, 89.108, 89.116,
        89.134
    ])
    lco_Seps_example = np.array([
        6.27,   6.258, 6.258,  6.258,  6.306,
        6.294,  6.27,  6.27,   6.264,  6.27,
        6.264
    ])

    # 4) Call the plotting function
    plot_double_star_three_datasets_average_lco(
        hist_dates_example,
        hist_PAs_example,
        hist_Seps_example,
        gaia_PAs=gaia_PAs_example,
        gaia_Seps=gaia_Seps_example,
        lco_PAs=lco_PAs_example,
        lco_Seps=lco_Seps_example,
        gaia_label="Gaia DR3 measurement",
        lco_label="2024.019 LCO (avg)"   # change it to the corresponding time/year for your LCO measurement
    )
