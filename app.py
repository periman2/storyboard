import os
from config import TEMP_FOLDER_NAME
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import time
from story_engine import StoryEngine, StoryItem, StoryItemType
from helpers import is_image, is_any_document
import base64

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

## App Layout
app.layout = html.Div([
    html.Div([
        # Upload Files element
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
        # Uploaded Files or 'no files uploaded' text
        html.Div(id='file-upload-content'),
        # Upload progress bar
        dbc.Progress(id='upload-progress', 
                     value=0, 
                     max=100, 
                     style={
                         'width': '75%',
                         'textAlign': 'center'
                         }
                     ),
        
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
                style={'width': '200px'}
            ),
        ], id='input-options'),
        
        # Generate Story Button
        dbc.Button(
            "Generate Story", 
            color="primary", 
            id='generate-button', 
            className="m-3", 
            disabled=True
            ),
        
        #Download Result
        dcc.Download(id="download-result"),
        
        # Download Result Button
        dbc.Button(
            "Download Result", 
            color="primary", 
            id='download-button', 
            className="m-3"
            ),
        
        # Generation Progress bar
        dbc.Progress(id='generation-progress', 
                     value=0,
                     max=100, 
                     style={
                         'width': '75%',
                         'textAlign': 'center'
                         }
                     ),
        # Fakeing the progress at the moment (i think)
        dcc.Interval(id='generation-interval', 
                     interval=2000, 
                     n_intervals=0
                     ),
        ], 
        #Formatting things
        className="d-flex flex-column align-items-center", 
        style={
            'border': '1px solid', 
            'padding': '20px',
            'border-radius': '15px'
            }
        )
])

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
    if not os.path.exists(TEMP_FOLDER_NAME):
        os.makedirs(TEMP_FOLDER_NAME)

    if contents is not None:
        total_files = len(contents)
        uploaded_files = 0
        file_contents = []

        story_engine = StoryEngine("fantasy")

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

                #Filtering out only the accepted story type file formats. However this should be done before arriving at the backend normally. (TODO: Priority 3)
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
            print("Progress is : " + str(round(p * 100)) + "%")
            
        story = story_engine.once_upon_a_time(story_progress_callback)
        
        story_path = os.path.join(story_data_path, story_engine.story_title + '.txt')
        
        upload_progress = int(uploaded_files / total_files * 100) if total_files > 0 else 0

        with open(story_path, 'w') as f:
            f.write(story)
            
        if file_contents:
            return story  # Enable the Generate button

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

print("App is running!")
if __name__ == '__main__':
    app.run_server( "0.0.0.0", 80, debug = True)