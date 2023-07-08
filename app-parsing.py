# import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from langchain.llms import VertexAI
from langchain import PromptTemplate, LLMChain

import requests
import base64

from dotenv import load_dotenv
load_dotenv()


# llm = VertexAI(model_name="text-bison@001")
# prompt = "Write a python function that identifies if the number is a prime number?"
# llm_result = llm(prompt)
# print(llm_result)

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def convert_to_base64(image_data):
    if image_data is not None:
        base64_data = base64.b64encode(image_data).decode('utf-8')
        return base64_data
    else:
        return None

image_label_detector = VertexAI(model_name="Salesforce/blip-image-captioning-base")

# Example usage
image_url = 'https://cdn.discordapp.com/attachments/1120724994444509265/1120731975527976990/mrscript_a_39_year_old_woman_with_short_golden_hair_and_black__72e4bf03-f404-4d2d-87f5-de5c54e47614.png'

# Download the image
# image_data = download_image(image_url)

# Convert the image to Base64
# base64_image = convert_to_base64(image_data)

# print(base64_image)

image_label_detector([{
        "image": {
            "source": {
                "imageUri": image_url
            }
        },
        "features": [{
            "type": "ZEROSHOT_LABEL_DETECTION"
        }],
        "imageContext": {
            "zeroshot_label_detection_params": {
                "labels": ["flower","a corgi","tree"]
            }
        }
    }])

# descriptions=blip(base64_image)
# print(descriptions)
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app.layout = html.Div([
#     html.Div([
#         dcc.Upload(
#             id='upload-data',
#             children=html.Div([
#                 'Drag and Drop or ',
#                 html.A('Select Files')
#             ]),
#             style={
#                 'width': '100%',
#                 'height': '60px',
#                 'lineHeight': '60px',
#                 'borderWidth': '1px',
#                 'borderStyle': 'dashed',
#                 'borderRadius': '5px',
#                 'textAlign': 'center',
#                 'margin': '10px'
#             },
#             multiple=True
#         ),
#         html.Div(id='file-upload-content'),

#         html.Div([
#             # This is a placeholder for your input options
#             # Add your dropdowns and sliders here
#         ], id='input-options'),

#         dbc.Button("Generate", color="primary", id='generate-button', className="m-3"),

#         dcc.Download(id="download-result"),

#         dbc.Button("Download Result", color="primary", id='download-button', className="m-3"),
#     ], className="d-flex flex-column align-items-center", style={'border': '1px solid', 'padding': '20px', 'border-radius': '15px'})
# ])

# @app.callback(
#     Output('file-upload-content', 'children'),
#     Input('upload-data', 'contents'),
#     State('upload-data', 'filename'),
#     State('upload-data', 'last_modified')
# )
# def update_output(list_of_contents, list_of_names, list_of_dates):
#     if list_of_contents is not None:
#         # Here you can store the files for further use
#         # Make sure to return some information about the files to the frontend
#         pass

# @app.callback(
#     Output('download-button', 'color'),
#     Output('download-result', 'data'),
#     Input('generate-button', 'n_clicks')
# )
# def run_backend(n):
#     if n is None:
#         return {'display': 'none'}, 'primary', None
#     else:
#         # Here you can start your backend operation and return its result
#         # return {}, 'success', dict(content="Result", filename="result.txt") when the backend operation is done
#         pass

# if __name__ == '__main__':
#     app.run_server(debug=True)
