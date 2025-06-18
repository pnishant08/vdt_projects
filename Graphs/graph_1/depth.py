import pandas as pd
import plotly.graph_objects as go
import os
import webbrowser

# Load and clean data
file_path = r"C:\Users\manvi\OneDrive\Documents\14inch RD to RT Oil Pipeline.xlsx"
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()
df.rename(columns={'Depth, % WT': 'Depth % WT'}, inplace=True)
df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()

# Round distance to nearest 1m to avoid overlaps
df['Abs. Distance (m)'] = df['Abs. Distance (m)'].round(1)

# Group and deduplicate by taking max depth at each location
df_grouped = df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).agg({
    'Depth % WT': 'max'
})
df_grouped.sort_values(by='Abs. Distance (m)', inplace=True)

# Split data
internal_df = df_grouped[df_grouped['Surface Location'] == 'Internal'].copy()
external_df = df_grouped[df_grouped['Surface Location'] == 'External'].copy()

# Axis ranges
min_oddo = int(df_grouped['Abs. Distance (m)'].min()) // 500 * 500
max_oddo = int(df_grouped['Abs. Distance (m)'].max()) + 500
y_max = df_grouped['Depth % WT'].max() + 10

# Common Y-axis config
y_axis_config = dict(
    title='Depth (% WT)',
    range=[0, y_max],
    dtick=5,
    gridcolor='lightgray',
    tickfont=dict(size=12)
)

# Plotting function
def plot_depth(df_plot, title, color, pattern_shape, filename):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_plot['Abs. Distance (m)'],
        y=df_plot['Depth % WT'],
        width=[60] * len(df_plot),
        opacity=0.9,
        marker_color=color,
        name=title,
    ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=22), x=0.5),
        xaxis=dict(
            tickmode='linear',
            dtick=500,
            title='Distance from Launcher (ODDO) in meters',
            range=[min_oddo - 100, max_oddo + 100],
            gridcolor='lightgray',
            tickfont=dict(size=12)
        ),
        yaxis=y_axis_config,
        height=700,
        width=1600,
        template='plotly_white',
        showlegend=False,
        bargap=0.05
    )

    html_path = os.path.abspath(filename)
    fig.write_html(html_path)
    webbrowser.open(f'file://{html_path}')

# Internal Plot
plot_depth(internal_df, "Internal Defects – Depth (% WT)", 'steelblue', "\\", 'internal_depth_clean.html')

# External Plot
plot_depth(external_df, "External Defects – Depth (% WT)", 'orangered', "x", 'external_depth_clean.html')

# Combined Plot
fig_combined = go.Figure()

fig_combined.add_trace(go.Bar(
    x=internal_df['Abs. Distance (m)'],
    y=internal_df['Depth % WT'],
    width=[60] * len(internal_df),
    opacity=0.9,
    name='Internal',
    marker_color='steelblue',
))

fig_combined.add_trace(go.Bar(
    x=external_df['Abs. Distance (m)'],
    y=external_df['Depth % WT'],
    width=[60] * len(external_df),
    opacity=0.9,
    name='External',
    marker_color='orangered',

))

fig_combined.update_layout(
    title=dict(text="Combined Internal & External Defects – Depth (% WT)", font=dict(size=24), x=0.5),
    xaxis=dict(
        tickmode='linear',
        dtick=500,
        title='Distance from Launcher (ODDO) in meters',
        range=[min_oddo - 100, max_oddo + 100],
        gridcolor='lightgray',
        tickfont=dict(size=12),
        tickformat='`d'
    ),
    yaxis=y_axis_config,
    height=700,
    width=1600,
    template='plotly_white',
    barmode='group',
    bargap=0.05,
    legend=dict(
        title=dict(text='Defect Type', font=dict(size=14)),
        x=1.02,
        y=1,
        xanchor='left',
        yanchor='top',
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='lightgray',
        borderwidth=1,
        font=dict(size=12)
    )
)

combined_path = os.path.abspath('combined_depth_clean.html')
fig_combined.write_html(combined_path)
webbrowser.open(f'file://{combined_path}')