import os
from config import TEMP_FOLDER_NAME
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from story_engine import StoryEngine, StoryItem, StoryItemType
from helpers import is_image, is_any_document
import base64

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    children=[
        html.Header(
            children=[
                html.H1('Storyboard'),
            ]
        ),
        html.Div(
            children=[
                html.Div([
                    html.Div([
                        # Genre Dropdown
                        dcc.Dropdown(
                            id='genre-dropdown',
                            options=[
                                {'label': 'Horror', 'value': 'horror'},
                                {'label': 'Fantasy', 'value': 'fantasy'},
                                {'label': 'Romance', 'value': 'romance'},
                            ],
                            placeholder="Select a genre"
                        ),
                        dcc.Dropdown(
                            id='author-dropdown',
                            options=[
                                {'label': 'Agatha Christie', 'value': 'Agatha Christie'},
                                {'label': 'Jane Austen', 'value': 'Jane Austen'},
                                {'label': 'Stephen King', 'value': 'Stephen King'},
                            ],
                            placeholder="Select an Author"
                        ),
                    ],
                    className='input-options'),
                    # Upload Files element
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files')
                        ]),
                        multiple=True,
                        className='upload-data'
                    ),
                    # Uploaded Files or 'no files uploaded' text
                    html.Div(id='file-upload-content'),
                    # Progress bar
                    dbc.Progress(id='progress-bar', value=0, max=100),
                    # Additional Inputs
                    # Generate Story Button
                    dbc.Button("Download Story", color="primary", id='download-button', className="m-3", disabled=True),
                    # Download Result
                    dcc.Download(id="download-result"),
                ], 
                # Formatting things
                className="d-flex flex-column align-items-center"
                )
            ]
        ),
    ]
)

# Store total progress outside the callback context
total_progress = 0

@app.callback(
    Output('file-upload-content', 'children'),
    Output('progress-bar', 'value'),
    Output('download-button', 'disabled'),
    Input('upload-data', 'contents'),
#    Input('genre-dropdown','children'), #Input from genre dropdown
#    Input('author-dropdown', 'children'), #input from author dropdown
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)
def update_output(contents, filenames, last_modified): #add genre and author
    global total_progress
    if not os.path.exists(TEMP_FOLDER_NAME):
        os.makedirs(TEMP_FOLDER_NAME)

    if contents is not None:
        total_files = len(contents)
        uploaded_files = 0
        file_contents = []

        story_engine = StoryEngine("fantasy")# add genre and author

        story_data_path = os.path.join(TEMP_FOLDER_NAME, story_engine.story_id)
        print(story_data_path)
        os.mkdir(story_data_path)

        for content, filename, date in zip(contents, filenames, last_modified):
            if content is not None:
                # Save the file to a temporary location
                data = base64.b64decode(content.split(",")[1])
                filepath = os.path.join(story_data_path, filename)

                with open(filepath, 'wb') as f:
                    f.write(data)

                # Filtering out only the accepted story type file formats.
                storytype: StoryItemType
                if is_image(filename):
                    storytype = StoryItemType.IMAGE
                elif is_any_document(filename):
                    storytype = StoryItemType.DOCUMENT
                else:
                    continue

                story_engine.addItem(StoryItem(filepath, filename, storytype, date))
                file_contents.append(html.P(filename))
                uploaded_files += 1

                # Update upload progress (50% of total progress)
                total_progress = (uploaded_files / total_files) * 50
                print(f"Upload Progress: {total_progress}%")

        def story_progress_callback(p: float):
            global total_progress
            # Update story generation progress (50% of total progress)
            total_progress = 50 + (p * 50)
            print(f"Total Progress: {total_progress}%")
            return total_progress

        story = story_engine.once_upon_a_time(story_progress_callback)
        story_path = os.path.join(story_data_path, story_engine.story_title + '.txt')

        with open(story_path, 'w') as f:
            f.write(story)

        if file_contents:
            return file_contents, total_progress, False  # Enable the Generate button

    return 'No files uploaded.', 0, True  # Disable the Generate button

# Download Result
@app.callback(
    Output('download-result', 'data'),
    Input('download-button', 'n_clicks'),
    State('progress-bar', 'value')
)
def download_result(n_clicks, total_progress):
    if n_clicks and total_progress == 100:
        story = "This is the generated story."

        # Return the result for download
        return dict(content=story, filename='result.txt')

    return None

if __name__ == '__main__':
    app.run_server(debug=True)
