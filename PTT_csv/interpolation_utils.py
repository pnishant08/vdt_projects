import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

def process_csv_with_interpolation_row(df_dupe, x1, y1, z1, div_factor):
    new_data = {}

    base = round(x1 / div_factor)
    c = round(y1 / div_factor)
    dee = round(z1 / div_factor)

    c1 = c // 2
    c2 = c - c1
    dee1 = dee // 2
    dee2 = dee - dee1

    def generate_suffixes(n):
        return [chr(ord('a') + i) for i in range(n)]

    base_suffixes = generate_suffixes(int(base))
    c1_suffixes = generate_suffixes(int(c1))
    c2_suffixes = generate_suffixes(int(c2))
    dee1_suffixes = generate_suffixes(int(dee1))
    dee2_suffixes = generate_suffixes(int(dee2))

    sensor_cols = [int(col) for col in df_dupe.columns]
    sensor_cols.sort()

    for idx, row in df_dupe.iterrows():
        sensor_values = row.values
        x_coords = np.array(sensor_cols)

        if np.any(np.isnan(sensor_values)):
            continue  # Skip row if NaN exists

        cs = CubicSpline(x_coords, sensor_values)

        for i, col_int in enumerate(sensor_cols):
            if i == len(sensor_cols) - 1:
                continue

            next_col_int = sensor_cols[i + 1]

            if col_int % 4 == 0 and col_int % 16 != 0:
                total_virtual = len(c1_suffixes) + len(c2_suffixes)
                xi = np.linspace(col_int, next_col_int, total_virtual + 2)[1:-1]

                for idx_suf, suffix in enumerate(c1_suffixes):
                    val = cs(xi[idx_suf])
                    new_data.setdefault(f"{col_int}{suffix}_extra", []).append(float(val))

                for idx_suf, suffix in enumerate(c2_suffixes):
                    val = cs(xi[len(c1_suffixes) + idx_suf])
                    new_data.setdefault(f"{next_col_int}{suffix}_extra", []).append(float(val))

            elif col_int % 16 == 0:
                total_virtual = len(dee1_suffixes) + len(dee2_suffixes)
                xi = np.linspace(col_int, next_col_int, total_virtual + 2)[1:-1]

                for idx_suf, suffix in enumerate(dee1_suffixes):
                    val = cs(xi[idx_suf])
                    new_data.setdefault(f"{col_int}{suffix}_extra2", []).append(float(val))

                for idx_suf, suffix in enumerate(dee2_suffixes):
                    val = cs(xi[len(dee1_suffixes) + idx_suf])
                    new_data.setdefault(f"{next_col_int}{suffix}_extra2", []).append(float(val))

            else:
                total_virtual = len(base_suffixes)
                xi = np.linspace(col_int, next_col_int, total_virtual + 2)[1:-1]

                for idx_suf, suffix in enumerate(base_suffixes):
                    val = cs(xi[idx_suf])
                    new_data.setdefault(f"{col_int}{suffix}", []).append(float(val))

    max_len = max(len(v) for v in new_data.values())
    for key in new_data:
        if len(new_data[key]) < max_len:
            new_data[key] += [np.nan] * (max_len - len(new_data[key]))

    new_df_duplicate = pd.DataFrame(new_data)
    return new_df_duplicate
