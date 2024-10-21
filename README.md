# AI-Powered-Video-Audio-Correction-System
This project lets users upload a video, transcribe and correct its audio using GPT-4, and replace the original audio with an AI-generated voice. Built with Streamlit, it integrates Google Cloud's Speech-to-Text and Text-to-Speech for transcription and voice synthesis, ensuring the new audio is synced with the video.

## Features
- Upload video files for processing.
- Extract and transcribe audio from videos.
- Correct transcriptions using GPT-4o model.
- Generate AI voice using Google Cloud Text-to-Speech.
- Sync the new audio with the original video.
- User-friendly interface powered by Streamlit.

## Requirements
- Python 3.7 or higher
- Google Cloud account with Speech-to-Text and Text-to-Speech enabled
- Azure OpenAI account for GPT-4o model access

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

On Windows:
  ```bash
        venv\Scripts\activate
  ```
On macOS/Linux:
  ```bash
    source venv/bin/activate
  ```
4. Install the required packages:

  ```bash
pip install -r requirements.txt
  ```
5. Set up Google Cloud credentials:

Create a service account in Google Cloud Console.
Download the JSON key file and set the environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"  # On macOS/Linux
set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\service-account-file.json"  # On Windows
```

6. Run the Streamlit application:

```bash
streamlit run app.py
```

## Usage
- Open your browser and navigate to http://localhost:8501.
- Upload a video file and follow the on-screen instructions to process the audio.


## Acknowledgements

- Google Cloud Platform for providing Speech-to-Text and Text-to-Speech services.
- Azure OpenAI for the GPT-4o model.
- Streamlit for building the user interface.
