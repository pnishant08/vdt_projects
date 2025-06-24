# metal_loss_plot.py (Updated with full debug)

import pandas as pd
import plotly.graph_objects as go
import os
import numpy as np

#------------------------    Metal loss dynamic Graph       --------------------------------------

def plot_metal_loss(df, feature_type=None, dimension_class=None, return_fig=False):
    df.columns = df.columns.str.strip()
    print(f"[DEBUG] Initial dataframe shape: {df.shape}")

    #filter only metal loss
    df = df[df['Feature Type'].str.strip().str.lower() == 'metal loss']
    print(f"[DEBUG] After filtering Metal Loss: {df.shape}")
    
    #standardize strings
    df['Feature Identification'] = df['Feature Identification'].astype(str).str.strip()
    df['Dimension Classification'] = df['Dimension Classification'].astype(str).str.strip()

    print(f"[DEBUG] Unique Feature Identifications: {df['Feature Identification'].unique()}")
    print(f"[DEBUG] Unique Dimension Classifications: {df['Dimension Classification'].unique()}")
    
    #Filter by feature identifications 
    if feature_type:
        if feature_type == "Corrosion":
            df = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)]
            print(f"[DEBUG] After filtering Feature Identification (Corrosion): {df.shape}")
        elif feature_type == "MFG":
            df = df[df['Feature Identification'].str.contains('MFG', case=False, na=False)]
            print(f"[DEBUG] After filtering Feature Identification (MFG): {df.shape}")

    # filter by dimensions classifications
    if dimension_class and dimension_class != "ALL":
        df = df[df['Dimension Classification'].str.contains(dimension_class, case=False, na=False)]
        print(f"[DEBUG] After filtering Dimension Classification ({dimension_class}): {df.shape}")

    if df.empty:
        print("No matching defects found in the file.")
        return None
    
    #Define bin size
    bin_size = 500
    max_distance = df['Abs. Distance (m)'].max()
    bins = list(range(0, int(max_distance) + bin_size, bin_size))

    # bin_counts = df.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')
    # bin_counts['Bin Label'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))
    # df.loc[:, 'Distance Bin'] = pd.cut(df['Abs. Distance (m)'], bins=bins, right=True)


    # Assign 

    df.loc[:, 'Distance Bin'] = pd.cut(df['Abs. Distance (m)'], bins=bins, right=True)
    
    #Count records per bin
    bin_counts = df.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')
    bin_counts['Bin Start'] = bin_counts['Distance Bin'].apply(lambda x: int(x.left))
    bin_counts['Bin End'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))
    bin_counts['Bin Mid'] = bin_counts['Distance Bin'].apply(lambda x: (x.left + x.right) / 2)

    print(f"[DEBUG] Final bin counts:\n{bin_counts}")
    
    print(bin_counts[['Bin Start', 'Bin End', 'Bin Mid', 'Metal Loss Count']])
    
    # Debugging: Check customdata before passing to plotly
    customdata = bin_counts[['Bin Start', 'Bin End']].to_numpy()
    print("\n[DEBUG] Customdata to be passed to plotly (for hover):")
    print(customdata)
    
    #build bar plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bin_counts['Bin Mid'],
        y=bin_counts['Metal Loss Count'],
        width=[bin_size * 0.8] * len(bin_counts),
        marker_color='steelblue',
        hovertemplate='Distance Bin: %{customdata[0]} - %{customdata[1]} m<br>Metal Loss Count: %{y}<extra></extra>',
        customdata=bin_counts[['Bin Start', 'Bin End']],
        name='Metal Loss Defects'
    ))

    # Dynamic Y-axis title
    y_axis_title = "Number of"
    if feature_type:
        y_axis_title += f" {feature_type}"
    if dimension_class:
        y_axis_title += f" {dimension_class}"
    y_axis_title += " Metal Loss Defects"

    #final layout
    fig.update_layout(
        # title='Distribution of Metal Loss Defects Throughout the Pipeline Length',
        xaxis=dict(title='Distance from Launcher (ODDO) in meters', tickmode='linear', dtick=500, tickformat='d', gridcolor='lightgray'),
        yaxis=dict(title=y_axis_title , tick0=0, dtick=5, gridcolor='lightgray'),
        height=700,
        width=1600,
        template='plotly_white'
    )

    # save html
    html_path = os.path.abspath('metal_loss_graph.html')
    fig.write_html(html_path)

    if return_fig:
        return fig, html_path
    else:
        return html_path


#------------------------    end        --------------------------------------

#-----------------------    temperature graph------------------------------------

# def plot_temperature(df, return_fig=False):
#     df.columns = df.columns.str.strip()

#     #  Debug to check dataframe columns
#     print(f"[DEBUG] Dataframe columns: {df.columns.tolist()}")

#     # if 'Temperature (°C)' not in df.columns:
#     #     # If temperature column does not exist, create random data (you can remove this part if temperature already exists)
#     #     print("[INFO] Temperature column not found. Creating random temperature data.")
#     #     np.random.seed(0)  # For reproducibility
#     #     df['Temperature (°C)'] = np.random.uniform(low=20, high=80, size=len(df))

#     df.sort_values(by='Abs. Distance (m)', inplace=True)

#     fig = go.Figure()
#     fig.add_trace(go.Scatter(
#         x=df['Abs. Distance (m)'],
#         y=df['Temperature (°C)'],
#         mode='lines+markers',
#         name='Temperature',
#         line=dict(color='firebrick', width=2)
#     ))

#     fig.update_layout(
#         title='Temperature vs. Absolute Distance',
#         xaxis=dict(title='Absolute Distance (m)', gridcolor='lightgray'),
#         yaxis=dict(title='Temperature (°C)', gridcolor='lightgray'),
#         height=700,
#         width=1600,
#         template='plotly_white'
#     )

#     html_path = os.path.abspath('temperature_plot.html')
#     fig.write_html(html_path)

#     if return_fig:
#         return fig, html_path
#     else:
#         return html_path

#it is correct==============
def plot_temperature(df, return_fig=False):
    df.columns = df.columns.str.strip()
    df.sort_values(by='Abs. Distance (m)', inplace=True)

    # Calculate dynamic y-axis range
    # y_min = df['Temperature (°C)'].min() - 5
    # y_max = df['Temperature (°C)'].max() + 5

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Abs. Distance (m)'],
        y=df['Temperature (°C)'],
        mode='lines',
        name='Temperature Profile',
        line=dict(color='blue', width=2)
    ))

    fig.update_layout(
        title='Temperature Level Profile',
        xaxis=dict(title='Absolute Distance (m)', gridcolor='lightgray', dtick=2000),
        yaxis=dict(
            title='Temperature (°C)',
            gridcolor='lightgray',
            range=[0, 100],  
            dtick=20         
        ),
        height=700,
        width=1600,
        template='plotly_white'
    )

    html_path = os.path.abspath('temperature_plot.html')
    fig.write_html(html_path)

    if return_fig:
        return fig, html_path
    else:
        return html_path

#------------------------    end        --------------------------------------

# ------------------    sensor graph       -----------------------------------

def plot_sensor_percentage(df, return_fig=False):
    df.columns = df.columns.str.strip()

    # Debug to ensure correct columns
    print(f"[DEBUG] DataFrame Columns: {df.columns.tolist()}")

    # If Sensor % column does not exist, you can simulate or prompt the user to check
    # if 'Sensor %' not in df.columns:
    #     print("[INFO] 'Sensor %' column not found. Creating random sensor data.")
    #     import numpy as np
    #     np.random.seed(0)
    #     df['Sensor %'] = np.random.uniform(low=70, high=100, size=len(df))

    df.sort_values(by='Abs. Distance (m)', inplace=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Abs. Distance (m)'],
        y=df['Sensor %'],
        mode='lines',
        name='Sensor %',
        line=dict(color='green', width=2)
    ))

    fig.update_layout(
        title='Sensor % vs. Absolute Distance',
        xaxis=dict(title='Absolute Distance (m)', gridcolor='lightgray', dtick=2000),
        yaxis=dict(
            title='Sensor %',
            gridcolor='lightgray',
            range=[0, 100],  # 👉 Fixed Y-axis range
            dtick=20         # 👉 Y-axis ticks at 0, 20, 40, ..., 100
        ),
        height=700,
        width=1600,
        template='plotly_white'
    )

    html_path = os.path.abspath('sensor_percentage_plot.html')
    fig.write_html(html_path)

    if return_fig:
        return fig, html_path
    else:
        return html_path


#------------------------    end        --------------------------------------

#------------------------    ERF Graph        --------------------------------------
def plot_erf(df, view="Both",return_fig=False):
    df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()
    df['Abs. Distance (m)'] = df['Abs. Distance (m)'].round(1)
    df = df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).agg({'ERF (ASME B31G)': 'max'})
    df.sort_values(by='Abs. Distance (m)', inplace=True)

    min_oddo = int(df['Abs. Distance (m)'].min()) // 500 * 500
    max_oddo = int(df['Abs. Distance (m)'].max()) + 500
    y_max = df['ERF (ASME B31G)'].max() + 0.05

    fig = go.Figure()

    if view in ["Internal", "Both"]:
        internal_df = df[df['Surface Location'] == 'Internal']
        fig.add_trace(go.Bar(
            x=internal_df['Abs. Distance (m)'],
            y=internal_df['ERF (ASME B31G)'],
            name="Internal",
            marker_color='steelblue',
            width=[60]*len(internal_df)
        ))

    if view in ["External", "Both"]:
        external_df = df[df['Surface Location'] == 'External']
        fig.add_trace(go.Bar(
            x=external_df['Abs. Distance (m)'],
            y=external_df['ERF (ASME B31G)'],
            name="External",
            marker_color='orangered',
            width=[60]*len(external_df)
        ))

    fig.update_layout(
        title=f"ERF – {view} View",
        xaxis=dict(title="Distance from Launcher (ODDO) in meters", dtick=500, tickformat="~d"),
        yaxis=dict(title="ERF (ASME B31G)", range=[0, y_max], dtick=0.05),
        barmode="group",
        height=700,
        width=1600,
        template="plotly_white"
    )

    html_path = os.path.abspath("erf_plot.html")
    fig.write_html(html_path)
    # return html_path
    return fig, html_path


#------------------------    PSAFE Graph        --------------------------------------
def plot_psafe(df, view="Both",return_fig=False):
    df.columns = df.columns.str.strip()
    df.rename(columns={col: "Psafe (ASME B31G)" for col in df.columns if "Psafe" in col}, inplace=True)
    df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()
    df['Abs. Distance (m)'] = df['Abs. Distance (m)'].round(1)
    df = df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).agg({'Psafe (ASME B31G)': 'max'})
    df.sort_values(by='Abs. Distance (m)', inplace=True)

    min_oddo = int(df['Abs. Distance (m)'].min()) // 500 * 500
    max_oddo = int(df['Abs. Distance (m)'].max()) + 500
    y_max = df['Psafe (ASME B31G)'].max() + 10

    fig = go.Figure()

    if view in ["Internal", "Both"]:
        internal_df = df[df['Surface Location'] == 'Internal']
        fig.add_trace(go.Bar(
            x=internal_df['Abs. Distance (m)'],
            y=internal_df['Psafe (ASME B31G)'],
            name="Internal",
            marker_color='steelblue',
            width=[60]*len(internal_df)
        ))

    if view in ["External", "Both"]:
        external_df = df[df['Surface Location'] == 'External']
        fig.add_trace(go.Bar(
            x=external_df['Abs. Distance (m)'],
            y=external_df['Psafe (ASME B31G)'],
            name="External",
            marker_color='orangered',
            width=[60]*len(external_df)
        ))

    fig.update_layout(
        title=f"Psafe – {view} View",
        xaxis=dict(title="Distance from Launcher (ODDO) in meters", dtick=500, tickformat="~d"),
        yaxis=dict(title="Psafe (ASME B31G) in kg/cm²", range=[0, y_max], dtick=50),
        barmode="group",
        height=700,
        width=1600,
        template="plotly_white"
    )

    html_path = os.path.abspath("psafe_plot.html")
    fig.write_html(html_path)
    # return html_path
    return fig, html_path



#------------------------    Orientation Graph        --------------------------------------
def clock_to_degrees(clock_str):
    try:
        h, m, s = map(int, str(clock_str).split(":"))
        decimal = h + m / 60 + s / 3600
        return (decimal % 12) * 30
    except:
        return None

def degrees_to_clock(deg):
    total_seconds = deg / 30 * 3600
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

def plot_orientation(df, view="Both",return_fig=False):
    df.columns = df.columns.str.strip()
    df['Angle (deg)'] = df['Orientation O\'clock'].apply(clock_to_degrees)
    df.dropna(subset=['Angle (deg)', 'Abs. Distance (m)', 'Surface Location'], inplace=True)

    min_dist = df['Abs. Distance (m)'].min()
    max_dist = df['Abs. Distance (m)'].max()

    fig = go.Figure()

    if view in ["Internal", "Both"]:
        internal_df = df[df['Surface Location'] == 'Internal']
        fig.add_trace(go.Scatter(
            x=internal_df['Abs. Distance (m)'],
            y=internal_df['Angle (deg)'],
            mode="markers",
            name="Internal",
            marker=dict(color="steelblue", size=6, symbol="triangle-up"),
            hovertemplate="Internal<br>Distance: %{x} m<br>Orientation: %{customdata}",
            customdata=internal_df['Angle (deg)'].apply(degrees_to_clock)
        ))

    if view in ["External", "Both"]:
        external_df = df[df['Surface Location'] == 'External']
        fig.add_trace(go.Scatter(
            x=external_df['Abs. Distance (m)'],
            y=external_df['Angle (deg)'],
            mode="markers",
            name="External",
            marker=dict(color="orangered", size=6, symbol="triangle-up"),
            hovertemplate="External<br>Distance: %{x} m<br>Orientation: %{customdata}",
            customdata=external_df['Angle (deg)'].apply(degrees_to_clock)
        ))

    fig.update_layout(
        title=f"Orientation vs Distance – {view} View",
        xaxis=dict(title="Distance from Launcher (ODDO) in meters", dtick=500, tickformat="~d"),
        yaxis=dict(title="Circumferential Orientation (o\'clock)", tickvals=[i*30 for i in range(13)], ticktext=[f"{i:02}:00:00" for i in range(13)]),
        height=700,
        width=1600,
        template="plotly_white"
    )

    html_path = os.path.abspath("orientation_plot.html")
    fig.write_html(html_path)
    # return html_path
    return fig, html_path


#------------------------    Depth Graph        --------------------------------------
def plot_depth(df, view="Both",return_fig=False):
    df.columns = df.columns.str.strip()
    df.rename(columns={col: "Depth % WT" for col in df.columns if "Depth" in col}, inplace=True)
    df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()
    df['Abs. Distance (m)'] = df['Abs. Distance (m)'].round(1)
    df = df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).agg({'Depth % WT': 'max'})
    df.sort_values(by='Abs. Distance (m)', inplace=True)

    min_oddo = int(df['Abs. Distance (m)'].min()) // 500 * 500
    max_oddo = int(df['Abs. Distance (m)'].max()) + 500
    y_max = df['Depth % WT'].max() + 10

    fig = go.Figure()

    if view in ["Internal", "Both"]:
        internal_df = df[df['Surface Location'] == 'Internal']
        fig.add_trace(go.Bar(
            x=internal_df['Abs. Distance (m)'],
            y=internal_df['Depth % WT'],
            name="Internal",
            marker_color='steelblue',
            width=[60]*len(internal_df),
            showlegend=True
        ))

    if view in ["External", "Both"]:
        external_df = df[df['Surface Location'] == 'External']
        fig.add_trace(go.Bar(
            x=external_df['Abs. Distance (m)'],
            y=external_df['Depth % WT'],
            name="External",
            marker_color='orangered',
            width=[60]*len(external_df),
            showlegend=True
        ))

    fig.update_layout(
        title="",
        xaxis=dict(title="Distance from Launcher (ODDO) in m", dtick=500, tickformat="~d"),
        yaxis=dict(title="Depth (% WT)", range=[0, y_max], dtick=5),
        barmode="group",
        height=700,
        width=1600,
        template="plotly_white"
    )

    html_path = os.path.abspath("depth_plot.html")
    fig.write_html(html_path)
    # return html_path
    return fig, html_path
