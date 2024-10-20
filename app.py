import streamlit as st
import subprocess
import requests
from google.cloud import speech, texttospeech
import openai

# Azure OpenAI connection details
azure_openai_key = "22ec84421ec24230a3638d1b51e3a7dc" 
azure_openai_endpoint = "https://internshala.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview" 

def main():
    st.title("AI-Powered Video Audio Replacement")

    # Upload video file
    uploaded_file = st.file_uploader("Upload your video", type=["mp4"])

    if uploaded_file:
        st.video(uploaded_file)
        
        # Process video when button is clicked
        if st.button("Process Video"):
            st.write("Extracting audio from video...")
            video_path = save_uploaded_file(uploaded_file)

            # Extract and transcribe the audio
            audio_path = extract_audio_from_video(video_path)
            transcription = transcribe_audio(audio_path)
            st.write("Original Transcription:")
            st.write(transcription)

            # Correct the transcription using GPT-4o
            st.write("Correcting transcription with GPT-4o...")
            corrected_transcription = clean_transcription_with_gpt4(transcription)
            st.write("Corrected Transcription:")
            st.write(corrected_transcription)

            # Generate AI voice from corrected transcription
            st.write("Generating AI voice...")
            new_audio_path = synthesize_speech(corrected_transcription)
            
            # Extract original audio duration
            original_audio_duration = get_audio_duration(audio_path)

            # Adjust AI-generated audio to match original audio duration
            adjusted_audio_path = adjust_audio_duration_to_match(original_audio_duration, new_audio_path)

            # Replace audio in video
            st.write("Replacing and syncing audio in video...")   
            final_video_path = replace_audio_in_video(video_path, new_audio_path)

            st.write("Here is your final video:")
            st.video(final_video_path)

# Save uploaded video to temporary directory
def save_uploaded_file(uploaded_file):
    video_path = f"temp_{uploaded_file.name}"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())
    return video_path

# Extract audio from video using FFmpeg and convert to mono
def extract_audio_from_video(video_file):
    output_audio = "audio_mono.wav"  # Output audio file name
    subprocess.run(["ffmpeg", "-i", video_file, "-ac", "1", output_audio])  # -ac 1 forces the audio to be mono
    return output_audio


# Transcribe audio using Google Speech-to-Text API
def transcribe_audio(audio_path):
    client = speech.SpeechClient()
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(language_code="en-US")
    response = client.recognize(config=config, audio=audio)
    transcription = ' '.join([result.alternatives[0].transcript for result in response.results])
    return transcription

# Use Azure OpenAI GPT-4o to clean transcription
def clean_transcription_with_gpt4(transcription):
    headers = {"Content-Type": "application/json", "api-key": azure_openai_key}
    data = {"messages": [{"role": "user", "content": f"Correct this transcription: {transcription}"}], "max_tokens": 1000}
    response = requests.post(azure_openai_endpoint, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    return None

# Generate AI voice using Google Text-to-Speech
def synthesize_speech(text):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="yue-HK-Standard-A")
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    output_audio = "new_audio.wav"
    with open(output_audio, "wb") as out:
        out.write(response.audio_content)
    return output_audio

# Get audio duration using FFmpeg
def get_audio_duration(audio_file):
    result = subprocess.run(
        ["ffmpeg", "-i", audio_file, "-hide_banner"], stderr=subprocess.PIPE, text=True
    )
    for line in result.stderr.splitlines():
        if "Duration" in line:
            duration_str = line.split(",")[0].split("Duration:")[1].strip()
            h, m, s = duration_str.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    return None


# Adjust AI-generated audio duration to match the original audio
def adjust_audio_duration_to_match(original_audio_duration, ai_audio_file):
    adjusted_audio_file = "adjusted_audio.wav"
    
    # Use FFmpeg to stretch/compress the AI-generated audio to match the original audio duration
    subprocess.run([
        "ffmpeg", "-i", ai_audio_file, 
        "-filter:a", f"aresample=async=1:min_hard_comp=0.100000:first_pts=0", 
        "-to", str(original_audio_duration), adjusted_audio_file
    ])
    return adjusted_audio_file

# Replace audio in video using FFmpeg
def replace_audio_in_video(video_path, new_audio_path):
    final_video_path = "final_video_with_synced_audio.mp4"
    
    # Ensure that the new audio is exactly in sync with the video using FFmpeg
    subprocess.run([
        "ffmpeg", "-i", video_path, "-i", new_audio_path, 
        "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", 
        "-map", "0:v:0", "-map", "1:a:0", 
        "-shortest", final_video_path
    ])
    
    return final_video_path

if __name__ == "__main__":
    main()
