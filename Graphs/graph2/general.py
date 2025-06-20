import pandas as pd
import plotly.graph_objects as go
import os

def plot_general(df,return_fig=False):
    df.columns = df.columns.str.strip()
    df['Dimension Classification'] = df['Dimension Classification'].astype(str).str.strip()

    # Filter only General features
    df_general = df[df['Dimension Classification'].str.contains('GENERAL', case=False, na=False)].copy()

    if df_general.empty:
        print("No GENERAL defects found in the file.")
        return None

    # Define bin edges (500-meter intervals)
    bin_size = 500
    max_distance = df_general['Abs. Distance (m)'].max()
    bins = list(range(0, int(max_distance) + bin_size, bin_size))

    # Assign bins using .loc to avoid SettingWithCopyWarning
    df_general.loc[:, 'Distance Bin'] = pd.cut(df_general['Abs. Distance (m)'], bins=bins, right=True)

    # Group by bins (with observed=False to suppress FutureWarning)
    bin_counts = df_general.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')

    # Extract bin labels as upper edges
    bin_counts['Bin Label'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bin_counts['Bin Label'],
        y=bin_counts['Metal Loss Count'],
        width=[bin_size * 0.5] * len(bin_counts),
        marker_color='steelblue',
        hovertemplate='Distance Bin: 0 - %{x} m<br>Metal Loss Count: %{y}<extra></extra>',
        name='General Metal Loss'
    ))

    fig.update_layout(
        title='Distribution of General Metal Loss Throughout the Pipeline Length',
        xaxis=dict(
            title='Distance from Launcher (ODDO) in meters',
            tickmode='linear',
            dtick=500,
            tickformat='d',
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title='Number of General Metal Loss Defects',
            tick0=0,
            range=[0, max(5, bin_counts['Metal Loss Count'].max() + 1)],
            dtick=5,
            gridcolor='lightgray'
        ),
        height=700,
        width=1600,
        template='plotly_white'
    )

    html_path = os.path.abspath('general_binned_graph.html')
    fig.write_html(html_path)
    # return html_path
    return fig, html_path
