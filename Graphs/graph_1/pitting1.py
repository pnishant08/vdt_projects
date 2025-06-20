def plot_pitting_count_with_dropdown(df, min_oddo, max_oddo, tick_vals, filename):
    import plotly.graph_objects as go
    import os
    import webbrowser

    # Filter for Metal Loss defects
    pitting_df = df[df['Feature Type'].str.strip() == 'Metal Loss']

    # Count Metal Loss per Abs. Distance (Internal and External)
    count_df = pitting_df.groupby(['Abs. Distance (m)', 'Surface Location'], as_index=False).size().rename(columns={'size': 'Pitting Count'})

    internal_df = count_df[count_df['Surface Location'] == 'Internal']
    external_df = count_df[count_df['Surface Location'] == 'External']

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=internal_df['Abs. Distance (m)'],
        y=internal_df['Pitting Count'],
        width=[60] * len(internal_df),
        marker_color='steelblue',
        name='Internal',
        hovertemplate='Distance: %{x} m<br>Pitting Count: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Bar(
        x=external_df['Abs. Distance (m)'],
        y=external_df['Pitting Count'],
        width=[60] * len(external_df),
        marker_color='orangered',
        name='External',
        hovertemplate='Distance: %{x} m<br>Pitting Count: %{y}<extra></extra>'
    ))

    fig.update_layout(
        title="Pitting Defects Count vs Distance – Interactive View",
        xaxis=dict(
            title="Distance from Launcher (ODDO) in meters",
            range=[min_oddo - 100, max_oddo + 100],
            tickmode="array",
            tickvals=tick_vals,
            ticktext=[str(val) for val in tick_vals]
        ),
        yaxis=dict(
            title='Pitting Defects Count',
            tick0=0,
            dtick=1,
            range=[0, max(internal_df['Pitting Count'].max(), external_df['Pitting Count'].max()) + 1]
        ),
        template='plotly_white',
        height=700,
        width=1600,
        barmode='group',
        updatemenus=[
            dict(
                type="dropdown",
                direction="down",
                x=1.15,
                y=1.1,
                showactive=True,
                buttons=[
                    dict(label="Internal Only", method="update", args=[{"visible": [True, False]}, {"title": "Pitting Defects – Internal"}]),
                    dict(label="External Only", method="update", args=[{"visible": [False, True]}, {"title": "Pitting Defects – External"}]),
                    dict(label="Both", method="update", args=[{"visible": [True, True]}, {"title": "Pitting Defects – Combined"}]),
                ],
            )
        ]
    )

    html_path = os.path.abspath(filename)
    fig.write_html(html_path)
    webbrowser.open(f'file://{html_path}')
