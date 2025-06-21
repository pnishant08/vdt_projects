# metal_loss_plot.py (Updated with full debug)

import pandas as pd
import plotly.graph_objects as go
import os

def plot_metal_loss(df, feature_type=None, dimension_class=None, return_fig=False):
    df.columns = df.columns.str.strip()
    print(f"[DEBUG] Initial dataframe shape: {df.shape}")

    df = df[df['Feature Type'].str.strip().str.lower() == 'metal loss']
    print(f"[DEBUG] After filtering Metal Loss: {df.shape}")

    df['Feature Identification'] = df['Feature Identification'].astype(str).str.strip()
    df['Dimension Classification'] = df['Dimension Classification'].astype(str).str.strip()

    print(f"[DEBUG] Unique Feature Identifications: {df['Feature Identification'].unique()}")
    print(f"[DEBUG] Unique Dimension Classifications: {df['Dimension Classification'].unique()}")

    if feature_type:
        if feature_type == "Corrosion":
            df = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)]
            print(f"[DEBUG] After filtering Feature Identification (Corrosion): {df.shape}")
        elif feature_type == "MFG":
            df = df[df['Feature Identification'].str.contains('MFG', case=False, na=False)]
            print(f"[DEBUG] After filtering Feature Identification (MFG): {df.shape}")

    if dimension_class and dimension_class != "ALL":
        df = df[df['Dimension Classification'].str.contains(dimension_class, case=False, na=False)]
        print(f"[DEBUG] After filtering Dimension Classification ({dimension_class}): {df.shape}")

    if df.empty:
        print("No matching defects found in the file.")
        return None

    bin_size = 500
    max_distance = df['Abs. Distance (m)'].max()
    bins = list(range(0, int(max_distance) + bin_size, bin_size))
    df.loc[:, 'Distance Bin'] = pd.cut(df['Abs. Distance (m)'], bins=bins, right=True)

    bin_counts = df.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')
    bin_counts['Bin Label'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))

    print(f"[DEBUG] Final bin counts:\n{bin_counts}")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bin_counts['Bin Label'],
        y=bin_counts['Metal Loss Count'],
        width=[bin_size * 0.8] * len(bin_counts),
        marker_color='steelblue',
        hovertemplate='Distance Bin: 0 - %{x} m<br>Metal Loss Count: %{y}<extra></extra>',
        name='Metal Loss Defects'
    ))
    # Dynamic Y-axis title
    y_axis_title = "Number of"
    if feature_type:
        y_axis_title += f" {feature_type}"
    if dimension_class:
        y_axis_title += f" {dimension_class}"
    y_axis_title += " Metal Loss Defects"

    fig.update_layout(
        # title='Distribution of Metal Loss Defects Throughout the Pipeline Length',
        xaxis=dict(title='Distance from Launcher (ODDO) in meters', tickmode='linear', dtick=500, tickformat='d', gridcolor='lightgray'),
        yaxis=dict(title=y_axis_title , tick0=0, dtick=5, gridcolor='lightgray'),
        height=700,
        width=1600,
        template='plotly_white'
    )

    html_path = os.path.abspath('metal_loss_graph.html')
    fig.write_html(html_path)

    if return_fig:
        return fig, html_path
    else:
        return html_path
