import os
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
            dcc.Dropdown(
                id='genre-dropdown',
                options=[
                    {'label': 'Horror', 'value': 'horror'},
                    {'label': 'Fantasy', 'value': 'fantasy'},
                    {'label': 'Romance', 'value': 'romance'},
                    # Add more genres as needed
                ],
                placeholder="Select a genre",
                style={'width': '200px'}
            ),
        ], id='input-options'),

        dbc.Button("Generate", color="primary", id='generate-button', className="m-3"),

        dcc.Download(id="download-result"),

        dbc.Button("Download Result", color="primary", id='download-button', className="m-3"),
    ], className="d-flex flex-column align-items-center", style={'border': '1px solid', 'padding': '20px', 'border-radius': '15px'})
])

# Update Output
@app.callback(
    Output('file-upload-content', 'children'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(contents, filenames, last_modified):
    if not os.path.exists('temp'):
        os.makedirs('temp')

    if contents is not None:
        file_contents = []
        for content, filename, date in zip(contents, filenames, last_modified):
            if content is not None:
                # Save the file to a temporary location
                data = content.encode('utf-8')
                filepath = os.path.join('temp', filename)
                with open(filepath, 'wb') as f:
                    f.write(data)

                file_contents.append(html.P(filename))

        if file_contents:
            return file_contents

    return 'No files uploaded.'



# Backend Function call
@app.callback(
    Output('download-button', 'color'),
    Output('download-result', 'data'),
    Input('generate-button', 'n_clicks'),
    State('genre-dropdown', 'value')
)
def run_backend(n_clicks, dropdown_value):
    if n_clicks is None:
        return 'primary', None
    else:
        # Call your backend function here
        # Placeholder code to simulate backend processing
        import time
        time.sleep(5)
        
        # Simulate generating a result
        result = {'story': 'This is a test story.'}
        
        # Return the result for download
        return 'success', dict(content=result['story'], filename='result.txt')

if __name__ == '__main__':
    app.run_server(debug=True)
