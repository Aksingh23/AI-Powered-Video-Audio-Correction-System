import streamlit as st
from moviepy.editor import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import subprocess
import requests
from google.cloud import speech, texttospeech
import openai
import numpy as np
import soundfile as sf

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
            original_audio_duration = get_audio_duration(video_path)

            # Extract original video duration
            original_video_duration = get_audio_duration(video_path)

            # Replace audio in video
            st.write("Replacing and syncing audio in video...")   
            final_video_path = replace_audio_in_video(video_path, new_audio_path, original_video_duration)

            st.write("Here is your final video:")
            st.video(final_video_path)

# Save uploaded video to temporary directory
def save_uploaded_file(uploaded_file):
    video_path = f"temp_{uploaded_file.name}"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())
    return video_path

# Extract audio from video using moviepy and convert to mono
def extract_audio_from_video(video_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    output_audio = "audio_stereo.wav"
    audio.write_audiofile(output_audio, fps=16000, codec="pcm_s16le")  # Save as stereo WAV first
    
    # Now convert stereo to mono using soundfile
    data, samplerate = sf.read(output_audio)
    
    # If stereo (2 channels), convert to mono by averaging the channels
    if len(data.shape) > 1 and data.shape[1] == 2:
        data = np.mean(data, axis=1)
    
    output_audio_mono = "audio_mono.wav"
    sf.write(output_audio_mono, data, samplerate)
    
    return output_audio_mono

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

# Get video duration using moviepy
def get_video_duration(video_file):
    video = VideoFileClip(video_file)
    return video.duration

# Get video duration using moviepy
def get_audio_duration(video_file):
    video = VideoFileClip(video_file)
    return video.duration

# Replace audio in video using moviepy
def replace_audio_in_video(video_path, new_audio_path, original_video_duration):
    video_clip = VideoFileClip(video_path)
    new_audio_clip = AudioFileClip(new_audio_path)  # Use AudioFileClip for audio files

    # Sync audio duration to the original video length
    new_audio_clip = new_audio_clip.subclip(0, min(original_video_duration, new_audio_clip.duration))

    final_video = video_clip.set_audio(new_audio_clip)
    final_video_path = "final_video_with_synced_audio.mp4"
    final_video.write_videofile(final_video_path, codec="libx264", audio_codec="aac")
    return final_video_path

if __name__ == "__main__":
    main()
