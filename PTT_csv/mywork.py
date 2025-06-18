import os

import plotly.graph_objs as go
import pandas as pd
import re
from scipy.ndimage import label, find_objects
import statistics
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import gmean
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
import math
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pymysql
from statistics import mean
import plotly.io as pio
import warnings
warnings.filterwarnings('ignore')

from db_config import DB_CONFIG
connection = pymysql.connect(**DB_CONFIG)

oddo1_ref = 0
roll_ref = 0
pipe_thickness = 7.1
outer_dia = 324
theta_ang1 = 1.7
theta_ang2 = 3.4
theta_ang3 = 9.7
positive_sigma_col = 0.75
# positive_sigma_col = 0.90

negative_sigma_col = 3
positive_sigma_row = 0.45
negative_sigma_row = 3
slope_per = 0.65
defect_box_thresh = 0.35
l_per1 = 0.76
w_per1 = 0.55
div_factor = 1.15
value_decreae_per = 0.02

"""
Read Csv file 
"""


# df = pd.read_csv("D:/VDT/desktop_web_application/GMFL_12_Inch_Desktop/DataFram es1/GMFL_12inch_24-01-2025_PTT(1)/3_24-01-2025_PTT(1).csv")
df = pd.read_pickle("C:/Users/pnish/Desktop/PTT_CSV/VDT_WORK_UPDATE/Nishant/PTT_csv/GMFL_12inch_24-01-2025_PTT(2)/3.pkl")
# df = pd.read_pickle("C:/Users/pnish/Desktop/PTT_CSV/VDT_WORK_UPDATE/Nishant/PTT_csv/GMFL_12inch_24-01-2025_PTT(3)/3.pkl")

def get_type_defect_1(geometrical_parameter, length_defect, width_defect):
    L_ratio_W = length_defect / width_defect
    if width_defect > 3 * geometrical_parameter and length_defect > 3 * geometrical_parameter:
        type_of_defect = 'GENERAL'
        return type_of_defect
    elif (
            6 * geometrical_parameter >= width_defect >= 1 * geometrical_parameter and 6 * geometrical_parameter >= length_defect >= 1 * geometrical_parameter) and (
            0.5 < (L_ratio_W) < 2) and not (
            width_defect >= 3 * geometrical_parameter and length_defect >= 3 * geometrical_parameter):
        type_of_defect = 'PITTING'
        return type_of_defect
    elif (1 * geometrical_parameter <= width_defect < 3 * geometrical_parameter) and (L_ratio_W >= 2):
        type_of_defect = 'AXIAL GROOVING'
        return type_of_defect
    elif L_ratio_W <= 0.5 and 3 * geometrical_parameter > length_defect >= 1 * geometrical_parameter:
        type_of_defect = 'CIRCUMFERENTIAL GROOVING'
        return type_of_defect
    elif 0 < width_defect < 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
        type_of_defect = 'PINHOLE'
        return type_of_defect
    elif 0 < width_defect < 1 * geometrical_parameter and length_defect >= 1 * geometrical_parameter:
        type_of_defect = 'AXIAL SLOTTING'
        return type_of_defect
    elif width_defect >= 1 * geometrical_parameter and 0 < length_defect < 1 * geometrical_parameter:
        type_of_defect = 'CIRCUMFERENTIAL SLOTTING'
        return type_of_defect

def internal_or_external(df_new_proximity, x):
    sensor_number = x + 1
    if sensor_number % 4 == 0:
        flapper_no = int(sensor_number / 4)
    else:
        flapper_no = int(sensor_number / 4) + 1
    proximity_no = flapper_no % 4
    if proximity_no == 0:
        proximity_no = 4
    proximity_index = 'F' + str(flapper_no) + 'P' + str(proximity_no)
    print("Proximity_index", proximity_index)
    maximum_depth_proximity_sensor = df_new_proximity[proximity_index]

    c = maximum_depth_proximity_sensor.tolist()
    minimum_value_proximity = min(c)
    mean_value_proximtiy = mean(c)

    print("mean_value_proximtiy", mean_value_proximtiy)
    print("minimum value of proximity", minimum_value_proximity)

    difference_mean = mean_value_proximtiy - minimum_value_proximity

    print("difference_minimum2", difference_mean)
    if difference_mean > 18000:
        type = "Internal"
        return type
    else:
        type = "External"
        return type

def degrees_to_hours_minutes2(degrees):
    if (degrees < 0):
        degrees = degrees % 360
    elif degrees >= 360:
        degrees %= 360
    degrees_per_second = 360 / (12 * 60 * 60)
    total_seconds = degrees / degrees_per_second
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return f"{hours:02d}:{minutes:02d}"

"""
Width Calculation Function
"""
def breadth(start_sensor, end_sensor):
    start_sensor1 = start_sensor + 1
    end_sensor1 = end_sensor + 1
    if start_sensor1 > end_sensor1 or start_sensor1 == end_sensor1:
        return 0  # Return 0 for invalid inputs

    outer_diameter_1 = outer_dia  # 12-inch pipe
    thickness_1 = pipe_thickness  # Replace with Config.pipe_thickness if using from config
    inner_diameter_1 = outer_diameter_1 - 2 * (thickness_1)
    radius_1 = inner_diameter_1 / 2

    theta_2 = theta_ang1             # approximate value for both pipes
    c_1 = math.radians(theta_2)
    theta_3 = theta_ang2               # approximate value for both pipes
    d_1 = math.radians(theta_3)
    theta_4 = theta_ang3             # 9.97 for thickness 5.5 and 9.53 for thickness 7.1
    e_1 = math.radians(theta_4)  # Convert to radians
    # print("c1, d1", c_1, d_1)

    x1 = round(radius_1 * c_1, 1)
    y1 = round(radius_1 * d_1, 1)
    z1 = round(radius_1 * e_1, 1)  # Distance for sensors at multiples of 16
    print("x1, y1, z1", x1, y1, z1)

    bredth = 0
    i = start_sensor1
    while i < end_sensor1:
        # next_sensor = i + 1
        next_sensor = i
        if next_sensor % 16 == 0 and next_sensor != end_sensor1:
            bredth += z1
            # print(f"{i} → {next_sensor:<10} z1 (because {next_sensor} is a multiple of 16)")
        elif next_sensor % 4 == 0:  # If the next sensor is a multiple of 4 (but not 16)
            bredth += y1
            # print(f"{i} → {next_sensor:<10} (y1 - x1) (because {next_sensor} is a multiple of 4)")
        else:
            bredth += x1
            # print(f"{i} → {next_sensor:<10} x1")
        i += 1  # Move to the next sensor
    return bredth

data_x = df.fillna(method='ffill')
df_new_proximity = pd.DataFrame(df, columns=['F1P1', 'F2P2', 'F3P3', 'F4P4', 'F5P1', 'F6P2', 'F7P3', 'F8P4',
                                             'F9P1', 'F10P2', 'F11P3', 'F12P4', 'F13P1', 'F14P2', 'F15P3', 'F16P4',
                                             'F17P1', 'F18P2', 'F19P3', 'F20P4', 'F21P1', 'F22P2', 'F23P3', 'F24P4',
                                             'F25P1', 'F26P2', 'F27P3', 'F28P4', 'F29P1', 'F30P2', 'F31P3', 'F32P4',
                                             'F33P1', 'F34P2', 'F35P3', 'F36P4'])

roll = data_x['ROLL'].tolist()
roll1 = []
for i in roll:
    roll1.append(i - (roll_ref))
# print(data_x)

roll_dictionary = {'1': roll1}
angle = [round(i*2.5, 1) for i in range(0, 144)]
# print(len(angle))

for i in range(2, 145):
    current_values = [round((value + angle[i - 1]), 2) for value in roll1]
    roll_dictionary['{}'.format(i)] = current_values

clock_dictionary = {}
for key in roll_dictionary:
    clock_dictionary[key] = [degrees_to_hours_minutes2(value) for value in roll_dictionary[key]]

Roll_hr = pd.DataFrame(clock_dictionary)
Roll_hr.columns = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]

oddometer1 = ((data_x['ODDO1'] - oddo1_ref)/1000).round(3)
df3_raw = data_x[[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]]
df2 = data_x[[f'F{i}H{j}' for i in range(1, 37) for j in range(1, 5)]]
print("df3", df3_raw)

"""
To Calculate Mean,0.2 sigma (Positive side)
"""
mean1 = df2.mean().tolist()
#mean1=df2.abs().mean().tolist()
# print("Mean Value of each Sensor ", mean1)
standard_deviation = df2.std(axis=0, skipna=True).tolist()
# print("standard_deviation sigma", standard_deviation)

# change the value of standard_deviation, if we required:
mean_plus_1sigma = []
for i, data1 in enumerate(mean1):
    sigma1 = data1 + (positive_sigma_col) * standard_deviation[i]
    mean_plus_1sigma.append(sigma1)
# print("sigma1_positive", mean_plus_1sigma)

"""
To Calculate sigma (Negative side)
"""
mean_negative_3sigma = []
for i_2, data_3 in enumerate(mean1):
    sigma_3 = data_3 - (negative_sigma_col) * standard_deviation[i_2]
    mean_negative_3sigma.append(sigma_3)
# print("sigma3_negative", mean_negative_3sigma)

# for col, data in enumerate(df2.columns):
#     df2[data] = df2[data].apply(
#         lambda x: 1 if (x > mean_plus_1sigma[col]) or (x < mean_negative_3sigma[col]) else 0)

for col, data in enumerate(df2.columns):
    df2[data] = df2[data].apply(
        lambda x: 1 if x > mean_plus_1sigma[col] else (-1 if x < mean_negative_3sigma[col] else 0))

clock_cols = [f"{h:02}:{m:02}" for h in range(12) for m in range(0, 60, 5)]
df2.columns = clock_cols
filtered_df1 = df2
# print("filtered Data",filtered_df1)
# print("df3",df3)

df3_raw.columns = filtered_df1.columns
df1_aligned = filtered_df1.reindex(df3_raw.index)
result = df1_aligned * df3_raw
result = result.dropna()
result.reset_index(drop=True, inplace=True)

result_raw_df = result.mask(result == 0, df3_raw)
result_raw_df = result_raw_df.dropna()
# print("result_raw_df",result_raw_df)
result_raw_df.reset_index(drop=True, inplace=True)

mean_clock_data = result_raw_df.mean().tolist()
val_ori_raw = ((result_raw_df - mean_clock_data)/mean_clock_data) * 100

""""
For PTT Software, Save CSV Here (once saved then comment the code)
"""
#file save for exe file using:
ptt_csv = result.copy()
ptt_csv['ODDO1'] = data_x['ODDO1']
prefix = '_x'
for col in Roll_hr.columns:
    ptt_csv[col + prefix] = Roll_hr[col]
for col in df_new_proximity.columns:
    ptt_csv[col] = df_new_proximity[col]
# ptt_csv.to_csv("E:/Process_Data_12Inch_MFL/MFL1/Clean_Data/12inch_AMFL_28.01.2025/CSV/PTT3_Pipe2_15.csv")
""""
Comment till above line
"""

t = result.transpose()
t_raw = val_ori_raw.transpose()
# t=t.clip(lower=0)
# print("filtered_data", t)
# t.to_csv("C:/Shradha Aagrwal/Desktop/t2.csv")
# data_array = t.values.astype(np.float64)
data_array = t.to_numpy(dtype=np.float64)


def dfs(matrix, x, y, visited, cluster):
    """Perform DFS to find clusters, but only include positive values."""
    stack = [(x, y)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited:  # Ignore negative values
            continue
        if matrix[cx, cy] <= 0:  # Ignore negative values
            continue
        visited.add((cx, cy))
        cluster.append((cx, cy))
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if (0 <= nx < matrix.shape[0] and 0 <= ny < matrix.shape[1] and
                    matrix[nx, ny] > 0 and (nx, ny) not in visited):  # Only traverse positive values
                stack.append((nx, ny))


def do_boxes_overlap(box1, box2):
    """Check if two bounding boxes overlap."""
    return not (box1['end_row'] < box2['start_row'] or
                box1['start_row'] > box2['end_row'] or
                box1['end_col'] < box2['start_col'] or
                box1['start_col'] > box2['end_col'])


# Find clusters of connected non-zero values and calculate bounding boxes
def merge_boxes(box1, box2):
    """Merge two overlapping bounding boxes into one."""
    return {
        'start_row': min(box1['start_row'], box2['start_row']),
        'end_row': max(box1['end_row'], box2['end_row']),
        'start_col': min(box1['start_col'], box2['start_col']),
        'end_col': max(box1['end_col'], box2['end_col'])
    }

visited = set()
bounding_boxes = []

for i in range(data_array.shape[0]):
    for j in range(data_array.shape[1]):
        if data_array[i, j] != 0 and (i, j) not in visited:
            cluster = []
            dfs(data_array, i, j, visited, cluster)
            if cluster:  # Check if the cluster is not empty
                min_row = min(point[0] for point in cluster)
                max_row = max(point[0] for point in cluster)
                min_col = min(point[1] for point in cluster)
                max_col = max(point[1] for point in cluster)
                bounding_boxes.append({'start_row': min_row, 'end_row': max_row, 'start_col': min_col, 'end_col': max_col})

# merged_boxes = []
merged_boxes = []
while bounding_boxes:
    box = bounding_boxes.pop(0)
    merged = False
    for i in range(len(merged_boxes)):
        if do_boxes_overlap(box, merged_boxes[i]):
            merged_boxes[i] = merge_boxes(box, merged_boxes[i])
            merged = True
            break
    if not merged:
        merged_boxes.append(box)

# Create a DataFrame from the bounding boxes
df_sorted = pd.DataFrame(merged_boxes).sort_values(by='start_col')

#print("df_sorted_value.........",df_sorted)

df_clock_holl_oddo1 = data_x['ODDO1']
oddo1_li = list(oddometer1)

figx112 = go.Figure(data=go.Heatmap(
    z=t_raw,
    y=t.index,
    x=[t.columns, oddo1_li],
    #hovertemplate='(%{x}, %{z})<br>Actual Ori: %{text[2]}',
    # hovertemplate='(%{x}, %{z})<br>Sensor no: %{text[0]}<br>Actual Ori: %{text[2]}',
    # text=[[item for item in Roll[col]] for col in map_ori_sens_1.columns],
    # x=oriVal111.columns,
    hovertemplate='Oddo: %{x}<br>Clock:{y}<br>Value: %{z}',
    zmin=-5,
    zmax=18,
    colorscale='jet',
    # colorbar=dict(title='Value')
))

max_submatrix_list = []
min_submatrix_list = []
new_boxes = []
for _, row in df_sorted.iterrows():
    start_sensor = row['start_row']
    end_sensor = row['end_row']
    start_reading = row['start_col']
    end_reading = row['end_col']
    if start_sensor == end_sensor:
        pass
    else:
        try:
            submatrix = result.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]
            submatrix = submatrix.apply(pd.to_numeric, errors='coerce')  # Ensure numeric data
            if submatrix.isnull().values.any():
                print("Submatrix contains NaN values, skipping this iteration.")
                continue
            max_value = submatrix.max().max()
            max_submatrix_list.append(max_value)
            two_d_list = submatrix.values.tolist()
            min_positive = min(x for row in two_d_list for x in row if x > 0)
            min_submatrix_list.append(min_positive)
        except Exception as e:
            print(f"Error found: {str(e)}")
            pass

max_of_all = max(max_submatrix_list)  # Get the max of all submatrix max_values
min_of_all = min(min_submatrix_list)
threshold_value = round(min_of_all + (max_of_all - min_of_all) * defect_box_thresh)
# print("Max of all submatrices:", max_of_all)
# print("Min of all submatrices:", min_of_all)
# print("Threshold Value:", threshold_value)

submatrices_dict = {}
defect_counter = 1
finial_defect_list = []
for _, row in df_sorted.iterrows():
    start_sensor = row['start_row']
    end_sensor = row['end_row']
    start_reading = row['start_col']
    end_reading = row['end_col']
    # print(start_sensor, end_sensor, start_reading, end_reading)
    if start_sensor == end_sensor:
        pass
    else:
        try:
            submatrix = result.iloc[start_reading:end_reading + 1, start_sensor:end_sensor + 1]
            submatrix = submatrix.apply(pd.to_numeric, errors='coerce')
            two_d_list = submatrix.values.tolist()
            max_value = submatrix.max().max()
            min_positive = min(x for row in two_d_list for x in row if x > 0)

            if (threshold_value <= max_value <= max_of_all):
                print("max_value", max_value)
                print("min_positive", min_positive)
                print("Max of all submatrices:", max_of_all)
                print("Threshold Value:", threshold_value)
                print(".....................................................")

                depth_old = (max_value-min_positive)/min_positive*100
                print("depth_old", depth_old)

                max_column = submatrix.max().idxmax()
                max_index = submatrix.columns.get_loc(max_column)
                sub_matrix_list = list(submatrix[max_column])

                # q1, q3 = np.percentile(sub_matrix_list, [25, 25])
                # start_point = np.argmax(sub_matrix_list > q1)
                # end_point = len(sub_matrix_list) - np.argmax(result[::-1] > q3) - 1
                # print("start_point",start_point)
                # print("end_point",end_point)

                # if all(val < 0 for val in sub_matrix_list):  # All values are negative
                #     max_val = max(sub_matrix_list)
                #     min_val = min(sub_matrix_list)
                #     print("max_val,min_val", max_val, min_val)
                # elif all(val > 0 for val in sub_matrix_list):  # All values are positive
                #     max_val = max(sub_matrix_list)
                #     min_val = min(sub_matrix_list)
                #     print("max_val,min_val", max_val, min_val)
                # else:
                #     max_val = max(sub_matrix_list)
                #     min_val = min(sub_matrix_list)
                #     print("max_val,min_val", max_val, min_val)

                counter_difference = end_reading-start_reading
                print("counter_difference", counter_difference)
                divid = int(counter_difference/2)
                center = start_reading+divid
                factor = divid*l_per1
                start = int(center-factor)
                end = int(center+factor)

                print("start_reading", start_reading)
                print("end_reading", end_reading)
                print("start", start)
                print("end", end)

                length_percent = (df_clock_holl_oddo1[end] - df_clock_holl_oddo1[start])
                print("length of defect", length_percent)

                """
                Start_oddo1 and end_oddo1 to calculated......
                """
                start_oddo1 = df_clock_holl_oddo1[start_reading]
                end_oddo1 = (df_clock_holl_oddo1[end_reading])/1000
                time_sec = end_reading/1500
                speed = end_oddo1/time_sec
                print("speed(m/s)", speed)

                base_value = mean1[max_index]
                print("base_value", base_value)

                internal_external = internal_or_external(df_new_proximity, max_index)
                print("internal_external", internal_external)

                absolute_distance = df_clock_holl_oddo1[start_reading]
                print("absolute_distance", absolute_distance)

                upstream = df_clock_holl_oddo1[start_reading] - df_clock_holl_oddo1[0]
                print("upstream", upstream)

                length = (df_clock_holl_oddo1[end_reading] - df_clock_holl_oddo1[start_reading])
                print("length of defect", length)

                # width = breadth(start_sensor, end_sensor)
                # print("breadth of defect", width)

                counter_difference_1 = (end_sensor + 1) - (start_sensor + 1)
                divid_1 = int(counter_difference_1/2)
                center_1 = start_sensor + divid_1
                factor1_1 = divid_1 * w_per1
                start1_1 = (int(center_1 - factor1_1)) - 1
                end1_1 = (int(center_1 + factor1_1)) - 1
                print("start_sensor_ind", start_sensor)
                print("end_sensor_ind", end_sensor)
                print("start1_1_ind", start1_1)
                print("end1_1_ind", end1_1)
                width = breadth(start_sensor, end_sensor)
                print("width_new", width)

                df_copy_submatrix = result.iloc[start_reading:end_reading+1, start1_1:end1_1 + 1]
                # print("df_copy_submatrix", df_copy_submatrix)
                # df_copy_submatrix_std = result.iloc[start_reading:end_reading+1, start1_1:end1_1 + 1]

                ############ Width modified code, duplicacy started from here ############
                def replace_first_column(df_n, s_sensor, e_sensor):
                    s_sensor = s_sensor + 1
                    e_sensor = e_sensor + 1
                    # Generate new column names within the given range
                    new_columns = list(range(s_sensor, s_sensor + df_n.shape[1]))
                    # Assign new column names
                    df_n.columns = new_columns
                    # Drop the last column if it exceeds end_sensor
                    df_n = df_n.loc[:, df_n.columns <= e_sensor]
                    return df_n

                # df_duplicate_std = replace_first_column(df_copy_submatrix, start_sensor, end_sensor)
                # df_duplicate_std.columns = df_duplicate_std.columns.astype(str)
                # print("df_duplicate", df_duplicate)

                df_duplicate = replace_first_column(df_copy_submatrix, start1_1, end1_1)
                df_duplicate.columns = df_duplicate.columns.astype(str)

                outer_diameter_1 = outer_dia  # 12-inch pipe
                thickness_1 = pipe_thickness  # Replace with Config.pipe_thickness if using from config
                inner_diameter_1 = outer_diameter_1 - 2 * thickness_1
                radius_1 = inner_diameter_1 / 2
                theta_2 = theta_ang1  # approximate value for both pipes
                c_1 = math.radians(theta_2)
                theta_3 = theta_ang2  # approximate value for both pipes
                d_1 = math.radians(theta_3)
                theta_4 = theta_ang3  # 9.97 for thickness 5.5 and 9.53 for thickness 7.1
                e_1 = math.radians(theta_4)  # Convert to radians
                # print("c1, d1", c_1, d_1)
                x1 = round(radius_1 * c_1, 1)
                y1 = round(radius_1 * d_1, 1)
                z1 = round(radius_1 * e_1, 1)

                def process_csv(df_dupe):
                    new_data = {}
                    next_col = None

                    base = round(x1 / div_factor)
                    c = round(y1 / div_factor)
                    dee = round(z1 / div_factor)

                    # base1 = base//2
                    # base2 = base-base1

                    c1 = c//2
                    c2 = c-c1

                    dee1 = dee//2
                    dee2 = dee-dee1

                    def generate_suffixes(n):
                        return [chr(ord('a') + i) for i in range(n)]

                    base_suffixes = generate_suffixes(int(base))

                    # base1_suffixes = generate_suffixes(int(base1))
                    # base2_suffixes = generate_suffixes(int(base2))
                    c1_suffixes = generate_suffixes(int(c1))
                    c2_suffixes = generate_suffixes(int(c2))
                    dee1_suffixes = generate_suffixes(int(dee1))
                    dee2_suffixes = generate_suffixes(int(dee2))

                    """" without value_decrease in matrix """
                    for colu in df_dupe.columns:
                        col_int = int(colu)
                        next_col = str(col_int + 1)

                        if next_col in df_dupe.columns:
                            # Special Case 1
                            if col_int % 4 == 0 and col_int % 16 != 0:
                                for idx, suffix in enumerate(c1_suffixes):
                                    # reduction = 1- ((idx+1)*Config.value_decrease_percent)
                                    # new_data[f"{col_int}{suffix}_extra"] = df_dupe[colu]*reduction
                                    new_data[f"{col_int}{suffix}_extra"] = df_dupe[colu]
                                # for suffix in c2_suffixes:
                                for idx, suffix in enumerate(c2_suffixes):
                                    # reduction = 1 - ((idx + 1) * Config.value_decrease_percent)
                                    # new_data[f"{int(next_col)}{suffix}_extra"] = df_dupe[next_col]*reduction
                                    new_data[f"{int(next_col)}{suffix}_extra"] = df_dupe[next_col]

                            # Special Case 2
                            elif col_int % 16 == 0:
                                # for suffix in dee1_suffixes:
                                for idx,suffix in enumerate(dee1_suffixes):
                                    # reduction = 1 - ((idx+1) * Config.value_decrease_percent)
                                    # new_data[f"{col_int}{suffix}_extra2"] = df_dupe[colu]*reduction
                                    new_data[f"{col_int}{suffix}_extra2"] = df_dupe[colu]
                                # for suffix in dee2_suffixes:
                                for idx, suffix in enumerate(dee2_suffixes):
                                    # reduction = 1 - ((idx + 1) * Config.value_decrease_percent)
                                    # new_data[f"{int(next_col)}{suffix}_extra2"] = df_dupe[next_col]*reduction
                                    new_data[f"{int(next_col)}{suffix}_extra2"] = df_dupe[next_col]

                            else:
                                for idx,suffix in enumerate(base_suffixes):
                                    # reduction = 1- ((idx+1)*Config.value_decrease_percent)
                                    # new_data[f"{col_int}{suffix}"] = df_dupe[colu]*reduction
                                    new_data[f"{col_int}{suffix}"] = df_dupe[colu]

                    """" with value_decrease in matrix """
                    # for colu in df_dupe.columns:
                    #     # print(f"colu: {colu}, type: {type(colu)}")
                    #
                    #     col_int = int(colu)
                    #     next_col = str(col_int + 1)
                    #
                    #     if next_col in df_dupe.columns:
                    #         # Special Case 1
                    #         if col_int % 4 == 0 and col_int % 16 != 0:
                    #             for idx, suffix in enumerate(c1_suffixes):
                    #                 reduction = 1- ((idx+1)*Config.value_decrease_percent)
                    #                 new_data[f"{col_int}{suffix}_extra"] = df_dupe[colu]*reduction
                    #             # for suffix in c2_suffixes:
                    #             for idx, suffix in enumerate(c2_suffixes):
                    #                 reduction = 1 - ((idx + 1) * Config.value_decrease_percent)
                    #                 new_data[f"{int(next_col)}{suffix}_extra"] = df_dupe[next_col]*reduction
                    #
                    #         # Special Case 2
                    #         elif col_int % 16 == 0:
                    #             # for suffix in dee1_suffixes:
                    #             for idx,suffix in enumerate(dee1_suffixes):
                    #                 reduction = 1 - ((idx+1) * Config.value_decrease_percent)
                    #                 new_data[f"{col_int}{suffix}_extra2"] = df_dupe[colu]*reduction
                    #             # for suffix in dee2_suffixes:
                    #             for idx, suffix in enumerate(dee2_suffixes):
                    #                 reduction = 1 - ((idx + 1) * Config.value_decrease_percent)
                    #                 new_data[f"{int(next_col)}{suffix}_extra2"] = df_dupe[next_col]*reduction
                    #
                    #         else:
                    #             # Base duplication
                    #
                    #             # for suffix in base_suffixes:
                    #             for idx,suffix in enumerate(base_suffixes):
                    #                 reduction = 1- ((idx+1)*Config.value_decrease_percent)
                    #                 new_data[f"{col_int}{suffix}"] = df_dupe[colu]*reduction
                    #
                    #
                    #             # for suffix in base1_suffixes:
                    #             #     new_data[f"{col_int}{suffix}"] = df_dupe[colu]
                    #             # for suffix in base2_suffixes:
                    #             #     new_data[f"{int(next_col)}{suffix}"] = df_dupe[next_col]

                    new_df_duplicate = pd.DataFrame(new_data)
                    return new_df_duplicate

                def process_submatrix(df_diff):
                    if df_diff.isnull().values.any():
                        return None
                    ### STDEV ON DEFECT MATRIX ROW-WISE ###
                    # print("df_diff", df_diff)
                    # df_diff = df_diff.applymap(lambda x: np.log(x) if x > 0 else np.nan)

                    df_diff_mean = list(df_diff.median(axis=1))
                    df_std_dev = list(df_diff.std(axis=1, ddof=1))
                    mean_plus_std = list(map(lambda x, y: x + y * (positive_sigma_row), df_diff_mean, df_std_dev))
                    # mean_plus_std = list(map(lambda x, y: x * (positive_sigma_row), df_diff_mean, df_std_dev))
                    mean_plus_std_series = pd.Series(mean_plus_std, index=df_diff.index)
                    # mean_neg_std = list(map(lambda x, y: x - y * (negative_sigma_row), df_diff_mean, df_std_dev))
                    # mean_neg_std_series = pd.Series(mean_neg_std, index=df_diff.index)
                    # Apply the function row-wise
                    df_result = df_diff.apply(lambda row: row.map(lambda x: 1 if x > mean_plus_std_series[row.name] else 0), axis=1)

                    ### STDEV ON DEFECT MATRIX COLUMN-WISE ###
                    # df_diff_mean = df_diff.median(axis=0).tolist()
                    # df_std_dev = df_diff.std(axis=0, skipna=True, ddof=1).tolist()
                    # mean_plus_std = []
                    # for i_std, data_std in enumerate(df_diff_mean):
                    #     sigma_std_col = data_std + (positive_sigma_row * df_std_dev[i_std])
                    #     mean_plus_std.append(sigma_std_col)
                    # df_result = pd.DataFrame(index=df_diff.index)
                    # for col1_std, data1_std in enumerate(df_diff.columns):
                    #     df_result[data1_std] = df_diff[data1_std].apply(lambda x: 1 if x > mean_plus_std[col1_std] else 0)

                    count_ones_per_column = df_result.sum(axis=0)
                    first_col_with_1 = count_ones_per_column.ne(0).idxmax()
                    last_col_with_1 = count_ones_per_column[::-1].ne(0).idxmax()
                    first_col_with_1_idx = df_result.columns.get_loc(first_col_with_1)
                    last_col_with_1_idx = df_result.columns.get_loc(last_col_with_1)

                    df_between = df_result.iloc[:, first_col_with_1_idx:last_col_with_1_idx + 1]
                    # Count columns that have at least one '1'
                    num_cols_with_ones = (df_between == 1).any(axis=0).sum()
                    num_cols_between = last_col_with_1_idx - first_col_with_1_idx + 1

                    # Step 3: Count the number of columns to remove from start and end
                    num_cols_to_remove_start = first_col_with_1_idx
                    num_cols_to_remove_end = len(count_ones_per_column) - 1 - last_col_with_1_idx

                    width_1_only = round(num_cols_with_ones * div_factor)
                    width_0_yes = round(num_cols_between * div_factor)
                    print("width_1_only", width_1_only)
                    print("width_0_yes", width_0_yes)
                    trimmed_original_matrix = df_diff.iloc[:, first_col_with_1_idx: last_col_with_1_idx + 1]
                    new_start_sensor = start1_1+num_cols_to_remove_start
                    new_end_sensor = end1_1-num_cols_to_remove_end
                    return trimmed_original_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor

                def slope_filter(df_diff):
                    refined_outputs = {}
                    width_0_no = 0
                    width_0_no1 = 0
                    try:
                        if df_diff.isnull().values.any():
                            return None
                        # q1 = df_diff.quantile(0.25)
                        # q3 = df_diff.quantile(0.75)
                        # iqr = q3 - q1
                        # iqr_threshold = iqr[iqr > 0].mean()
                        # important_cols_iqr = iqr[iqr > iqr_threshold].index
                        # refined_outputs['iqr'] = df_diff[important_cols_iqr]

                        slope_strength = df_diff.diff().abs().sum()
                        slope_threshold = slope_strength.mean() * (slope_per)
                        important_cols_slope = slope_strength[slope_strength > slope_threshold].index
                        refined_outputs['slope'] = df_diff[important_cols_slope]

                        width_0_no = (len(important_cols_slope) - 1) * div_factor
                        # width_0_no1 = (len(important_cols_iqr) - 1) * div_factor
                    except Exception as e:
                        refined_outputs['slope'] = None
                        # refined_outputs['iqr'] = None
                        print("Method failed:", e)
                    return refined_outputs, width_0_no

                modified_df = process_csv(df_duplicate)
                refined_output, width_slope = slope_filter(modified_df)
                trimmed_matrix, width_1_only, width_0_yes, new_start_sensor, new_end_sensor = process_submatrix(modified_df)
                print(trimmed_matrix.columns.to_list())
                # print("new_start_sensor_ind:", new_start_sensor)
                # print("new_end_sensor_ind:", new_end_sensor)

                geometrical_parameter = pipe_thickness
                dimension_classification = get_type_defect_1(geometrical_parameter, length, width)
                print("dimension_classification", dimension_classification)

                # print("start_reading", start, 'end_sensor', new_end_sensor)
                avg_counter = round((start+end)/2)
                avg_sensor = round((start1_1+end1_1)/2)
                orientation = Roll_hr.iloc[avg_counter, avg_sensor]
                # k2 = map_ori_sens_1.iloc[start_reading, end_sensor]
                # orientation = k2[2]
                print("orientation", orientation)

                try:
                    ################# each pipe thickness can be change #################
                    depth_val = round((((length / width) * (max_value / base_value))*100)/pipe_thickness)
                    # print("depth_val", depth_val)
                except:
                    depth_val = 0

                if depth_val > 5 and width > 3 and length > 3:
                    submatrices_dict[(defect_counter, start_sensor, end_sensor)] = modified_df
                    print("depth_value.....", depth_val)
                    # print("...................................................................................")
                    runid = 1
                    finial_defect_list.append(
                        {"runid": runid, "start_reading": start_reading, "end_reading": end_reading, "start_sensor": start1_1,
                         "end_sensor": end1_1, "absolute_distance": absolute_distance, "upstream": upstream, "length": length,
                         "length_percent": length_percent, "breadth": width, 'width_new': width_slope, 'width_new2': round(width_1_only, 0),
                         'orientation': orientation, 'defect_type': internal_external,
                         "dimension_classification": dimension_classification, "depth": depth_val, "depth_old": depth_old,
                         "start_oddo1": start_oddo1, "end_oddo1": end_oddo1, "speed": speed, "Min_Val": min_positive, "Max_Val": max_value
                         })
                    figx112.add_shape(
                        type='rect',
                        x0=start_reading - 0.5,  # Adjust for center of cells
                        x1=end_reading + 0.5,
                        y0=start_sensor - 0.5,
                        y1=end_sensor + 0.5,
                        line=dict(color='red', width=1),
                        fillcolor='rgba(255, 0, 0, 0.2)'  # Optional: transparent fill
                    )
                    # Add number annotation above each defect box
                    figx112.add_annotation(
                        x=(start_reading + end_reading) / 2,
                        y=start_sensor - 1,  # Position above the box; adjust if needed
                        # text=str(defect_counter),
                        text=f"Defect {defect_counter}<br>Sensor: {start1_1} to {end1_1}",
                        showarrow=False,
                        font=dict(color="red", size=12),
                        bgcolor="white",
                        bordercolor="black",
                        borderwidth=1
                    )

                    # Increment the counter only for valid (stored) defects
                    defect_counter += 1
            else:
                print("Error found 1:")
                pass
        except Exception as e:
            print("Error found 2:", {str(e)})
            pass

print(f"\nTotal submatrices stored: {len(submatrices_dict)}")
output_dir = os.path.join(os.getcwd(), "defect_matrices")
os.makedirs(output_dir, exist_ok=True)
for (defect_id, start_sensor, start_sensor), matrix in submatrices_dict.items():
    filename = f"submatrix_ptt-4{defect_id, start_sensor, start_sensor}.csv"
    filepath = os.path.join(output_dir, filename)
    matrix.to_csv(filepath, index=False)
    # print(f"Saved {filename}")

with (connection.cursor() as cursor):
    for i in finial_defect_list:
        runid = i['runid']
        start_index = i['start_reading']
        end_index = i['end_reading']
        # print("df", defect_df)
        start_sensor = i['start_sensor']
        end_sensor = i['end_sensor']
        absolute_distance = round(i['absolute_distance']/1000, 3)
        upstream = round(i['upstream']/1000, 3)
        length = round(i['length'])
        length_percent = round(i['length_percent'])
        Width = round(i['breadth'])
        width_new = round(i['width_new'])
        width_new2 = round(i['width_new2'])
        depth = round(i['depth'])
        depth_old = round(i['depth_old'])
        orientation = i['orientation']
        defect_type = i['defect_type']
        dimension_classification = i['dimension_classification']
        start_oddo1 = i['start_oddo1']
        end_oddo1 = i['end_oddo1']
        speed = round(i['speed'], 2)
        min_value = i['Min_Val']
        max_value = i['Max_Val']
        # am=i['Am']
        # gm=i['Gm']
        # hm=i['hm']
        with connection.cursor() as cursor:
            query_defect_insert = "INSERT INTO defect_local_hm(runid, start_index, end_index, start_sensor, end_sensor, absolute_distance, upstream, length, length_percent, Width, width_new, width_new2, depth,depth_old, orientation, defect_type, dimension_classification, start_oddo1, end_oddo1, speed, Min_Val, Max_Val) VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "

            cursor.execute(query_defect_insert, (
                int(runid), start_index, end_index, start_sensor, end_sensor, absolute_distance, upstream,
                length, length_percent, Width, width_new, width_new2, depth, depth_old,orientation, defect_type, dimension_classification,
                start_oddo1, end_oddo1, speed, min_value, max_value))

            connection.commit()

figx112.update_layout(
    # xaxis=dict(
    #     tickvals=1000
    # ),
    title='Heatmap',
    xaxis_title='Odometer(m)',
    yaxis_title='Orientation'
)
figx112.show()

# # Dash App
# app = dash.Dash(__name__)
#
# app.layout = html.Div([
#                 dcc.Graph(
#                     id='heatmap',
#                     figure=figx112,
#                     config={
#                         'displayModeBar': True,
#                         'modeBarButtonsToAdd': ['select2d', 'lasso2d'],
#                         'scrollZoom': True
#                     }
#                 ),
#                 html.Div(id='output-div', style={'marginTop': 20})
#             ])
#
# @app.callback(
#     Output('output-div', 'children'),
#     [Input('heatmap', 'selectedData')]
# )
# def capture_selection(selected_data):
#     global finial_defect_list  # Ensure the global list is updated
#
#     if selected_data and 'range' in selected_data:
#         x_range = selected_data['range']['x']
#         y_range = selected_data['range']['y']
#
#         x_start, x_end = x_range
#         y_start, y_end = y_range
#
#         x_labels = oddo1_li
#         y_labels = map_ori_sens.index.tolist()
#
#         x_start_label = x_labels[int(round(x_start))]
#         x_end_label = x_labels[int(round(x_end))]
#         y_start_label = y_labels[int(round(y_start))]
#         y_end_label = y_labels[int(round(y_end))]
#
#         output_text = (
#             f"Box Coordinates: Start = (x={x_start_label}, y={y_start_label}), "
#             f"End = (x={x_end_label}, y={y_end_label})\n"
#             f"Start Sensor: {y_start_label}, End Sensor: {y_end_label}"
#         )
#
#         try:
#             start_reading = int(round(x_start))
#             end_reading = int(round(x_end))
#             start_sensor = int(round(y_start))
#             end_sensor = int(round(y_end))
#
#             length = (oddo1_li[end_reading] - oddo1_li[start_reading]) * 1000  # Length in mm
#             width = breadth(start_sensor, end_sensor)
#
#             if width <= 0:
#                 return output_text
#
#             base_value = mean1[start_sensor]
#             max_value = 1000
#             depth_val = (length / width) * (max_value / base_value)
#             depth_val = (depth_val * 100) / 7.5
#
#             finial_defect_list.append({
#                 "Box Number": len(finial_defect_list) + 1,
#                 "Distance to U/S GW(m)": start_reading,
#                 "x1": end_reading,
#                 "y0": start_sensor,
#                 "y1": end_sensor,
#                 "Absolute Distance": oddo1_li[start_reading],
#                 "Width": length,
#                 "Breadth": width,
#                 "Orientation o' clock": map_ori_sens.iloc[start_reading, end_sensor][2],
#                 "Depth % ": depth_val,
#                 "Min_Val": None,
#                 "Max_Val": None,
#             })
#
#             figx112.add_shape(
#                 type='rect',
#                 x0=start_reading,
#                 x1=end_reading,
#                 y0=start_sensor,
#                 y1=end_sensor,
#                 line=dict(color='blue', width=2),
#                 fillcolor='rgba(0, 0, 255, 0.2)'
#             )
#
#         except Exception as e:
#             print(f"Error adding manual defect: {e}")
#
#         return output_text
#
#     return "No selection made"
#
# if __name__ == '__main__':
#     app.run_server(debug=True, port=8051)

