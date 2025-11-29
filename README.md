# LiteAudioScribe (AI-Powered Music Player)

**LiteAudioScribe** is a lightweight desktop application that combines a local MP3 player with the power of Generative AI. It allows you to play your local music collection and generate accurate, timestamped subtitles on demand using Google's Gemini Flash model.

## Features

*   **Local Playback:** Clean and simple interface to play `.mp3` files from your computer.
*   **AI Transcription:** Uses Google Gemini API to transcribe audio into text.
*   **Smart Sync:** Subtitles are synchronized with the audio timeline (Karaoke style).
*   **Real-time Controls:** Play, pause, stop, and seek through the track using a slider.


## Tech Stack

*   **Language:** Python 3.10+
*   **GUI:** Tkinter (CustomTkinter/Ttk)
*   **Audio Engine:** Pygame Mixer
*   **AI Model:** Google Gemini Flash via `google-genai` SDK
*   **Threading:** For non-blocking UI during AI processing

## How to Run

1.  **Clone the repository**
    ```bash
    git clone https://github.com/rpcrypt-0/LiteAudioScribe.git
    cd LiteAudioScribe
    ```

2.  **Install dependencies**
    ```bash
    pip install pygame google-genai python-dotenv
    ```

3.  **Setup API Key**
    *   Create a file named `.env` in the main folder.
    *   Add your key: `GEMINI_API_KEY=your_actual_api_key_here`
    *   *Alternatively, the app will ask you to enter it when you run it.*

4.  **Run the App**
    ```bash
    python main.py
    ```
