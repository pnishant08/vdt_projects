# main_plot.py

import pandas as pd
from graph_plotter import (
    # plot_real_oddo,
    # plot_combined,
    # plot_psafe_single,      
    # plot_psafe_combined,     
    # plot_depth_single, 
    # plot_depth_combined,
    plot_orientation_with_dropdown,
    plot_erf_with_dropdown,
    plot_psafe_with_dropdown,
    plot_depth_with_dropdown,
)

# Load Excel data
file_path = r"C:\Users\pnish\Desktop\graph data.xlsx"
df = pd.read_excel(file_path)
# print(df.columns.tolist())
# print(df)

# Filter and sort
df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()
df.sort_values(by='Abs. Distance (m)', inplace=True)

df.columns = df.columns.str.strip()
df.rename(columns={'Psafe (ASME B31G), kg/cm2': 'Psafe (ASME B31G)'}, inplace=True)
df.rename(columns={'Depth, % WT': 'Depth % WT'}, inplace=True)
df['Abs. Distance (m)'] = df['Abs. Distance (m)'].round(1)

# Make a separate copy for ERF grouping
df_erf = df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).agg({
    'ERF (ASME B31G)': 'max'
})
df_erf.sort_values(by='Abs. Distance (m)', inplace=True)


# Group by Abs. Distance and Surface Location to prevent duplicate x-values
df_grouped = df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).agg({
    'Psafe (ASME B31G)': 'max'  # use 'mean' if you want average instead
})
# Sort for consistent plotting
df_grouped.sort_values(by='Abs. Distance (m)', inplace=True)



# ODDO ticks
min_oddo = int(df['Abs. Distance (m)'].min()) // 500 * 500
max_oddo = int(df['Abs. Distance (m)'].max()) + 500
tick_vals = list(range(min_oddo, max_oddo, 500))



# For ERF (plot from df directly)
internal_df_erf = df_erf[df_erf['Surface Location'] == 'Internal'].copy()
external_df_erf = df_erf[df_erf['Surface Location'] == 'External'].copy()

# For Psafe (plot from grouped df)
internal_df_psafe = df_grouped[df_grouped['Surface Location'] == 'Internal'].copy()
external_df_psafe = df_grouped[df_grouped['Surface Location'] == 'External'].copy()


# Group Depth like Psafe
df_grouped_depth = df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).agg({
    'Depth % WT': 'max'  # or 'mean' if you want average depth
})

# Separate grouped Depth for plotting
internal_df_depth = df_grouped_depth[df_grouped_depth['Surface Location'] == 'Internal'].copy()
external_df_depth = df_grouped_depth[df_grouped_depth['Surface Location'] == 'External'].copy()


# # ================================ ERF ================================
# plot_real_oddo(internal_df_erf, tick_vals, min_oddo, max_oddo, 'ERF (ASME B31G)', "Internal Defects – ERF", 'steelblue', 'internal_erf.html')
# plot_real_oddo(external_df_erf, tick_vals, min_oddo, max_oddo, 'ERF (ASME B31G)', "External Defects – ERF", 'orangered', 'external_erf.html')
# plot_combined(internal_df_erf, external_df_erf, tick_vals, min_oddo, max_oddo, 'ERF (ASME B31G)', "Combined Internal & External – ERF", 'combined_erf.html')
#-----------ERF WITH DROP DOWN-----------
# plot_erf_with_dropdown(internal_df_erf, external_df_erf, min_oddo, max_oddo, tick_vals, "erf_dropdown.html")


# # # ================================ Psafe ================================
# plot_psafe_single(internal_df_psafe, "Internal Defects – Psafe (ASME B31G)", 'steelblue', "\\", 'internal_psafe.html', min_oddo, max_oddo)
# plot_psafe_single(external_df_psafe, "External Defects – Psafe (ASME B31G)", 'orangered', "x", 'external_psafe.html', min_oddo, max_oddo)
# plot_psafe_combined(internal_df_psafe, external_df_psafe, min_oddo, max_oddo, 'combined_psafe.html')
#-----------PSAFE WITH DROPDOWN-----------
# plot_psafe_with_dropdown(internal_df_psafe, external_df_psafe, min_oddo, max_oddo, tick_vals, "psafe_dropdown.html")


# # ================================ Depth ================================
# plot_depth_single(internal_df_depth, "Internal Defects – Depth (% WT)", 'steelblue', 'internal_depth.html', min_oddo, max_oddo)
# plot_depth_single(external_df_depth, "External Defects – Depth (% WT)", 'orangered', 'external_depth.html', min_oddo, max_oddo)
# plot_depth_combined(internal_df_depth, external_df_depth, min_oddo, max_oddo, 'combined_depth.html')
# plot_depth_with_dropdown(internal_df_depth, external_df_depth, min_oddo, max_oddo, tick_vals, "depth_dropdown.html")


# # ================================ Orientations ================================

# Convert to Degrees
def clock_to_degrees(clock_str):
    try:
        h, m, s = map(int, str(clock_str).split(":"))
        return (h + m / 60 + s / 3600) % 12 * 30
    except:
        return None

df["Angle (deg)"] = df["Orientation O'clock"].apply(clock_to_degrees)
df.dropna(subset=["Angle (deg)", "Abs. Distance (m)", "Surface Location"], inplace=True)

# Prepare Data
internal_orientation_df = df[df["Surface Location"] == "Internal"]
external_orientation_df = df[df["Surface Location"] == "External"]

min_dist = df["Abs. Distance (m)"].min()
max_dist = df["Abs. Distance (m)"].max()

# # Call Function
# plot_orientation_with_dropdown(internal_orientation_df, external_orientation_df, min_dist, max_dist, "orientation_dropdown.html")


# # ================================                                            ================================


# from graph_plotter import plot_erf_3d

# plot_erf_3d(internal_df_erf, external_df_erf, "erf_3d_plot.html")
from graph_plotter import plot_erf_3d_bars

plot_erf_3d_bars(internal_df_erf, external_df_erf, "erf_3d_bar_graph.html")

