
import pandas as pd
import plotly.graph_objects as go
import os

def plot_pitting(df,return_fig=False):
    df.columns = df.columns.str.strip()
    df['Dimension Classification'] = df['Dimension Classification'].astype(str).str.strip()

    # Filter only Pitting features
    df_pitting = df[df['Dimension Classification'].str.contains('Pitting', case=False, na=False)].copy()

    if df_pitting.empty:
        print("No pitting defects found in the file.")
        return None

    # Define bin edges (500-meter intervals)
    bin_size = 500
    max_distance = df_pitting['Abs. Distance (m)'].max()
    bins = list(range(0, int(max_distance) + bin_size, bin_size))

    # Assign bins using .loc to avoid SettingWithCopyWarning
    df_pitting.loc[:, 'Distance Bin'] = pd.cut(df_pitting['Abs. Distance (m)'], bins=bins, right=True)

    # Group by bins (with observed=False to suppress FutureWarning)
    bin_counts = df_pitting.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')

    # Extract bin labels as upper edges
    bin_counts['Bin Label'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bin_counts['Bin Label'],
        y=bin_counts['Metal Loss Count'],
        width=[bin_size * 0.8] * len(bin_counts),
        marker_color='steelblue',
        hovertemplate='Distance Bin: 0 - %{x} m<br>Metal Loss Count: %{y}<extra></extra>',
        name='Pitting Metal Loss'
    ))

    fig.update_layout(
        title='Distribution of Pitting Metal Loss in Pipeline Length',
        xaxis=dict(
            title='Distance from Launcher (ODDO) in meters',
            tickmode='linear',
            dtick=500,
            tickformat='d',
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title='Number of Metal Loss due to Pitting',
            tick0=0,
            dtick=5,
            gridcolor='lightgray'
        ),
        height=700,
        width=1600,
        template='plotly_white'
    )

    html_path = os.path.abspath('pitting_binned_graph.html')
    fig.write_html(html_path)
    # return html_path
    return fig, html_path
