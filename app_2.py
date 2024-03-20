import dash
from dash import dcc, html, Input, Output, State, ALL
import dash_bootstrap_components as dbc
import pandas as pd

# Load your local DataFrame
# Replace 'your_dataframe.csv' with the path to your actual DataFrame file
df = pd.read_excel('last_50_rows.xlsx')

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.Button("Add Group", id="add-group-btn", n_clicks=0),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Select Columns and Values")),
        dbc.ModalBody([
            html.Div([
                dbc.Checklist(
                    options=[{"label": col, "value": col} for col in df.columns],
                    id="column-select",
                    inline=True,
                    value=[],
                    switch=True,
                )
            ], id="column-select-container"),
            html.Div(id="value-select-container"),
        ]),
        dbc.ModalFooter(
            dbc.Button("Add", id="add-selection-btn", className="ms-auto", n_clicks=0)
        ),
    ], id="modal", is_open=False, size="lg"),
    html.Div(id="group-output")
])

@app.callback(
    Output("modal", "is_open"),
    [Input("add-group-btn", "n_clicks"), Input("add-selection-btn", "n_clicks")],
    [State("modal", "is_open")]
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("value-select-container", "children"),
    Input("column-select", "value")
)
def set_value_options(selected_columns):
    if selected_columns:
        return [
            html.Div([
                html.Label(col),
                dcc.Dropdown(
                    id={'type': 'dynamic-value-select', 'index': col},
                    options=[{"label": value, "value": value} for value in df[col].dropna().unique()],
                    multi=True
                )
            ]) for col in selected_columns
        ]
    return []

@app.callback(
    Output("group-output", "children"),
    [Input("add-selection-btn", "n_clicks")],
    [State({'type': 'dynamic-value-select', 'index': ALL}, 'value'),
     State({'type': 'dynamic-value-select', 'index': ALL}, 'id')]
)
def update_output(n_clicks, selected_values, ids):
    if n_clicks > 0:
        selected_columns = [id['index'] for id in ids]
        output_dict = {selected_columns[i]: selected_values[i] for i in range(len(selected_columns))}
        return str(output_dict)
    raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)
