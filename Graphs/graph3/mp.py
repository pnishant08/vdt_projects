import pandas as pd
import plotly.graph_objects as go
import os

def plot_metal_loss(df, feature_type=None, dimension_class=None, return_fig=False):
    df.columns = df.columns.str.strip()
    #  Debug initial dataframe size 
    # print(f"[DEBUG] Initial dataframe shape: {df.shape}")-->Initial dataframe shape: (1621, 18)

    df = df[df['Feature Type'].str.strip().str.lower() == 'metal loss']
    #  Debug after filtering Metal Loss
    # print(f"[DEBUG] After filtering Metal Loss: {df.shape}")-->After filtering Metal Loss: (701, 18)

    #  Debug unique Feature Identifications
    # print(f"[DEBUG] Unique Feature Identifications: {df['Feature Identification'].unique()}")--->Unique Feature Identifications: ['Corrosion' 'MFG']

    df['Feature Identification'] = df['Feature Identification'].astype(str).str.strip()
    df['Dimension Classification'] = df['Dimension Classification'].astype(str).str.strip()

    # Filter Metal Loss rows
    df = df[df['Feature Type'].str.contains('Metal Loss', case=False, na=False)].copy()

    if feature_type == "Corrosion":
        df = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)]
        #  Debug after filtering by Feature Identification
        # print(f"[DEBUG] After filtering Feature Identification ({feature_type}): {df.shape}")
    elif feature_type == "MFG":
        df = df[df['Feature Identification'].str.contains('MFG', case=False, na=False)]
    # If feature_type is None or 'Both', we keep all metal loss records

    if dimension_class and dimension_class != "ALL":
        df = df[df['Dimension Classification'].str.contains(dimension_class, case=False, na=False)]

    if df.empty:
        print("No matching defects found in the file.")
        return None

    # Group by bins
    bin_size = 500
    max_distance = df['Abs. Distance (m)'].max()
    bins = list(range(0, int(max_distance) + bin_size, bin_size))
    df.loc[:, 'Distance Bin'] = pd.cut(df['Abs. Distance (m)'], bins=bins, right=True)

    bin_counts = df.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')
    bin_counts['Bin Label'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bin_counts['Bin Label'],
        y=bin_counts['Metal Loss Count'],
        width=[bin_size * 0.8] * len(bin_counts),
        marker_color='steelblue',
        hovertemplate='Distance Bin: 0 - %{x} m<br>Metal Loss Count: %{y}<extra></extra>',
        name='Metal Loss Defects'
    ))

    fig.update_layout(
        title='Distribution of Metal Loss Defects Throughout the Pipeline Length',
        xaxis=dict(
            title='Distance from Launcher (ODDO) in meters',
            tickmode='linear',
            dtick=500,
            tickformat='d',
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title='Number of Metal Loss Defects',
            tick0=0,
            dtick=5,
            gridcolor='lightgray'
        ),
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
