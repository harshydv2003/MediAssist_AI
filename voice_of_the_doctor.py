# voice_of_the_doctor.py
import os
import platform
import subprocess
from elevenlabs.client import ElevenLabs
from elevenlabs import save

# The API key is automatically picked up from the environment variable ELEVENLABS_API_KEY
# Make sure you have set it:
# export ELEVENLABS_API_KEY="your_api_key_here"   # Linux/macOS
# set ELEVENLABS_API_KEY="your_api_key_here"      # Windows

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    # Initialize client
    client = ElevenLabs()  # API key is loaded automatically

    # Convert text to speech
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="21m00Tcm4TlvDq8ikWAM",  # Aria's voice ID
        model_id="eleven_multilingual_v2"
    )

    # Save audio file
    save(audio, output_filepath)

    # Auto-play audio
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])
        else:
            raise OSError("Unsupported OS")
    except Exception as e:
        print(f"Error while trying to play audio: {e}")