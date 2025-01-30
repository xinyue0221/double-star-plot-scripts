import numpy as np
import matplotlib.pyplot as plt

def plot_double_star_with_prediction(
    # ------------------------------------
    # Historical data (X, Y, Dates)
    # ------------------------------------
    hist_x,          # array-like (N)
    hist_y,          # array-like (N)
    hist_dates,      # array-like (N) => for color-coding
    # ------------------------------------
    # Gaia data (X, Y)
    # ------------------------------------
    gaia_x=None,     # array-like or None
    gaia_y=None,     # array-like or None
    gaia_label="Gaia DR3 measurement",
    # ------------------------------------
    # LCO data (X, Y) - averaged
    # ------------------------------------
    lco_x=None,      # array-like or None
    lco_y=None,      # array-like or None
    lco_label="LCO measurement (average)",
    # ------------------------------------
    # Prediction data (X, Y) - single point
    # ------------------------------------
    pred_x=None,     # float or None
    pred_y=None,     # float or None
    pred_label="Prediction"
):
    """
    Plots four separate data sets for a double-star system, assuming
    the (X, Y) positions are already computed:

    1) Historical data: color-coded by observation date (hist_dates).
    2) Gaia data: red circles (gaia_x, gaia_y).
    3) LCO data: multiple points (lco_x, lco_y) averaged into one green "X".
    4) Prediction data: one light-blue "X" (pred_x, pred_y).

    No bounding box is drawn. Axes are forced to have the same numeric
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
    gaia_label : str
        Legend label for Gaia points (default "Gaia DR3 measurement").
    lco_x : array-like or None
        X-coordinates for LCO measurements (if multiple points, same length as lco_y).
    lco_y : array-like or None
        Y-coordinates for LCO measurements.
    lco_label : str
        Legend label for the single averaged LCO point (default "LCO measurement (average)").
    pred_x : float or None
        X-coordinate for one predicted data point.
    pred_y : float or None
        Y-coordinate for one predicted data point.
    pred_label : str
        Legend label for the predicted data point (default "Prediction").
    """

    # -----------------------------
    # 1) Historical Data
    # -----------------------------
    hist_x = np.asarray(hist_x)
    hist_y = np.asarray(hist_y)
    hist_dates = np.asarray(hist_dates)

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
    # 4) Prediction Data (Izmailov 2019)
    #     We'll assume it's just a single (X, Y) point.
    # -----------------------------
    if pred_x is not None and pred_y is not None:
        pred_x_val = float(pred_x)
        pred_y_val = float(pred_y)
        # We'll add these into the "all data" array for axis-limits calculation
    else:
        pred_x_val = np.nan
        pred_y_val = np.nan

    # -----------------------------
    # 5) Create the Figure
    # -----------------------------
    fig, ax = plt.subplots(figsize=(6,6))

    # 5.1) Plot historical data color‐coded by date
    sc = ax.scatter(
        hist_x, hist_y,
        c=hist_dates,
        cmap='plasma_r',  # reversed => newer = darker
        s=50,
        edgecolor='black'
    )
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Historical Observation Year")

    # 5.2) Plot Gaia data in red circles (if any)
    if gaia_x.size > 0:
        ax.scatter(
            gaia_x, gaia_y,
            c='red', marker='o',
            s=80, edgecolor='k', linewidth=1,
            label=gaia_label
        )

    # 5.3) Plot the AVERAGE LCO data as a single green “X” (if any)
    if not np.isnan(lco_x_mean):
        ax.scatter(
            [lco_x_mean], [lco_y_mean],
            marker='x', s=100, linewidths=2,
            c='green',
            label=lco_label
        )

    # 5.4) Plot the Prediction data as a light-blue “X”
    if not np.isnan(pred_x_val):
        ax.scatter(
            [pred_x_val], [pred_y_val],
            marker='x', s=120, linewidths=2,
            c='lightblue',
            label=pred_label
        )

    # -----------------------------
    # 6) Force same numeric range for X & Y
    # -----------------------------
    # Combine all X, Y from historical + Gaia + LCO arrays + pred
    all_x_arrays = [hist_x, gaia_x, lco_x]
    all_y_arrays = [hist_y, gaia_y, lco_y]

    # If pred_x_val is valid, we tack it on as an array
    if not np.isnan(pred_x_val):
        all_x_arrays.append(np.array([pred_x_val]))
        all_y_arrays.append(np.array([pred_y_val]))

    # Combine them
    all_x = np.concatenate(all_x_arrays) if len(all_x_arrays) > 0 else np.array([0])
    all_y = np.concatenate(all_y_arrays) if len(all_y_arrays) > 0 else np.array([0])

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
    # 7) Final Labels & Show
    # -----------------------------
    ax.set_xlabel("Relative X (arcseconds)")
    ax.set_ylabel("Relative Y (arcseconds)")
    ax.set_title("Double Star Plot\nWith Prediction")
    ax.legend(loc='upper right')

    plt.show()


# -----------------------------
# Example Usage
# -----------------------------
if __name__ == "__main__":

    # 1) Example Historical data (with or without 1882)
    hist_x_example = np.array([
    1.316704686, 1.560506902, 1.883954736, 1.901135993, 1.566995085, 1.888239111,
    1.767815639, 1.937580904, 1.873388784, 1.962460626, 2.348858984, 2.057223591,
    2.099760734, 1.875480739, 2.021876106, 1.993977436, 1.911738496, 2.044108736,
    1.816153155, 1.955960346, 2.039146477, 1.819509312, 1.83319822, 1.212588665,
    2.252052474, 2.053664131, 2.122736226, 2.065801666, 2.197213375, 2.22046431,
    2.131511517, 2.070517961, 2.213541059, 2.379692465, 2.135678806, 2.202012199,
    2.256969355, 2.369764856, 2.042697312, 2.228214622, 2.278871263, 2.006182536,
    2.294243076, 2.153528633, 2.29020846, 2.252290591, 2.268390627, 2.290400123,
    2.214783076, 2.312524252, 2.313468051, 2.324257267, 2.173547626, 2.311400723,
    2.330567964, 2.286558564, 2.515222691, 2.238078587, 2.282695857, 2.253465243,
    2.343172555, 2.296740037, 2.282014234, 2.320279088, 2.341718372, 2.26647573,
    2.251465557, 2.459209432, 2.311400723, 2.308279095, 2.227153544, 2.274716492,
    2.284157587, 2.403716095, 2.374761821, 2.292281891, 2.279478647, 2.466259005,
    2.353862131, 2.117846382, 2.465498332, 2.445959254, 2.466259005, 2.197112995,
    2.396442288, 2.477316439, 2.462183724, 2.528692687, 2.352201394, 2.499116917,
    2.535225185, 2.52035394, 2.526239116, 2.546936363, 2.496402476, 2.456746512,
    2.544927969, 2.811895797, 2.601334495, 2.618684924, 2.618335678, 2.722935064,
    2.667259614, 3.164681926, 2.996350776, 2.782897787, 2.723393321, 2.74024386,
    2.454878422, 2.466377017, 2.669116617, 2.817536294, 2.817536294, 2.737689579,
    2.728828233, 2.788049513, 2.896213768, 2.801426591, 2.821392033, 2.82544567,
    2.816472736, 2.856799287, 2.81134308, 2.838759182, 2.842429598, 2.851659455,
    2.698264867, 2.857790392, 2.860910183, 2.81134308, 2.8868105, 2.762749222,
    2.85898116, 2.775691815, 2.892214342, 2.776405551, 2.882385057, 2.880779763,
    2.884333707, 2.842346677, 2.88441815, 2.88713039, 2.893103925, 2.898624768,
    2.903743586, 2.913459133
    ])

    hist_y_example = np.array([
    -5.360661225, -5.336517423, -5.696552866, -5.49015318, -5.324192559, -5.610788987,
    -5.376841812, -5.381837998, -5.319775791, -5.276897601, -5.226448266, -5.444284259,
    -5.73786588, -5.572878251, -5.350739856, -5.478407979, -5.368785423, -5.352991638,
    -4.756034979, -4.915111303, -5.483099639, -4.224853354, -4.196024939, -6.417444174,
    -6.395049621, -5.134526623, -5.472740713, -5.67574343, -5.22696407, -5.282275859,
    -5.275676132, -5.567455018, -5.317690851, -6.041201269, -5.681881382, -5.289994544,
    -5.558245257, -5.61001912, -5.321408431, -5.300713122, -5.474636587, -5.452644462,
    -5.511564996, -5.439192442, -5.317804548, -5.440195869, -5.428083729, -5.502332894,
    -5.565504103, -5.752584774, -5.503523015, -5.422898502, -5.095811095, -5.341331921,
    -5.390786767, -5.386794402, -5.226246724, -5.280267914, -5.292730451, -5.278069287,
    -5.414752292, -5.397679242, -5.311531986, -5.359282131, -5.284387861, -5.262697765,
    -5.356024911, -5.549521508, -5.341331921, -5.2335693, -5.62514774, -5.4113367,
    -5.407358331, -5.34102967, -5.328795576, -5.479876251, -5.344162899, -5.305823925,
    -5.213226742, -4.847558839, -5.301766401, -5.313010853, -5.305823925, -4.524775628,
    -5.292746391, -5.486647725, -5.328653799, -5.230852062, -5.541439218, -5.239507576,
    -5.331964859, -5.310244817, -5.296370449, -5.221993409, -5.257411404, -5.220852093,
    -5.278535937, -5.072794301, -5.25877817, -5.256863919, -5.246981445, -5.121096039,
    -5.294044782, -6.131458905, -5.427880067, -5.168402065, -5.231589894, -5.219395424,
    -5.033246659, -5.194177934, -4.9570875, -5.103958192, -5.103958192, -5.192490325,
    -5.175683286, -5.199690367, -5.036670111, -5.181130094, -5.194195606, -5.190853183,
    -5.200276658, -5.196498613, -5.221230706, -5.191335911, -5.178492761, -5.182434697,
    -5.032242711, -5.241558363, -5.181674819, -5.221230706, -5.316843532, -5.088351082,
    -5.170287452, -5.069904826, -5.200340994, -4.996421541, -5.176285007, -5.176377494,
    -5.185958145, -5.170209412, -5.177384683, -5.176513933, -5.168124371, -5.162965761,
    -5.159629594, -5.167815025
    ])

    hist_dates_example = np.array([
    1822.23, 1829.32, 1843.21, 1844.31, 1854.25, 1856.72, 1858.07, 1864.35, 1868.69, 1887.32,
    1888.2, 1888.21, 1888.3, 1889.32, 1890.11, 1890.3, 1892.17, 1892.25, 1893.21, 1893.31,
    1895.25, 1899.22, 1899.23, 1903.2, 1903.8, 1906.21, 1906.213, 1906.54, 1908.2, 1909.02,
    1909.27, 1910.996, 1911.17, 1911.2, 1914.2, 1914.21, 1914.7, 1915.24, 1917.22, 1920.231,
    1920.89, 1921.24, 1922.21, 1923.099, 1923.17, 1923.21, 1923.21, 1923.23, 1923.27, 1924.18,
    1924.2, 1924.32, 1925.13, 1925.18, 1926.16, 1926.2, 1926.205, 1926.23, 1926.23, 1926.24,
    1926.28, 1927.2, 1927.2, 1927.2, 1927.35, 1928.28, 1930.17, 1930.49, 1931.71, 1933.28,
    1937.25, 1938.22, 1938.86, 1941.08, 1941.93, 1942.05, 1944.89, 1950.13, 1951.23, 1951.31,
    1953.942, 1953.955, 1953.966, 1955.07, 1957.21, 1957.86, 1958.22, 1959.21, 1960.35,
    1961.218, 1962.258, 1962.272, 1962.277, 1962.92, 1964.29, 1964.35, 1966.14, 1972.999,
    1975.876, 1975.928, 1976.092, 1979.999, 1982.2, 1982.22, 1988.283, 1989.322, 1991.25,
    1991.62, 1994.182, 1994.22, 1995.25, 1997.272, 1997.272, 1998.03, 2001.091, 2002.296,
    2003.16, 2003.296, 2004.215, 2005.191, 2005.23, 2007.128, 2007.1375, 2008.173,
    2009.303, 2010.282, 2010.5, 2011.173, 2011.207, 2011.223, 2011.225, 2011.395,
    2012.0811, 2013.239, 2013.301, 2014.11, 2014.298, 2015, 2015.196, 2015.25, 2015.5,
    2016, 2016.087, 2017.244, 2018.195, 2019.245
    ])

    # 2) Gaia data (multiple or single)
    gaia_x_example = np.array([2.88766494])
    gaia_y_example = np.array([-5.176089799])

    # 3) LCO data (multiple points, to be averaged)
    lco_x_example = np.array([
        2.914080462
    ])
    lco_y_example = np.array([
        -5.13242039
    ])

    # 4) Predicted point
    pred_x_example = 2.933637292
    pred_y_example = -5.122419471

    # 5) Call the function
    plot_double_star_with_prediction(
        hist_x_example, hist_y_example, hist_dates_example,
        gaia_x=gaia_x_example, gaia_y=gaia_y_example,
        lco_x=lco_x_example,  lco_y=lco_y_example,
        pred_x=pred_x_example, pred_y=pred_y_example
    )
