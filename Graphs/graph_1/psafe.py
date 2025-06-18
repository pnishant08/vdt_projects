import pandas as pd
import plotly.graph_objects as go
import os
import webbrowser

# Load the Excel file
file_path = r"C:\Users\pnish\Desktop\graph data.xlsx"
df = pd.read_excel(file_path)

# Clean column names
df.columns = df.columns.str.strip()
df.rename(columns={'Psafe \n(ASME B31G), kg/cm2': 'Psafe (ASME B31G)'}, inplace=True)

# Filter for valid Surface Location
df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()

# Group by Abs. Distance and Surface Location to prevent duplicate x-values
df_grouped = df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).agg({
    'Psafe (ASME B31G)': 'max'  # use 'mean' if you want average instead
})

# Sort for consistent plotting
df_grouped.sort_values(by='Abs. Distance (m)', inplace=True)

# Split into internal and external
internal_df = df_grouped[df_grouped['Surface Location'] == 'Internal'].copy()
external_df = df_grouped[df_grouped['Surface Location'] == 'External'].copy()

# Define axis range
min_oddo = int(df_grouped['Abs. Distance (m)'].min()) // 500 * 500
max_oddo = int(df_grouped['Abs. Distance (m)'].max()) + 500

# Common Y-axis config
y_axis_config = dict(
    title='Psafe (ASME B31G) in kg/cm²',
    range=[0, 500],
    dtick=50,
    gridcolor='lightgray',
    tickfont=dict(size=12)
)

# Plotting function
def plot_psafe(df_plot, title, color, pattern_shape, filename):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_plot['Abs. Distance (m)'],
        y=df_plot['Psafe (ASME B31G)'],
        width=[60] * len(df_plot),
        opacity=0.9,
        marker=dict(
            color=color,
            line=dict(width=0.5, color='black'),
            pattern=dict(shape=pattern_shape, fgcolor="rgba(0,0,0,0.15)", fillmode="overlay")
        ),
        name=title,
        hovertemplate='Distance: %{x} m<br>Psafe: %{y} kg/cm²<extra></extra>'
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
        bargap=0.2
    )

    html_path = os.path.abspath(filename)
    fig.write_html(html_path)
    webbrowser.open(f'file://{html_path}')

# Internal Plot
plot_psafe(internal_df, "Internal Defects – Psafe (ASME B31G)", 'steelblue', "\\", 'internal_psafe_cleaned.html')

# External Plot
plot_psafe(external_df, "External Defects – Psafe (ASME B31G)", 'orangered', "x", 'external_psafe_cleaned.html')

# Combined Plot
fig_combined = go.Figure()

fig_combined.add_trace(go.Bar(
    x=internal_df['Abs. Distance (m)'],
    y=internal_df['Psafe (ASME B31G)'],
    width=[60] * len(internal_df),
    opacity=0.9,
    name='Internal',
    marker=dict(
        color='steelblue',
        line=dict(width=0.5, color='black'),
        pattern=dict(shape='\\', fgcolor="rgba(0,0,0,0.15)", fillmode="overlay")
    ),
    hovertemplate='Internal<br>Distance: %{x} m<br>Psafe: %{y} kg/cm²<extra></extra>'
))

fig_combined.add_trace(go.Bar(
    x=external_df['Abs. Distance (m)'],
    y=external_df['Psafe (ASME B31G)'],
    width=[60] * len(external_df),
    opacity=0.9,
    name='External',
    marker=dict(
        color='orangered',
        line=dict(width=0.5, color='black'),
        pattern=dict(shape='x', fgcolor="rgba(0,0,0,0.15)", fillmode="overlay")
    ),
    hovertemplate='External<br>Distance: %{x} m<br>Psafe: %{y} kg/cm²<extra></extra>'
))

fig_combined.update_layout(
    title=dict(text="Combined Internal & External Defects – Psafe (ASME B31G)", font=dict(size=24), x=0.5),
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
    barmode='group',
    bargap=0.2,
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

combined_path = os.path.abspath('combined_psafe_cleaned.html')
fig_combined.write_html(combined_path)
webbrowser.open(f'file://{combined_path}')