
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import webbrowser
import os

# Load Excel data
# file_path = r"C:\Users\pnish\Desktop\erf-oddo.xlsx"
# file_path = r"C:\Users\pnish\Desktop\erf2data.xlsx"
file_path = r"C:\Users\pnish\Desktop\graph data.xlsx"
df = pd.read_excel(file_path)

# Filter and sort
df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()
df.sort_values(by='Abs. Distance (m)', inplace=True)

# Split
internal_df = df[df['Surface Location'] == 'Internal'].copy()
external_df = df[df['Surface Location'] == 'External'].copy()

# General tick setup for ODDO distance (every 500m)
min_oddo = int(df['Abs. Distance (m)'].min()) // 500 * 500
max_oddo = int(df['Abs. Distance (m)'].max()) + 500
tick_vals = list(range(min_oddo, max_oddo, 500))

# Function to plot with real ODDO as X-axis
def plot_real_oddo(df_plot, title, color, filename):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_plot['Abs. Distance (m)'],
        y=df_plot['ERF (ASME B31G)'],
        width=[40] * len(df_plot),
        marker_color=color,
        name=title
    ))

    fig.update_layout(
        title=title,
        xaxis=dict(
            tickmode='array',
            tickvals=tick_vals,
            ticktext=[str(val) for val in tick_vals],
            title='Distance from Launcher (ODDO) in meters',
            range=[min_oddo - 100, max_oddo + 100]
        ),
        yaxis=dict(
            title='ERF (ASME B31G)',
            tick0=0,
            dtick=0.05,
            range=[0, df_plot['ERF (ASME B31G)'].max() + 0.05]
        ),
        height=700,
        width=1600,
        template='plotly_white'
    )

    html_path = os.path.abspath(filename)
    fig.write_html(html_path)
    webbrowser.open(f'file://{html_path}')

# Plot Internal
plot_real_oddo(internal_df, "Internal Defects – Real ODDO Spacing", 'steelblue', 'internal_real_oddo.html')

# Plot External
plot_real_oddo(external_df, "External Defects – Real ODDO Spacing", 'orangered', 'external_real_oddo.html')

# Plot Combined
fig = go.Figure()
fig.add_trace(go.Bar(
    x=internal_df['Abs. Distance (m)'],
    y=internal_df['ERF (ASME B31G)'],
    width=[100] * len(internal_df),  # Increased thickness
    marker_color='steelblue',
    name='Internal'
))
fig.add_trace(go.Bar(
    x=external_df['Abs. Distance (m)'],
    y=external_df['ERF (ASME B31G)'],
    width=[60] * len(external_df),  # Increased thickness
    marker_color='orangered',
    name='External'
))


fig.update_layout(
    title="Combined Internal & External Defects – Real ODDO Spacing",
    xaxis=dict(
        tickmode='array',
        tickvals=tick_vals,
        ticktext=[str(val) for val in tick_vals],
        title='Distance from Launcher (ODDO) in meters',
        range=[min_oddo - 100, max_oddo + 100]
    ),
    yaxis=dict(
        title='ERF (ASME B31G)',
        tick0=0,
        dtick=0.05,
        range=[0, df['ERF (ASME B31G)'].max() + 0.05]
    ),
    height=700,
    width=1600,
    template='plotly_white',
    barmode='group'
)

combined_html = os.path.abspath('combined_real_oddo.html')
fig.write_html(combined_html)
webbrowser.open(f'file://{combined_html}')