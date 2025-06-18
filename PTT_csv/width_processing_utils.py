# width_processing_utils.py

import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

def interpolate_matrix(df_duplicate):
    interpolated_rows = []
    x_coords = np.arange(1, len(df_duplicate.columns) + 1)

    for idx, row in df_duplicate.iterrows():
        y_values = row.values

        # Fill NaN with row mean
        if np.any(np.isnan(y_values)):
            y_values = pd.Series(y_values).fillna(np.nanmean(y_values)).values

        cs = CubicSpline(x_coords, y_values)
        # x_interp = np.linspace(1, len(df_duplicate.columns), len(df_duplicate.columns) * 10)
        x_interp = np.linspace(1, len(df_duplicate.columns), len(df_duplicate.columns) * 3)

        y_interp = cs(x_interp)

        interpolated_rows.append(y_interp)

    interpolated_matrix = pd.DataFrame(interpolated_rows)
    return interpolated_matrix


def apply_mad_filtering(df_interp):
    filtered_matrix = df_interp.copy()
    for idx, row in df_interp.iterrows():
        row_median = np.median(row)
        mad = np.median(np.abs(row - row_median))
        mad_threshold = row_median + 0.8 * mad
        filtered_matrix.iloc[idx] = (row > mad_threshold).astype(int)

    # Apply rolling window smoothing here
    filtered_matrix = filtered_matrix.rolling(window=3, axis=1, min_periods=1).max()

    return filtered_matrix

def calculate_width(filtered_matrix, div_factor=1.0):
    widths = []
    tolerance_gap = 6  # Larger connection gap

    for idx, row in filtered_matrix.iterrows():
        defect_columns = np.where(row.values == 1)[0]
        num_cols_with_ones = len(defect_columns)

        if num_cols_with_ones < 10:
            correction_factor = 1.50
        elif num_cols_with_ones < 20:
            correction_factor = 1.30
        else:
            correction_factor = 1.15

        # width_1_only = round((num_cols_with_ones + tolerance_gap) * div_factor * correction_factor)
        if len(defect_columns) > 0:
          center_of_defect = np.mean(defect_columns)
        if center_of_defect < len(row) / 4 or center_of_defect > 3 * len(row) / 4:
           correction_factor -= 0.05  # Less correction at edges

        width_1_only = round((num_cols_with_ones + tolerance_gap) * div_factor * correction_factor * 0.9)


        if width_1_only > 100:
            width_1_only = 100

        widths.append(width_1_only)

    return widths
