import pandas as pd
import plotly.graph_objects as go
import os
import webbrowser

# Load Excel data
file_path = r"C:\Users\pnish\Desktop\graph data.xlsx"
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

# Filter only Internal and External
df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()
df['Abs. Distance (m)'] = df['Abs. Distance (m)'].round(1)

# Group by to avoid overlaps
df = df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).agg({
    'ERF (ASME B31G)': 'max'
})
df.sort_values(by='Abs. Distance (m)', inplace=True)

# Split into two groups
internal_df = df[df['Surface Location'] == 'Internal']
external_df = df[df['Surface Location'] == 'External']

# Define axis limits
min_oddo = int(df['Abs. Distance (m)'].min()) // 500 * 500
max_oddo = int(df['Abs. Distance (m)'].max()) + 500
y_max = df['ERF (ASME B31G)'].max() + 0.05

# Build interactive dropdown plot
fig = go.Figure()

# Internal
fig.add_trace(go.Bar(
    x=internal_df['Abs. Distance (m)'],
    y=internal_df['ERF (ASME B31G)'],
    width=[60] * len(internal_df),
    name='Internal',
    marker_color='steelblue',
    opacity=0.9
))

# External
fig.add_trace(go.Bar(
    x=external_df['Abs. Distance (m)'],
    y=external_df['ERF (ASME B31G)'],
    width=[60] * len(external_df),
    name='External',
    marker_color='orangered',
    opacity=0.9
))

# Layout
fig.update_layout(
    title=dict(text="ERF (ASME B31G) vs Distance – Interactive View", font=dict(size=22), x=0.5),
    xaxis=dict(
        tickmode='linear',
        dtick=500,
        title='Distance from Launcher (ODDO) in meters',
        range=[min_oddo - 100, max_oddo + 100],
        gridcolor='lightgray',
        tickfont=dict(size=12),
        tickformat='~d'
    ),
    yaxis=dict(
        title='ERF (ASME B31G)',
        range=[0, y_max],
        dtick=0.05,
        gridcolor='lightgray',
        tickfont=dict(size=12)
    ),
    height=700,
    width=1600,
    template='plotly_white',
    barmode='group',
    bargap=0.2,
    legend=dict(
        title=dict(text='Defect Type', font=dict(size=14)),
        x=1.01,
        y=1,
        bgcolor='rgba(255,255,255,0.8)',
        bordercolor='lightgray',
        borderwidth=1,
        font=dict(size=12)
    ),
    updatemenus=[
        dict(
            type="dropdown",
            direction="down",
            x=1.15,
            y=1.15,
            showactive=True,
            buttons=[
                dict(label="Internal Only", method="update",
                     args=[{"visible": [True, False]},
                           {"title": "ERF (ASME B31G) vs Distance – Internal"}]),
                dict(label="External Only", method="update",
                     args=[{"visible": [False, True]},
                           {"title": "ERF (ASME B31G) vs Distance – External"}]),
                dict(label="Both", method="update",
                     args=[{"visible": [True, True]},
                           {"title": "ERF (ASME B31G) vs Distance – Combined"}]),
            ]
        )
    ]
)

# Save and open
html_path = os.path.abspath("erf_dropdown_plot.html")
fig.write_html(html_path)
webbrowser.open(f"file://{html_path}")