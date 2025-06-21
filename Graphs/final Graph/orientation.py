import plotly.graph_objects as go
import os

def clock_to_degrees(clock_str):
    try:
        h, m, s = map(int, str(clock_str).split(":"))
        decimal = h + m / 60 + s / 3600
        return (decimal % 12) * 30
    except:
        return None

def degrees_to_clock(deg):
    total_seconds = deg / 30 * 3600
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    return f"{h:02}:{m:02}:{s:02}"

def plot_orientation(df, view="Both",return_fig=False):
    df.columns = df.columns.str.strip()
    df['Angle (deg)'] = df['Orientation O\'clock'].apply(clock_to_degrees)
    df.dropna(subset=['Angle (deg)', 'Abs. Distance (m)', 'Surface Location'], inplace=True)

    min_dist = df['Abs. Distance (m)'].min()
    max_dist = df['Abs. Distance (m)'].max()

    fig = go.Figure()

    if view in ["Internal", "Both"]:
        internal_df = df[df['Surface Location'] == 'Internal']
        fig.add_trace(go.Scatter(
            x=internal_df['Abs. Distance (m)'],
            y=internal_df['Angle (deg)'],
            mode="markers",
            name="Internal",
            marker=dict(color="steelblue", size=6, symbol="triangle-up"),
            hovertemplate="Internal<br>Distance: %{x} m<br>Orientation: %{customdata}",
            customdata=internal_df['Angle (deg)'].apply(degrees_to_clock)
        ))

    if view in ["External", "Both"]:
        external_df = df[df['Surface Location'] == 'External']
        fig.add_trace(go.Scatter(
            x=external_df['Abs. Distance (m)'],
            y=external_df['Angle (deg)'],
            mode="markers",
            name="External",
            marker=dict(color="orangered", size=6, symbol="triangle-up"),
            hovertemplate="External<br>Distance: %{x} m<br>Orientation: %{customdata}",
            customdata=external_df['Angle (deg)'].apply(degrees_to_clock)
        ))

    fig.update_layout(
        title=f"Orientation vs Distance – {view} View",
        xaxis=dict(title="Distance from Launcher (ODDO) in meters", dtick=500, tickformat="~d"),
        yaxis=dict(title="Circumferential Orientation (o\'clock)", tickvals=[i*30 for i in range(13)], ticktext=[f"{i:02}:00:00" for i in range(13)]),
        height=700,
        width=1600,
        template="plotly_white"
    )

    html_path = os.path.abspath("orientation_plot.html")
    fig.write_html(html_path)
    # return html_path
    return fig, html_path