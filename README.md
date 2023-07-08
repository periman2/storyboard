# Storyboard web application for the Google Vertex AI hackathlon!

This is a front-end prototype of a Dash web application designed for a Hackathon project. It has been built using Python, Dash and Bootstrap. The application is designed to accept file uploads, simulate progress, and generate and download results based on inputs from the user.

## Dependencies
- Python 3.x
- Dash
- Dash Bootstrap Components

## Features

- **File Uploads:** The user can upload one or more files via the 'Select Files' or drag-and-drop mechanism.
- **Genre Selection:** The user can select a genre from a dropdown menu. 
- **Story Generation:** The user can click a button to generate a story based on the uploaded files (and the selected genre, in theory, it doesn't pass that variable atm)
- **Download Results:** The user can download the generated story by clicking the 'Download Result' button.

## Code Explanation
The code consists of several key components:

1. **App Layout:** The layout of the app is defined using HTML and Dash components. This includes a file upload section, a progress bar for file uploads, a dropdown for genre selection, a button to initiate story generation, another progress bar for story generation, and a button to download the result.

2. **Upload Files:** The `update_output` function handles file uploads. It saves uploaded files to a temporary directory and calculates the upload progress. If files are uploaded successfully, the 'Generate Story' button is enabled.

3. **Story Generation:** The `update_generation_progress` function simulates story generation as a placeholder by incrementing a progress bar by 10% every 2 seconds when the 'Generate Story' button is clicked.

4. **Download Result:** The `download_result` function simulates downloading the generated story. When the 'Download Result' button is clicked, and the story generation progress is complete, it returns a placeholder string as the content of the generated story.

## How to Run

1. Ensure you have Python 3 and the required libraries installed. 
2. Clone or download this repository.
3. Navigate to the project directory and run the following command in your terminal:
    ```bash
    python main.py
    ```
4. Open a web browser and navigate to `http://127.0.0.1:8050/` to view the app.

## Note
This application is currently a front-end prototype and doesn't actually generate a story based on the input files and genre. The file upload, progress tracking, and result download features are functional, but the story generation is simulated. The backend logic for story generation will need to be added to the `update_generation_progress` and `download_result` functions.
