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
        dcc.Loading(id="loader", children=[
            html.Div(
            id="main-container",
            style={"display": "block"},
            children=[
                html.Div(
                    id="main-conatiner",
                    style={"display": "block"},
                    children=[
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
                            html.A('Select Files'),
                            html.P("Supported types: pdf docx jpeg png txt")
                        ]),
                        multiple=True,
                        className='upload-data'
                    ),
                    # Generate Story Button
                    dbc.Button("Download Story", color="primary", id='download-button', className="m-3", style={"display": "none"}),
                    # Download Result
                    dcc.Textarea(
                        id='textarea',
                        value='',
                        style={"display": "none"}
                    ),
                    dcc.Download(id="download-result"),
                ], 
                # Formatting things
                className="d-flex flex-column align-items-center"
                )
            ]
        )
        ], type="circle")
    ]
)

## Functions
# Update Output



@app.callback(
    Output('download-button', 'style'),
    Output('textarea', 'style'),
    Output('textarea', 'value'),
    Output("main-container", "style"),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified'),
    State('genre-dropdown','value'), #Input from genre dropdown
    State('author-dropdown', 'value'), #input from author dropdown
)
def upload_files(contents, filenames, last_modified, genre: str, author: str): #add genre and author
    if not os.path.exists(TEMP_FOLDER_NAME):
        os.makedirs(TEMP_FOLDER_NAME)

    if contents is not None:
        total_files = len(contents)
        uploaded_files = 0
        file_contents = []
        
        if genre is None or genre == '':
            genre = 'fantasy'

        story_engine = StoryEngine(genre, author)# add genre and author

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

        def story_progress_callback(p: float):
            print(f"Total Progress: {round(p*100)}%")

        story = story_engine.once_upon_a_time(story_progress_callback)
        story_path = os.path.join(story_data_path, story_engine.story_title + '.txt')

        with open(story_path, 'w') as f:
            f.write(story)

        if file_contents:
            return  {"display": "block"}, {"display": "block"}, story, {"display": "block"}   # Enable the Generate button

    return {"display": "none"}, {"display": "none"}, '', {"display": "block"} # Disable the Generate button

# Download Result
# @app.callback(
#     Output('download-result', 'data'),
#     Input('download-button', 'n_clicks'),
# )
# def download_result(n_clicks, total_progress):
#     if n_clicks and total_progress == 100:
#         story = "This is the generated story."

#         # Return the result for download
#         return dict(content=story, filename='result.txt')

#     return None

print("App is running!")
if __name__ == '__main__':
    app.run_server( "0.0.0.0", 80, debug = True)