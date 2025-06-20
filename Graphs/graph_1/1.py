import dash
from dash import dcc, html, Output, Input, State, ctx
import pandas as pd
import plotly.graph_objects as go
import base64
import io

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pipeline Defect Visualization UI"),

    # File Upload Component
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload Excel File'),
        multiple=False
    ),

    html.Br(),

    # Dropdown for graph type
    html.Label('Select Graph Type:'),
    dcc.Dropdown(
        id='graph-type',
        options=[
            {'label': 'ERF', 'value': 'ERF'},
            {'label': 'Psafe', 'value': 'Psafe'},
            {'label': 'Depth', 'value': 'Depth'},
        ],
        value='ERF'
    ),

    html.Br(),

    # Dropdown for defect type
    html.Label('Select Defect Type:'),
    dcc.Dropdown(
        id='defect-type',
        options=[
            {'label': 'Internal', 'value': 'Internal'},
            {'label': 'External', 'value': 'External'},
            {'label': 'Combined', 'value': 'Combined'}
        ],
        value='Combined'
    ),

    html.Br(),

    # Graph output
    dcc.Graph(id='graph-output')
])

# ============================
# Callback Function
# ============================

@app.callback(
    Output('graph-output', 'figure'),
    Input('upload-data', 'contents'),
    Input('graph-type', 'value'),
    Input('defect-type', 'value'),
    prevent_initial_call=True
)
def update_graph(contents, graph_type, defect_type):
    if contents is None:
        return go.Figure()

    # Read uploaded Excel file
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_excel(io.BytesIO(decoded))

    # Clean the data
    df.columns = df.columns.str.strip()
    df = df[df['Surface Location'].isin(['Internal', 'External'])]
    df['Abs. Distance (m)'] = df['Abs. Distance (m)'].round(1)

    # Choose Y-axis based on graph type
    y_col = ''
    if graph_type == 'ERF':
        y_col = 'ERF (ASME B31G)'
    elif graph_type == 'Psafe':
        y_col = 'Psafe (ASME B31G), kg/cm2'
    elif graph_type == 'Depth':
        y_col = 'Depth, % WT'

    # Filter data
    if defect_type == 'Internal':
        df = df[df['Surface Location'] == 'Internal']
    elif defect_type == 'External':
        df = df[df['Surface Location'] == 'External']

    # Build the figure
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['Abs. Distance (m)'],
        y=df[y_col],
        name=defect_type,
        marker_color='steelblue' if defect_type == 'Internal' else 'orangered'
    ))

    fig.update_layout(
        title=f'{graph_type} – {defect_type} Defects',
        xaxis_title='Distance from Launcher (ODDO) (m)',
        yaxis_title=y_col,
        template='plotly_white'
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
