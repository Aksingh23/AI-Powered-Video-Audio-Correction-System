AI-Powered Video Audio Correction System

This project is designed to automatically process a video file by:

1. Extracting the audio.

2. Transcribing the audio using Google's Speech-to-Text API.

3. Correcting grammatical mistakes, filler words (e.g., "umms" and "hmms"), and errors using Azure OpenAI GPT-4o.

4. Generating a new, grammatically correct audio using Google's Text-to-Speech API (Journey voice model or a valid substitute).

5. Replacing the original audio in the video with the corrected audio.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Features:

1. Automatic Transcription: Converts the video's audio to text using Google's Speech-to-Text API.

2. Grammar Correction: Utilizes GPT-4o to clean up and correct the transcribed text.

3. AI Voice Generation: Uses Google's Text-to-Speech API to create an AI-generated voice with the corrected transcription.

4. Audio Replacement: Replaces the video's original audio with the generated AI voice, syncing it back to the video.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Tech Stack:

1. Streamlit: For building a user interface to upload videos and manage the workflow.

2. FFmpeg: For extracting and replacing audio in video files.

3. Google Cloud Speech-to-Text: For transcribing video audio.

4. Azure OpenAI GPT-4o: For correcting the transcription.

5. Google Cloud Text-to-Speech: For generating the corrected AI voice.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Prerequisites:

1. Python 3.8+ installed on your machine.

2. Set up accounts and API keys for:

     a. Google Cloud Speech-to-Text
     b.	Google Cloud Text-to-Speech
     c.	Azure OpenAI GPT-4o

3. Install required dependencies:

PowerShell Command

pip install streamlit requests google-cloud-speech google-cloud-texttospeech openai ffmpeg-python

4. FFmpeg installed on your system:

5. Set up environment variables for Google Cloud API authentication:

PowerShell Command

export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

How to Run the Project:

1. Clone the repository:

PowerShell Command

git clone https://github.com/yourusername/ai-video-correction.git
cd AI-Video-poc

2. Run the Streamlit application:

Command
streamlit run app.py

3. Upload a video file: Once the Streamlit UI is up and running, upload a video file with audio containing grammatical mistakes or filler words.

4. Process the video: Click the "Process Video" button, and the app will:

	a. Extract the audio.
	b. Transcribe the audio.
	c. Correct the transcription.
	d. Generate new audio.
	e. Replace the original audio with the corrected AI-generated audio.

5. Download or preview the final video: The corrected video with new audio will be displayed.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Example Workflow:

1. Upload a video file (e.g., sample_video.mp4).

2. The app will process the audio, correct the transcription, and sync the new audio back to the video.
3. The output video will be available for preview or download.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Notes:

1. Ensure your video file is in a supported format (e.g., .mp4).

2. The transcription accuracy depends on the quality of the audio and the capabilities of Google's Speech-to-Text API.

3. You may need to adjust the voice model used in Text-to-Speech based on availability in your region.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------

Additional Information:

1. The video and audio files will be stored in the project directory.

2. If the previous video or audio files are present in the project directory either you have to remove it or overwrite the file.

3. You can remove the previous audio and video files by just selecting the desired files and deleting it.

4. For overwriting the files you have to follow these:
	
	a. When you are running this command on the command prompt "streamlit run app.py".
	b. You will get an option for overwriting the file in the command prompt.
	c. Type y for 'Yes' and then proceed your whole process will go as designed.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------


Thank You very much..............................................................................
