# graph_plotter.py
import plotly.express as px
import plotly.graph_objects as go
import os
import webbrowser
import pandas as pd
file_path = r"C:\Users\pnish\Desktop\graph data.xlsx"
df = pd.read_excel(file_path)

#---------------------- ERF vs Absolute Distance Graph (internal ,external and combined )---------------------

# def plot_real_oddo(df_plot, tick_vals, min_oddo, max_oddo, y_column, title, color, filename):
#     fig = go.Figure()
    

#     fig.add_trace(go.Bar(
#         x=df_plot['Abs. Distance (m)'],
#         y=df_plot[y_column],
#         width=[40] * len(df_plot),
#         marker_color=color,                     
#         name=title,
#         # hovertemplate='Distance: %{x} m<br>Value: %{y}<extra></extra>'
#     ))




#     fig.update_layout(
#         title=title,
#         xaxis=dict(
#             tickmode='array',
#             tickvals=tick_vals,
#             ticktext=[str(val) for val in tick_vals],
#             title='Distance from Launcher (ODDO) in meters',
#             range=[min_oddo - 100, max_oddo + 100]
#         ),
#         yaxis=dict(
#             title=y_column,
#             tick0=0,
#             dtick=.05,
#             range=[0, df_plot[y_column].max() + .05]
#         ),
#         height=700,
#         width=1600,
#         template='plotly_white'
#     )

#     html_path = os.path.abspath(filename)
#     fig.write_html(html_path)
#     webbrowser.open(f'file://{html_path}')

# def plot_combined(internal_df, external_df, tick_vals, min_oddo, max_oddo, y_column, title, filename):
#     fig = go.Figure()

#     fig.add_trace(go.Bar(
#         x=internal_df['Abs. Distance (m)'],
#         y=internal_df[y_column],
#         width=[100] * len(internal_df),
#         marker_color='steelblue',
#         name='Internal'
#     ))

#     fig.add_trace(go.Bar(
#         x=external_df['Abs. Distance (m)'],
#         y=external_df[y_column],
#         width=[60] * len(external_df),
#         marker_color='orangered',
#         name='External'
#     ))

#     fig.update_layout(
#         title=title,
#         xaxis=dict(
#             tickmode='array',
#             tickvals=tick_vals,
#             ticktext=[str(val) for val in tick_vals],
#             title='Distance from Launcher (ODDO) in meters',
#             range=[min_oddo - 100, max_oddo + 100]
#         ),
#         yaxis=dict(
#             title=y_column,
#             tick0=0,
#             dtick=.05,
#             range=[0, max(internal_df[y_column].max(), external_df[y_column].max()) + .05]
#         ),
#         height=700,
#         width=1600,
#         template='plotly_white',
#         barmode='group'
#     )

#     html_path = os.path.abspath(filename)
#     fig.write_html(html_path)
#     webbrowser.open(f'file://{html_path}')

def plot_erf_with_dropdown(internal_df, external_df, min_oddo, max_oddo, tick_vals, filename):
    fig = go.Figure()

    # Internal
    fig.add_trace(go.Bar(
        x=internal_df['Abs. Distance (m)'],
        y=internal_df['ERF (ASME B31G)'],
        width=[60] * len(internal_df),
        marker_color='steelblue',
        name='Internal',
        hovertemplate='Distance: %{x} m<br>ERF: %{y}<extra></extra>'
    ))

    # External
    fig.add_trace(go.Bar(
        x=external_df['Abs. Distance (m)'],
        y=external_df['ERF (ASME B31G)'],
        width=[60] * len(external_df),
        marker_color='orangered',
        name='External',
        hovertemplate='Distance: %{x} m<br>ERF: %{y}<extra></extra>'
    ))

    fig.update_layout(
        title="ERF vs Distance – Interactive View",
        xaxis=dict(
            title="Distance from Launcher (ODDO) in meters",
            range=[min_oddo - 100, max_oddo + 100],
            tickmode="array",
            tickvals=tick_vals,
            ticktext=[str(val) for val in tick_vals]
        ),
        yaxis=dict(
            title='ERF (ASME B31G)',
            tick0=0,
            dtick=0.05,
            range=[0, max(internal_df['ERF (ASME B31G)'].max(), external_df['ERF (ASME B31G)'].max()) + 0.05]
        ),
        template='plotly_white',
        height=700,
        width=1600,
        barmode='group',
        updatemenus=[  # Dropdown Menu
            dict(
                type="dropdown",
                direction="down",
                x=1.15,
                y=1.1,
                showactive=True,
                active=2,
                buttons=[
                    dict(label="Internal Only", method="update", args=[{"visible": [True, False]}, {"title": "ERF vs Distance – Internal"}]),
                    dict(label="External Only", method="update", args=[{"visible": [False, True]}, {"title": "ERF vs Distance – External"}]),
                    dict(label="Both", method="update", args=[{"visible": [True, True]}, {"title": "ERF vs Distance – Combined"}]),
                ],
            )
        ]
    )

    html_path = os.path.abspath(filename)
    fig.write_html(html_path)
    webbrowser.open(f'file://{html_path}')




#---------------------- PSAFE vs Absolute Distance Graph (internal ,external and combined )---------------------




# Common Y-axis configuration
y_axis_config = dict(
    title='Psafe (ASME B31G) in kg/cm²',
    range=[0, 500],
    dtick=50,
    gridcolor='lightgray',
    tickfont=dict(size=12)
)

# def plot_psafe_single(df_plot, title, color, pattern_shape, filename, min_oddo, max_oddo):
#     """Plot Psafe graph for Internal or External defects."""
#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         x=df_plot['Abs. Distance (m)'],
#         y=df_plot['Psafe (ASME B31G)'],
#         width=[60] * len(df_plot),
#         opacity=0.9,
#         marker=dict(
#             color=color,
#             line=dict(width=0.5, color='white'),
#             pattern=dict(shape=pattern_shape, fgcolor="rgba(0,0,0,0.15)", fillmode="overlay")
#         ),
#         name=title,
#         hovertemplate='Distance: %{x} m<br>Psafe: %{y} kg/cm²<extra></extra>'
#     ))

#     fig.update_layout(
#         title=dict(text=title, font=dict(size=22), x=0.5),
#         xaxis=dict(
#             tickmode='linear',
#             dtick=500,
#             title='Distance from Launcher (ODDO) in meters',
#             range=[min_oddo - 100, max_oddo + 100],
#             gridcolor='lightgray',
#             tickfont=dict(size=12)
#         ),
#         yaxis=y_axis_config,
#         height=700,
#         width=1600,
#         template='plotly_white',
#         showlegend=False,
#         bargap=0.2
#     )

#     html_path = os.path.abspath(filename)
#     fig.write_html(html_path)
#     webbrowser.open(f'file://{html_path}')

# def plot_psafe_combined(internal_df, external_df, min_oddo, max_oddo, filename):
#     """Plot combined Internal & External Psafe graph."""
#     fig_combined = go.Figure()

#     fig_combined.add_trace(go.Bar(
#         x=internal_df['Abs. Distance (m)'],
#         y=internal_df['Psafe (ASME B31G)'],
#         width=[60] * len(internal_df),
#         opacity=0.9,
#         name='Internal',
#         marker=dict(
#             color='steelblue',
#             line=dict(width=0.5, color='white'),
#             pattern=dict(shape='\\', fgcolor="rgba(0,0,0,0.15)", fillmode="overlay")
#         ),
#         hovertemplate='Internal<br>Distance: %{x} m<br>Psafe: %{y} kg/cm²<extra></extra>'
#     ))

#     fig_combined.add_trace(go.Bar(
#         x=external_df['Abs. Distance (m)'],
#         y=external_df['Psafe (ASME B31G)'],
#         width=[60] * len(external_df),
#         opacity=0.9,
#         name='External',
#         marker=dict(
#             color='orangered',
#             line=dict(width=0.5, color='white'),
#             pattern=dict(shape='x', fgcolor="rgba(0,0,0,0.15)", fillmode="overlay")
#         ),
#         hovertemplate='External<br>Distance: %{x} m<br>Psafe: %{y} kg/cm²<extra></extra>'
#     ))

#     fig_combined.update_layout(
#         title=dict(text="Combined Internal & External Defects – Psafe (ASME B31G)", font=dict(size=24), x=0.5),
#         xaxis=dict(
#             tickmode='linear',
#             dtick=500,
#             title='Distance from Launcher (ODDO) in meters',
#             range=[min_oddo - 100, max_oddo + 100],
#             gridcolor='lightgray',
#             tickfont=dict(size=12)
#         ),
#         yaxis=y_axis_config,
#         height=700,
#         width=1600,
#         template='plotly_white',
#         barmode='group',
#         bargap=0.2,
#         legend=dict(
#             title=dict(text='Defect Type', font=dict(size=14)),
#             x=1.02,
#             y=1,
#             xanchor='left',
#             yanchor='top',
#             bgcolor='rgba(255,255,255,0.8)',
#             bordercolor='lightgray',
#             borderwidth=1,
#             font=dict(size=12)
#         )
#     )

#     html_path = os.path.abspath(filename)
#     fig_combined.write_html(html_path)
#     webbrowser.open(f'file://{html_path}')

def plot_psafe_with_dropdown(internal_df, external_df, min_oddo, max_oddo, tick_vals, filename):
    """Plot Psafe graph with dropdown for Internal, External, and Combined views."""
    fig = go.Figure()

    # Internal
    fig.add_trace(go.Bar(
        x=internal_df['Abs. Distance (m)'],
        y=internal_df['Psafe (ASME B31G)'],
        width=[60] * len(internal_df),
        opacity=0.9,
        name='Internal',
        marker=dict(
            color='steelblue',
            line=dict(width=0.5, color='white'),
            pattern=dict(shape='\\', fgcolor="rgba(0,0,0,0.15)", fillmode="overlay")
        ),
        hovertemplate='Internal<br>Distance: %{x} m<br>Psafe: %{y} kg/cm²<extra></extra>'
    ))

    # External
    fig.add_trace(go.Bar(
        x=external_df['Abs. Distance (m)'],
        y=external_df['Psafe (ASME B31G)'],
        width=[60] * len(external_df),
        opacity=0.9,
        name='External',
        marker=dict(
            color='orangered',
            line=dict(width=0.5, color='white'),
            pattern=dict(shape='x', fgcolor="rgba(0,0,0,0.15)", fillmode="overlay")
        ),
        hovertemplate='External<br>Distance: %{x} m<br>Psafe: %{y} kg/cm²<extra></extra>'
    ))

    fig.update_layout(
        title="Psafe vs Distance – Combined View",
        xaxis=dict(
            title="Distance from Launcher (ODDO) in meters",
            range=[min_oddo - 100, max_oddo + 100],
            tickmode="array",
            tickvals=tick_vals,
            ticktext=[str(val) for val in tick_vals]
        ),
        yaxis=y_axis_config,
        template='plotly_white',
        height=700,
        width=1600,
        barmode='group',
        bargap=0.2,
        updatemenus=[  # Dropdown Menu
            dict(
                type="dropdown",
                direction="down",
                x=1.15,
                y=1.1,
                showactive=True,
                active=2,
                buttons=[
                    dict(label="Internal Only", method="update", args=[{"visible": [True, False]}, {"title": "Psafe vs Distance – Internal"}]),
                    dict(label="External Only", method="update", args=[{"visible": [False, True]}, {"title": "Psafe vs Distance – External"}]),
                    dict(label="Both", method="update", args=[{"visible": [True, True]}, {"title": "Psafe vs Distance – Combined"}]),
                ],
            )
        ]
    )

    html_path = os.path.abspath(filename)
    fig.write_html(html_path)
    webbrowser.open(f'file://{html_path}')






# ======================= DEPTH vs Absolute Distance Graph (Internal, External, Combined) =======================

    # """Plot Depth graph for Internal or External defects."""
# def plot_depth_single(df_plot, title, color, filename, min_oddo, max_oddo):
#     fig = go.Figure()
#     fig.add_trace(go.Bar(
#         x=df_plot['Abs. Distance (m)'],
#         y=df_plot['Depth % WT'],
#         width=[60] * len(df_plot),
#         opacity=0.9,
#         marker_color=color,
#         name=title,
#         # hovertemplate='Distance: %{x} m<br>Depth: %{y}% WT<extra></extra>'
#     ))

#     fig.update_layout(
#         title=dict(text=title, font=dict(size=22), x=0.5),
#         xaxis=dict(
#             tickmode='linear',
#             dtick=500,
#             tickformat = 'd',
#             title='Distance from Launcher (ODDO) in meters',
#             range=[min_oddo - 100, max_oddo + 100],
#             gridcolor='lightgray',
#             tickfont=dict(size=12)
#         ),
#         yaxis=dict(
#             title='Depth (% WT)',
#             range=[0, df_plot['Depth % WT'].max() + 10],
#             dtick=5,
#             gridcolor='lightgray',
#             tickfont=dict(size=12)
#         ),
#         height=700,
#         width=1600,
#         template='plotly_white',
#         showlegend=False,
#         bargap=0.05
#     )

#     html_path = os.path.abspath(filename)
#     fig.write_html(html_path)
#     webbrowser.open(f'file://{html_path}')

# def plot_depth_combined(internal_df, external_df, min_oddo, max_oddo, filename):
#     """Plot combined Depth graph for Internal & External defects."""
#     fig = go.Figure()

#     fig.add_trace(go.Bar(
#         x=internal_df['Abs. Distance (m)'],
#         y=internal_df['Depth % WT'],
#         width=[60] * len(internal_df),
#         opacity=0.9,
#         name='Internal',
#         marker_color='steelblue',
#         hovertemplate='Internal<br>Distance: %{x} m<br>Depth: %{y}% WT<extra></extra>'
#     ))

#     fig.add_trace(go.Bar(
#         x=external_df['Abs. Distance (m)'],
#         y=external_df['Depth % WT'],
#         width=[60] * len(external_df),
#         opacity=0.9,
#         name='External',
#         marker_color='orangered',
#         hovertemplate='External<br>Distance: %{x} m<br>Depth: %{y}% WT<extra></extra>'
#     ))

#     fig.update_layout(
#         title=dict(text="Combined Internal & External Defects – Depth (% WT)", font=dict(size=24), x=0.5),
#         xaxis=dict(
#             tickmode='linear',
#             dtick=500,
#             tickformat = 'd',
#             title='Distance from Launcher (ODDO) in meters',
#             range=[min_oddo - 100, max_oddo + 100],
#             gridcolor='lightgray',
#             tickfont=dict(size=12)
#         ),
#         yaxis=dict(
#             title='Depth (% WT)',
#             range=[0, max(internal_df['Depth % WT'].max(), external_df['Depth % WT'].max()) + 10],
#             dtick=5,
#             gridcolor='lightgray',
#             tickfont=dict(size=12)
#         ),
#         height=700,
#         width=1600,
#         template='plotly_white',
#         barmode='group',
#         bargap=0.2,
#         legend=dict(
#             title=dict(text='Defect Type', font=dict(size=14)),
#             x=1.02,
#             y=1,
#             xanchor='left',
#             yanchor='top',
#             bgcolor='rgba(255,255,255,0.8)',
#             bordercolor='lightgray',
#             borderwidth=1,
#             font=dict(size=12)
#         )
#     )

#     html_path = os.path.abspath(filename)
#     fig.write_html(html_path)
#     webbrowser.open(f'file://{html_path}')
 
def plot_depth_with_dropdown(internal_df, external_df, min_oddo, max_oddo, tick_vals, filename):
    """Plot Depth graph with dropdown for Internal, External, and Combined views."""
    fig = go.Figure()

    # Internal
    fig.add_trace(go.Bar(
        x=internal_df['Abs. Distance (m)'],
        y=internal_df['Depth % WT'],
        width=[60] * len(internal_df),
        opacity=0.9,
        name='Internal',
        marker_color='steelblue',
        hovertemplate='Internal<br>Distance: %{x} m<br>Depth: %{y}% WT<extra></extra>'
    ))

    # External
    fig.add_trace(go.Bar(
        x=external_df['Abs. Distance (m)'],
        y=external_df['Depth % WT'],
        width=[60] * len(external_df),
        opacity=0.9,
        name='External',
        marker_color='orangered',
        hovertemplate='External<br>Distance: %{x} m<br>Depth: %{y}% WT<extra></extra>'
    ))

    fig.update_layout(
        title="Depth vs Distance – Combined View",
        xaxis=dict(
            title="Distance from Launcher (ODDO) in meters",
            range=[min_oddo - 100, max_oddo + 100],
            tickmode="array",
            tickvals=tick_vals,
            ticktext=[str(val) for val in tick_vals],
            dtick=500,
            tickformat='d',
            gridcolor='lightgray'
        ),
        yaxis=dict(
            title='Depth (% WT)',
            range=[0, max(internal_df['Depth % WT'].max(), external_df['Depth % WT'].max()) + 10],
            dtick=5,
            gridcolor='lightgray'
        ),
        template='plotly_white',
        height=700,
        width=1600,
        barmode='group',
        bargap=0.2,
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                x=1.15,
                y=1.1,
                showactive=True,
                active=2,
                buttons=[
                    dict(label="Internal Only", method="update", args=[{"visible": [True, False]}, {"title": "Depth vs Distance – Internal"}]),
                    dict(label="External Only", method="update", args=[{"visible": [False, True]}, {"title": "Depth vs Distance – External"}]),
                    dict(label="Both", method="update", args=[{"visible": [True, True]}, {"title": "Depth vs Distance – Combined"}]),
                ],
            )
        ]
    )

    html_path = os.path.abspath(filename)
    fig.write_html(html_path)
    webbrowser.open(f'file://{html_path}')


# ======================= Orientation vs Absolute Distance Graph (Internal, External, Combined) =======================

def plot_orientation_with_dropdown(internal_df, external_df, min_dist, max_dist, filename):
    fig = go.Figure()

    # Internal Data
    fig.add_trace(go.Scatter(
        x=internal_df["Abs. Distance (m)"],
        y=internal_df["Angle (deg)"],
        mode="markers",
        name="Internal",
        marker=dict(color="steelblue", size=6, symbol="triangle-up"),
        hovertemplate="Internal<br>Distance: %{x} m<br>Orientation: %{y}°<extra></extra>"
    ))

    # External Data
    fig.add_trace(go.Scatter(
        x=external_df["Abs. Distance (m)"],
        y=external_df["Angle (deg)"],
        mode="markers",
        name="External",
        marker=dict(color="orangered", size=6, symbol="triangle-up"),
        hovertemplate="External<br>Distance: %{x} m<br>Orientation: %{y}°<extra></extra>"
    ))

    # Dropdown Menu
    fig.update_layout(
        title="Orientation vs Distance – Interactive View",
        xaxis=dict(
            title="Distance from Launcher (ODDO) in meters",
            range=[min_dist, max_dist],
            tickformat="~d",
            dtick=500,
            tickmode="linear"
        ),
        yaxis=dict(title="Circumferential Orientation (°)", range=[0, 360], dtick=30),
        template="plotly_white",
        height=700,
        width=1400,
        updatemenus=[  # Dropdown Configuration
            dict(
                type="dropdown",
                direction="down",
                x=1.15,
                y=1.1,
                showactive=True,
                buttons=[
                    dict(label="Internal Only", method="update", args=[{"visible": [True, False]}, {"title": "Orientation vs Distance – Internal"}]),
                    dict(label="External Only", method="update", args=[{"visible": [False, True]}, {"title": "Orientation vs Distance – External"}]),
                    dict(label="Both", method="update", args=[{"visible": [True, True]}, {"title": "Orientation vs Distance – Combined"}]),
                ],
            )
        ]
    )

    html_path = os.path.abspath(filename)
    fig.write_html(html_path)
    webbrowser.open(f"file://{html_path}")






import plotly.graph_objects as go
import pandas as pd
import os
import webbrowser

def plot_erf_3d_bars(df_internal, df_external, filename):
    fig = go.Figure()

    # Plot bars for Internal defects
    for idx, row in df_internal.iterrows():
        fig.add_trace(go.Scatter3d(
            x=[row['Abs. Distance (m)'], row['Abs. Distance (m)']],
            y=[0, 0],  # Group 'Internal' at y=0
            z=[0, row['ERF (ASME B31G)']],
            mode='lines',
            line=dict(color='steelblue', width=10),
            name='Internal'
        ))

    # Plot bars for External defects
    for idx, row in df_external.iterrows():
        fig.add_trace(go.Scatter3d(
            x=[row['Abs. Distance (m)'], row['Abs. Distance (m)']],
            y=[1, 1],  # Group 'External' at y=1
            z=[0, row['ERF (ASME B31G)']],
            mode='lines',
            line=dict(color='orangered', width=10),
            name='External'
        ))

    fig.update_layout(
        title='3D ERF Bar Graph',
        scene=dict(
            xaxis_title='Distance from Launcher (ODDO) (m)',
            yaxis=dict(
                title='Surface Location',
                tickvals=[0, 1],
                ticktext=['Internal', 'External']
            ),
            zaxis_title='ERF (ASME B31G)'
        ),
        width=1400,
        height=800,
        template='plotly_white',
        showlegend=False
    )

    html_path = os.path.abspath(filename)
    fig.write_html(html_path)
    webbrowser.open(f'file://{html_path}')

