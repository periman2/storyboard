# import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=True
        ),
        html.Div(id='file-upload-content'),

        html.Div([
            # This is a placeholder for your input options
            # Add your dropdowns and sliders here
        ], id='input-options'),

        dbc.Button("Generate", color="primary", id='generate-button', className="m-3"),

        dcc.Download(id="download-result"),

        dbc.Button("Download Result", color="primary", id='download-button', className="m-3"),
    ], className="d-flex flex-column align-items-center", style={'border': '1px solid', 'padding': '20px', 'border-radius': '15px'})
])

@app.callback(
    Output('file-upload-content', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        # Here you can store the files for further use
        # Make sure to return some information about the files to the frontend
        pass

@app.callback(
    Output('download-button', 'color'),
    Output('download-result', 'data'),
    Input('generate-button', 'n_clicks')
)
def run_backend(n):
    if n is None:
        return {'display': 'none'}, 'primary', None
    else:
        # Here you can start your backend operation and return its result
        # return {}, 'success', dict(content="Result", filename="result.txt") when the backend operation is done
        pass

if __name__ == '__main__':
    app.run_server(debug=True)
