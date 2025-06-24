import plotly.graph_objects as go
import os

def dynamic_standard_plot(df, y_column, view="Both", graph_title="", y_axis_label="", plot_type="bar", return_fig=False):
    #  Debugclear
    # : initial columns
    print(f"[DEBUG] Initial Columns: {df.columns.tolist()}")

    df.columns = df.columns.str.strip()
    df.rename(columns={col: y_column for col in df.columns if y_column in col}, inplace=True)

    #  Debug: columns after rename
    print(f"[DEBUG] Columns After Rename: {df.columns.tolist()}")

    df = df[df['Surface Location'].isin(['Internal', 'External'])].copy()

    #  Debug: filtered dataframe shape
    print(f"[DEBUG] Filtered Dataframe Shape: {df.shape}")

    df['Abs. Distance (m)'] = df['Abs. Distance (m)'].round(1)

    if plot_type == "bar":
        df = df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).agg({y_column: 'max'})
        #  Debug: after grouping for bar
        print(f"[DEBUG] After Grouping (Bar): {df.head()}")
    else:
        df = df.sort_values(by='Abs. Distance (m)')
        #  Debug: after sorting for line
        print(f"[DEBUG] After Sorting (Line): {df.head()}")

    min_oddo = int(df['Abs. Distance (m)'].min()) // 500 * 500
    max_oddo = int(df['Abs. Distance (m)'].max()) + 500
    y_max = df[y_column].max() + 10

    #  Debug: axis ranges
    print(f"[DEBUG] ODDO Range: {min_oddo} to {max_oddo}")
    print(f"[DEBUG] Y-axis Max: {y_max}")

    fig = go.Figure()

    if view in ["Internal", "Both"]:
        internal_df = df[df['Surface Location'] == 'Internal']
        #  Debug: Internal points
        print(f"[DEBUG] Internal Data Points: {internal_df.shape}")

        if plot_type == "bar":
            fig.add_trace(go.Bar(
                x=internal_df['Abs. Distance (m)'],
                y=internal_df[y_column],
                name="Internal",
                marker_color='steelblue',
                width=[60] * len(internal_df)
            ))
        else:
            fig.add_trace(go.Scatter(
                x=internal_df['Abs. Distance (m)'],
                y=internal_df[y_column],
                mode='lines+markers',
                name="Internal",
                marker_color='steelblue'
            ))

    if view in ["External", "Both"]:
        external_df = df[df['Surface Location'] == 'External']
        #  Debug: External points
        print(f"[DEBUG] External Data Points: {external_df.shape}")

        if plot_type == "bar":
            fig.add_trace(go.Bar(
                x=external_df['Abs. Distance (m)'],
                y=external_df[y_column],
                name="External",
                marker_color='orangered',
                width=[60] * len(external_df)
            ))
        else:
            fig.add_trace(go.Scatter(
                x=external_df['Abs. Distance (m)'],
                y=external_df[y_column],
                mode='lines+markers',
                name="External",
                marker_color='orangered'
            ))

    fig.update_layout(
        title=f"{graph_title} – {view} View",
        xaxis=dict(title="Distance from Launcher (ODDO) in meters", dtick=500, tickformat="~d"),
        yaxis=dict(title=y_axis_label, range=[0, y_max], dtick=50),
        barmode="group" if plot_type == "bar" else None,
        height=700,
        width=1600,
        template="plotly_white"
    )

    html_path = os.path.abspath(f"{y_column.replace(' ', '_').lower()}_plot.html")
    fig.write_html(html_path)

    #  Debug: HTML Path
    print(f"[DEBUG] Graph saved at: {html_path}")

    if return_fig:
        return fig, html_path
    else:
        return html_path
