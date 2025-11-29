import os
from google import genai
from google.genai import types

SYSTEM_PROMPT = """
You are a transcription engine. Output ONLY the subtitles.
Format every line exactly like this: MM:SS:MS - MM:SS:MS | The text goes here
Where MS is milliseconds (3 digits).
Example:
00:12:155 - 00:15:500 | Hello world.
please be concise and accurate with your transcriptions. Precison is what matters.
"""

def transcribe_audio(api_key, file_path):
    try: 
        with open(file_path, "rb") as f:
            audio_data = f.read()
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=[types.Content(parts=[
                types.Part.from_text(text=SYSTEM_PROMPT),
                types.Part.from_bytes(data=audio_data, mime_type="audio/mp3")
            ])]
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"