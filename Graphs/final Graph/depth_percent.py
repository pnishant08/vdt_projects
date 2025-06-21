import plotly.graph_objects as go
import os

def plot_depth(df, view="Both",return_fig=False):
    df.columns = df.columns.str.strip()
    df.rename(columns={col: "Depth % WT" for col in df.columns if "Depth" in col}, inplace=True)
    df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()
    df['Abs. Distance (m)'] = df['Abs. Distance (m)'].round(1)
    df = df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).agg({'Depth % WT': 'max'})
    df.sort_values(by='Abs. Distance (m)', inplace=True)

    min_oddo = int(df['Abs. Distance (m)'].min()) // 500 * 500
    max_oddo = int(df['Abs. Distance (m)'].max()) + 500
    y_max = df['Depth % WT'].max() + 10

    fig = go.Figure()

    if view in ["Internal", "Both"]:
        internal_df = df[df['Surface Location'] == 'Internal']
        fig.add_trace(go.Bar(
            x=internal_df['Abs. Distance (m)'],
            y=internal_df['Depth % WT'],
            name="Internal",
            marker_color='steelblue',
            width=[60]*len(internal_df),
            showlegend=True
        ))

    if view in ["External", "Both"]:
        external_df = df[df['Surface Location'] == 'External']
        fig.add_trace(go.Bar(
            x=external_df['Abs. Distance (m)'],
            y=external_df['Depth % WT'],
            name="External",
            marker_color='orangered',
            width=[60]*len(external_df),
            showlegend=True
        ))

    fig.update_layout(
        title="",
        xaxis=dict(title="Distance from Launcher (ODDO) in m", dtick=500, tickformat="~d"),
        yaxis=dict(title="Depth (% WT)", range=[0, y_max], dtick=5),
        barmode="group",
        height=700,
        width=1600,
        template="plotly_white"
    )

    html_path = os.path.abspath("depth_plot.html")
    fig.write_html(html_path)
    # return html_path
    return fig, html_path
