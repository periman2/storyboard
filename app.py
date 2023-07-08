import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import time

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

## App Layout
app.layout = html.Div([
    html.Div([
        html.Div([
            # Upload Files element
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                className='upload-data',
                multiple=True
            ),
            # Uploaded Files or 'no files uploaded' text
            html.Div(id='file-upload-content'),
            # Upload progress bar
            dbc.Progress(id='upload-progress', value=0, max=100, className='upload-progress'),
            # Additional Inputs
            html.Div([
                # Genre Dropdown
                dcc.Dropdown(
                    id='genre-dropdown',
                    options=[
                        {'label': 'Horror', 'value': 'horror'},
                        {'label': 'Fantasy', 'value': 'fantasy'},
                        {'label': 'Romance', 'value': 'romance'},
                        # Add more genres as needed
                    ],
                    placeholder="Select a genre",
                    className='genre-dropdown'
                ),
            ], id='input-options', className='input-options'),
            # Generate Story Button
            dbc.Button("Generate Story", color="primary", id='generate-button', className="m-3", disabled=True),
            # Download Result
            dcc.Download(id="download-result"),
            # Download Result Button
            dbc.Button("Download Result", color="primary", id='download-button', className="m-3"),
            # Generation Progress bar
            dbc.Progress(id='generation-progress', value=0, max=100, className='generation-progress'),
            # Faking the progress at the moment (i think)
            dcc.Interval(id='generation-interval', interval=2000, n_intervals=0),
        ], className="d-flex flex-column align-items-center")
    ])
])

# Your callback functions remain unchanged...

if __name__ == '__main__':
    app.run_server(debug=True)


## Functions
# Update Output
#
@app.callback(
    Output('file-upload-content', 'children'),
    Output('upload-progress', 'value'),
    Output('generate-button', 'disabled'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(contents, filenames, last_modified):
    if not os.path.exists('temp'):
        os.makedirs('temp')

    if contents is not None:
        total_files = len(contents)
        uploaded_files = 0
        file_contents = []

        for content, filename, date in zip(contents, filenames, last_modified):
            if content is not None:
                # Save the file to a temporary location
                data = content.encode('utf-8')
                filepath = os.path.join('temp', filename)
                with open(filepath, 'wb') as f:
                    f.write(data)

                file_contents.append(html.P(filename))
                uploaded_files += 1

        upload_progress = int(uploaded_files / total_files * 100) if total_files > 0 else 0

        if file_contents:
            return file_contents, upload_progress, False  # Enable the Generate button

    return 'No files uploaded.', 0, True  # Disable the Generate button

# Generation Progress
total_progress = 0  # Store total progress outside the callback context

@app.callback(
    Output('generation-progress', 'value'),
    Output('generation-progress', 'children'),
    Input('generation-interval', 'n_intervals'),
    State('generate-button', 'n_clicks')
)
def update_generation_progress(n_intervals, n_clicks):
    global total_progress

    if n_clicks:
        if total_progress < 100:
            time.sleep(1)  # Simulate delay
            total_progress += 10

        return total_progress, f'{total_progress}%'
    
    return 0, ''

# Download Result
@app.callback(
    Output('download-result', 'data'),
    Input('download-button', 'n_clicks'),
    State('generation-progress', 'value')
)
def download_result(n_clicks, generation_progress):
    if n_clicks and generation_progress == 100:
        # Placeholder code to simulate the generated story
        story = "This is the generated story."

        # Return the result for download
        return dict(content=story, filename='result.txt')

    return None

if __name__ == '__main__':
    app.run_server(debug=True)
