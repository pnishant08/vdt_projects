import pandas as pd
import plotly.graph_objects as go
import os

def plot_corrosion(df,return_fig=False):
    # Correct column and string cleaning
    df.columns = df.columns.str.strip()  # You wrote df.coloumns (wrong spelling)
    df["Feature Identification"] = df["Feature Identification"].astype(str).str.strip()

    # Correct column name and spelling
    df_corrosion = df[df['Feature Identification'].str.contains('Corrosion', case=False, na=False)].copy()

    if df_corrosion.empty:
        print("No corrosion defects found in the file.")
        return None

    # Binning logic
    bin_size = 500
    max_distance = df_corrosion['Abs. Distance (m)'].max()
    bins = list(range(0, int(max_distance) + bin_size, bin_size))

    df_corrosion.loc[:, 'Distance Bin'] = pd.cut(df_corrosion['Abs. Distance (m)'], bins=bins, right=True)

    bin_counts = df_corrosion.groupby('Distance Bin', observed=False).size().reset_index(name='Metal Loss Count')
    bin_counts['Bin Label'] = bin_counts['Distance Bin'].apply(lambda x: int(x.right))

    # Plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bin_counts['Bin Label'],
        y=bin_counts['Metal Loss Count'],
        width=[bin_size * 0.8] * len(bin_counts),
        marker_color='steelblue',
        hovertemplate='Distance Bin: 0 - %{x} m<br>Metal Loss Count: %{y}<extra></extra>',
        name='Corrosion Metal Loss'
    ))

    fig.update_layout(
        title='Distribution of Corrosion Metal Loss Throughout the Pipeline Length',
        xaxis=dict(
            title='Distance from Launcher (ODDO) in meters',
            tickmode='linear',
            dtick=500,
            tickformat='d',
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title='Number of Metal Loss due to Corrosion',
            tick0=0,
            dtick=10,
            gridcolor='lightgray'
        ),
        height=700,
        width=1600,
        template='plotly_white'
    )

    html_path = os.path.abspath('corrosion_binned_graph.html')
    fig.write_html(html_path)
    # return html_path
    return fig, html_path
