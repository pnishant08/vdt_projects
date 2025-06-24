import pandas as pd
import plotly.graph_objects as go
import os

def plot_metal_loss(df, feature_type=None, dimension_class=None, return_fig=False):
    df.columns = df.columns.str.strip()
    print(f"[DEBUG] Initial dataframe shape: {df.shape}")

    # Filter only Metal Loss records
    df = df[df['Feature Type'].str.strip().str.lower() == 'metal loss']
    print(f"[DEBUG] After filtering Metal Loss: {df.shape}")

    # Standardize strings
    df['Feature Identification'] = df['Feature Identification'].astype(str).str.strip()
    df['Dimension Classification'] = df['Dimension Classification'].astype(str).str.strip()

    print(f"[DEBUG] Unique Feature Identifications: {df['Feature Identification'].unique()}")
    print(f"[DEBUG] Unique Dimension Classifications: {df['Dimension Classification'].unique()}")

    # Filter by Feature Identification if specified
    if feature_type:
        if feature_type == "Corrosion":
            df = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)]
            print(f"[DEBUG] After filtering Feature Identification (Corrosion): {df.shape}")
        elif feature_type == "MFG":
            df = df[df['Feature Identification'].str.contains('MFG', case=False, na=False)]
            print(f"[DEBUG] After filtering Feature Identification (MFG): {df.shape}")

    # Filter by Dimension Classification if specified
    if dimension_class and dimension_class != "ALL":
        df = df[df['Dimension Classification'].str.contains(dimension_class, case=False, na=False)]
        print(f"[DEBUG] After filtering Dimension Classification ({dimension_class}): {df.shape}")

    if df.empty:
        print("No matching defects found in the file.")
        return None

    # Define bins
    bin_size = 500
    max_distance = df['Abs. Distance (m)'].max()
    bins = list(range(0, int(max_distance) + bin_size, bin_size))

    # Assign bins
    df.loc[:, 'Distance Bin'] = pd.cut(df['Abs. Distance (m)'], bins=bins, right=True)

    # Count records per bin
    bin_counts = df.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')
    bin_counts['Bin Start'] = bin_counts['Distance Bin'].apply(lambda x: int(x.left))
    bin_counts['Bin End'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))
    bin_counts['Bin Mid'] = bin_counts['Distance Bin'].apply(lambda x: (x.left + x.right) / 2)

    print(f"[DEBUG] Final bin counts:\n{bin_counts}")

    # Build bar plot
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

    # Final layout
    fig.update_layout(
        xaxis=dict(
            title='Distance from Launcher (ODDO) in meters',
            tickmode='linear',
            dtick=500,
            tickformat='d',
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title=y_axis_title,
            tick0=0,
            dtick=5,
            gridcolor='lightgray'
        ),
        height=700,
        width=1600,
        template='plotly_white'
    )

    # Save HTML
    html_path = os.path.abspath('metal_loss_graph.html')
    fig.write_html(html_path)

    if return_fig:
        return fig, html_path
    else:
        return html_path