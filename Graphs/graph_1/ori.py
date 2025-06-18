# import pandas as pd
# import plotly.graph_objects as go
# import os
# import webbrowser
#
# # Step 1: Load data
# file_path = r"C:\Users\manvi\OneDrive\Documents\orientation_combined.xlsx"
# df = pd.read_excel(file_path)
# df.columns = df.columns.str.strip()
#
# # Step 2: Convert clock to angle (in degrees)
# def clock_to_degrees(clock_str):
#     try:
#         h, m, s = map(int, str(clock_str).split(":"))
#         decimal_hours = h + m / 60 + s / 3600
#         return (decimal_hours % 12) * 30
#     except:
#         return None
#
# df["Angle (deg)"] = df["Orientation O'clock"].apply(clock_to_degrees)
# df = df.dropna(subset=["Angle (deg)", "Abs. Distance (m)", "Surface Location"])
#
# # Split into internal and external
# internal_df = df[df["Surface Location"] == "Internal"]
# external_df = df[df["Surface Location"] == "External"]
#
# # Axis ranges
# min_dist = df["Abs. Distance (m)"].min()
# max_dist = df["Abs. Distance (m)"].max()
# min_angle = 0
# max_angle = 360
#
# # Reusable plot function
# def plot_orientation(data, title, color, filename):
#     fig = go.Figure()
#
#     fig.add_trace(go.Scatter(
#         x=data["Abs. Distance (m)"],
#         y=data["Angle (deg)"],
#         mode="markers",
#         marker=dict(color=color, size=6, symbol="triangle-up"),
#         name=title,
#         hovertemplate="Distance: %{x} m<br>Orientation: %{y}°<extra></extra>"
#     ))
#
#     fig.update_layout(
#         title=title,
#         xaxis=dict(
#             title="Distance from Launcher (ODDO) in meters",
#             range=[min_dist, max_dist],
#             tickformat="~d",
#             dtick=500,
#             tickmode="linear"
#         ),
#         yaxis=dict(title="Circumferential Orientation (°)", range=[min_angle, max_angle], dtick=30),
#         template="plotly_white",
#         height=700,
#         width=1400,
#     )
#
#     output_path = os.path.abspath(filename)
#     fig.write_html(output_path)
#     webbrowser.open(f"file://{output_path}")
#
# # Internal
# plot_orientation(internal_df, "Orientation vs Distance – Internal", "steelblue", "orientation_internal.html")
#
# # External
# plot_orientation(external_df, "Orientation vs Distance – External", "orangered", "orientation_external.html")
#
# # Combined Plot
# fig = go.Figure()
#
# fig.add_trace(go.Scatter(
#     x=internal_df["Abs. Distance (m)"],
#     y=internal_df["Angle (deg)"],
#     mode="markers",
#     marker=dict(color="steelblue", size=6, symbol="triangle-up"),
#     name="Internal"
# ))
#
# fig.add_trace(go.Scatter(
#     x=external_df["Abs. Distance (m)"],
#     y=external_df["Angle (deg)"],
#     mode="markers",
#     marker=dict(color="orangered", size=6, symbol="triangle-up"),
#     name="External"
# ))
#
# fig.update_layout(
#     title="Orientation vs Distance – Combined",
#     xaxis=dict(
#         title="Distance from Launcher (ODDO) in meters",
#         range=[min_dist, max_dist],
#         tickformat="~d",
#         dtick=500,
#         tickmode="linear"
#     ),
#     yaxis=dict(title="Circumferential Orientation (°)", range=[min_angle, max_angle], dtick=30),
#     template="plotly_white",
#     height=700,
#     width=1400,
# )
#
# combined_path = os.path.abspath("orientation_combined.html")
# fig.write_html(combined_path)
# webbrowser.open(f"file://{combined_path}")




import pandas as pd
import plotly.graph_objects as go
import os
import webbrowser

# Load data
# file_path = r"C:\Users\manvi\OneDrive\Documents\orientation_combined.xlsx"
file_path = r"C:\Users\pnish\Desktop\graph data.xlsx"

df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

# Convert Orientation O'clock to degrees
def clock_to_degrees(clock_str):
    try:
        h, m, s = map(int, str(clock_str).split(":"))
        return (h + m / 60 + s / 3600) % 12 * 30
    except:
        return None

df["Angle (deg)"] = df["Orientation O'clock"].apply(clock_to_degrees)
df.dropna(subset=["Angle (deg)", "Abs. Distance (m)", "Surface Location"], inplace=True)

# Split datasets
internal_df = df[df["Surface Location"] == "Internal"]
external_df = df[df["Surface Location"] == "External"]

# Axis ranges
min_dist = df["Abs. Distance (m)"].min()
max_dist = df["Abs. Distance (m)"].max()

# Create figure with 3 traces
fig = go.Figure()

# Internal
fig.add_trace(go.Scatter(
    x=internal_df["Abs. Distance (m)"],
    y=internal_df["Angle (deg)"],
    mode="markers",
    name="Internal",
    marker=dict(color="steelblue", size=6, symbol="triangle-up"),
    hovertemplate="Internal<br>Distance: %{x} m<br>Orientation: %{y}°<extra></extra>"
))

# External
fig.add_trace(go.Scatter(
    x=external_df["Abs. Distance (m)"],
    y=external_df["Angle (deg)"],
    mode="markers",
    name="External",
    marker=dict(color="orangered", size=6, symbol="triangle-up"),
    hovertemplate="External<br>Distance: %{x} m<br>Orientation: %{y}°<extra></extra>"
))

# Update layout with dropdown
fig.update_layout(
    title="Orientation vs Distance – Interactive View",
    xaxis=dict(
        title="Distance from Launcher (ODDO) in meters",
        range=[min_dist, max_dist],
        tickformat="~d",
        dtick=500,
        tickmode="linear"
    ),
    yaxis=dict(title="Circumferential Orientation (°)", range=[0, 360], dtick=30),
    template="plotly_white",
    height=700,
    width=1400,
    updatemenus=[
        dict(
            type="dropdown",
            direction="down",
            x=1.15,
            y=1.1,
            showactive=True,
            buttons=[
                dict(label="Internal Only", method="update", args=[{"visible": [True, False]}, {"title": "Orientation vs Distance – Internal"}]),
                dict(label="External Only", method="update", args=[{"visible": [False, True]}, {"title": "Orientation vs Distance – External"}]),
                dict(label="Both", method="update", args=[{"visible": [True, True]}, {"title": "Orientation vs Distance – Combined"}]),
            ],
        )
    ]
)

# Save and open
output_path = os.path.abspath("orientation_dropdown.html")
fig.write_html(output_path)
webbrowser.open(f"file://{output_path}")