import pandas as pd
import plotly.graph_objects as go
import numpy as np
import webbrowser
import os

# Load data
file_path = r"C:\Users\pnish\Desktop\erf-oddo.xlsx"
df = pd.read_excel(file_path)

# Clean and prepare
df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()
df.sort_values(by='Abs. Distance (m)', inplace=True)
df['x_index'] = np.arange(len(df)) *2  # Add spacing between bars
df.reset_index(drop=True, inplace=True)

# Split
internal_df = df[df['Surface Location'] == 'Internal'].copy()
external_df = df[df['Surface Location'] == 'External'].copy()

# Function to plot and open in browser
def plot_and_open(df_plot, title, color, filename):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_plot['x_index'],
        y=df_plot['ERF (ASME B31G)'],
        width=[2.0] * len(df_plot),
        marker_color=color,
        name=title
    ))

    # Customize x-ticks with real ODDO values
    tick_count = 25 if len(df_plot) > 25 else len(df_plot)
    tick_indices = np.linspace(0, len(df_plot) - 1, tick_count, dtype=int)
    fig.update_layout(
        title=title,
        xaxis=dict(
            tickmode='array',
            tickvals=df_plot['x_index'].iloc[tick_indices],
            ticktext=df_plot['Abs. Distance (m)'].iloc[tick_indices].round(0).astype(str).values,
            title='Distance from Launcher (ODDO) in meters'
        ),
        yaxis=dict(title='ERF (ASME B31G)'),
        height=700,
        width=1600,
        template='plotly_white'
    )

    # Save & Open
    html_path = os.path.abspath(filename)
    fig.write_html(html_path)
    webbrowser.open(f'file://{html_path}')

# Plot Internal
plot_and_open(internal_df, "Internal Defects – 2D Bar Graph", 'steelblue', 'internal_erf.html')

# Plot External
plot_and_open(external_df, "External Defects – 2D Bar Graph", 'orangered', 'external_erf.html')

# Plot Combined
fig = go.Figure()
fig.add_trace(go.Bar(
    x=internal_df['x_index'],
    y=internal_df['ERF (ASME B31G)'],
    width=[2.0] * len(internal_df),
    marker_color='steelblue',
    name='Internal'
))
fig.add_trace(go.Bar(
    x=external_df['x_index'],
    y=external_df['ERF (ASME B31G)'],
    width=[2.0] * len(external_df),
    marker_color='orangered',
    name='External'
))

tick_count = 25 if len(df) > 25 else len(df)
tick_indices = np.linspace(0, len(df) - 1, tick_count, dtype=int)
fig.update_layout(
    title="Combined Internal & External Defects – 2D Bar Graph",
    xaxis=dict(
        tickmode='array',
        tickvals=df['x_index'].iloc[tick_indices],
        ticktext=df['Abs. Distance (m)'].iloc[tick_indices].round(0).astype(str).values,
        title='Distance from Launcher (ODDO) in meters'
    ),
    yaxis=dict(title='ERF (ASME B31G)'),
    barmode='group',
    height=700,
    width=1600,
    template='plotly_white'
)

html_path_combined = os.path.abspath('combined_erf.html')
fig.write_html(html_path_combined)
webbrowser.open(f'file://{html_path_combined}')