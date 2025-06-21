import pandas as pd
import plotly.graph_objects as go
import os

def plot_metal_loss(df, feature_type=None, dimension_class=None, return_fig=False):
    df.columns = df.columns.str.strip()
    df['Feature Identification'] = df['Feature Identification'].astype(str).str.strip()
    df['Dimension Classification'] = df['Dimension Classification'].astype(str).str.strip()

    # Filter Metal Loss rows
    df = df[df['Feature Type'].str.contains('Metal Loss', case=False, na=False)].copy()

    # Filter based on Feature Identification
    if feature_type == "Corrosion":
        df = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)]
    elif feature_type == "MFG":
        df = df[df['Feature Identification'].str.contains('MFG', case=False, na=False)]
    # If feature_type is None or 'Both', we keep all metal loss records

    # Filter based on Dimensional Classification
    if dimension_class and dimension_class != "ALL":
        df = df[df['Dimension Classification'].str.contains(dimension_class, case=False, na=False)]

    if df.empty:
        print("No matching defects found in the file.")
        return None

    # Group by bins for the graph
    bin_size = 500
    max_distance = df['Abs. Distance (m)'].max()
    bins = list(range(0, int(max_distance) + bin_size, bin_size))
    df.loc[:, 'Distance Bin'] = pd.cut(df['Abs. Distance (m)'], bins=bins, right=True)

    bin_counts = df.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')
    bin_counts['Bin Label'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))


    # Set dynamic titles and labels based on selected feature and dimensional classification
    if feature_type == "Corrosion":
        # title = "Distribution of Corrosion Metal Loss Defects Throughout the Pipeline Length"
        yaxis_title = "Number of Corrosion Metal Loss Defects"
    elif feature_type == "MFG":
        # title = "Distribution of MFG Metal Loss Defects Throughout the Pipeline Length"
        yaxis_title = "Number of MFG Metal Loss Defects"
    else:
        # title = "Distribution of Metal Loss Defects Throughout the Pipeline Length"
        yaxis_title = "Number of Metal Loss Defects"

    # Update title and labels based on Dimensional Classification
    if dimension_class:
        if dimension_class == "Pitting":
            # title += " - Pitting Classification"
            yaxis_title = "Number of Pitting Metal Loss Defects"
        elif dimension_class == "Axial Grooving":
            # title += " - Axial Grooving Classification"
            yaxis_title = "Number of Axial Grooving Metal Loss Defects"
        elif dimension_class == "Axial Slotting":
            # title += " - Axial Slotting Classification"
            yaxis_title = "Number of Axial Slotting Metal Loss Defects"
        elif dimension_class == "Circumferential Grooving":
            # title += " - Circumferential Grooving Classification"
            yaxis_title = "Number of Circumferential Grooving Metal Loss Defects"
        elif dimension_class == "Circumferential Slotting":
            # title += " - Circumferential Slotting Classification"
            yaxis_title = "Number of Circumferential Slotting Metal Loss Defects"
        elif dimension_class == "Pinhole":
            # title += " - Pinhole Classification"
            yaxis_title = "Number of Pinhole Metal Loss Defects"
        elif dimension_class == "General":
            # title += " - General Classification"
            yaxis_title = "Number of General Metal Loss Defects"
        elif dimension_class == "Both":
            # title += " - All Classification"
            yaxis_title = "Total Number of Metal Loss Defects"
    print(f"[DEBUG] Final bin counts:\n{bin_counts}")
    # Plotting the graph
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bin_counts['Bin Label'],
        y=bin_counts['Metal Loss Count'],
        width=[bin_size * 0.8] * len(bin_counts),
        marker_color='steelblue',
        hovertemplate='Distance Bin: 0 - %{x} m<br>Metal Loss Count: %{y}<extra></extra>',
        name=f'{feature_type} Metal Loss Defects' if feature_type else 'Metal Loss Defects'
    ))

    fig.update_layout(
        # title=title,
        xaxis=dict(
            title='Distance from Launcher (ODDO) in meters',
            tickmode='linear',
            dtick=500,
            tickformat='d',
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title=yaxis_title,
            tick0=0,
            dtick=5,
            gridcolor='lightgray'
        ),
        height=700,
        width=1600,
        template='plotly_white'
    )

    # Save the plot as an HTML file
    html_path = os.path.abspath('metal_loss_graph.html')
    fig.write_html(html_path)

    if return_fig:
        return fig, html_path
    else:
        return html_path