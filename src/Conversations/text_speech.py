
from random import randint
from gtts import gTTS
from io import BytesIO
import tempfile
import os
import base64


def text_to_speech_local(text, lang="en"):
    """Converts text to speech using gTTS and streams audio to the browser."""
    
    # Generate TTS audio using gTTS
    tts = gTTS(text=text, lang=lang)
    
    # Create a temporary file to store audio as MP3
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        audio_path = temp_audio.name

    # Save audio to the temporary file
    tts.save(audio_path)

    # Read the audio content as bytes into a BytesIO stream
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
    
    # Delete the temporary file after reading
    os.remove(audio_path)
    
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')

    return audio_base64


# def text_to_speech_local(text):
#     """Converts text to speech using pyttsx3 and streams audio to the browser."""
#     # Initialize pyttsx3 engine
#     engine = pyttsx3.init()
    
#     # Set voice properties if needed
#     engine.setProperty('rate', 150)  # Speed of speech (default ~200)
#     engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

#     # Create a temporary file to store audio
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
#         audio_path = temp_audio.name
    
#     # Save audio to the temporary file
#     engine.save_to_file(text, audio_path)
#     engine.runAndWait()
    
#     # Read audio content into BytesIO
#     with open(audio_path, "rb") as audio_file:
#         audio_bytes = audio_file.read()
    
#     return BytesIO(audio_bytes)


#     # Stream audio to the browser
#     #st.audio(BytesIO(audio_bytes), format="audio/mp3")

#     # Clean up temporary file
#     #os.remove(audio_path)

# from gtts import gTTS
# import os

# def text_to_speech_local(text, lang='en'):
#     tts = gTTS(text=text, lang=lang)
#     tts.save("output.mp3")
#     os.system("afplay output.mp3")  # macOS: Use 'start' for Windows, 'mpg321' for Linux


if __name__ == "__main__":
    audio_io = text_to_speech_local("hello how are you.")
    print(audio_io)