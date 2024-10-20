from google.cloud import texttospeech

def list_available_voices():
    client = texttospeech.TextToSpeechClient()

    # Perform the list voices request
    response = client.list_voices()

    # Display the available voices
    for voice in response.voices:
        print(f"Name: {voice.name}")
        for language_code in voice.language_codes:
            print(f"Supported Language: {language_code}")
        print(f"SSML Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
        print(f"Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")

list_available_voices()
