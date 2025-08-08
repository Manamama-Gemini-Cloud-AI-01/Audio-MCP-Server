### Audio Server (`audio_server.py`)

This script sets up a `FastMCP` server to provide tools for audio interaction and communication with the Google Gemini API. It uses the `sounddevice` and `soundfile` libraries for audio operations.

**Core Functionality:**

The server exposes the following tools:

*   **`list_audio_devices()`**: Lists all available audio input (microphones) and output (speakers) devices on the system.
*   **`record_audio(duration, sample_rate, channels, device_index)`**: Records audio from a specified microphone for a given duration. The recording is saved as a timestamped `.ogg` file in the `audio/` directory.
*   **`play_audio_file(file_path, device_index)`**: Plays a specified audio file through the selected speakers.
*   **`play_audio(text, voice)`**: A placeholder tool intended for text-to-speech (TTS) functionality. It currently does not convert text to audio but returns a message indicating that a TTS library is required.
*   **`gemini_conversation(duration, ...)`**: Initiates a conversation with the Gemini API.
    *   It records audio from the microphone.
    *   It **simulates** speech-to-text by using a hardcoded transcript.
    *   It sends the transcript to the Gemini API and retrieves a response.
    *   It returns the simulated user transcript and Gemini's text response.
    *   **Note:** This tool requires the `GOOGLE_API_KEY` environment variable to be set for authentication with the Gemini API. A full implementation would require actual speech-to-text and text-to-speech capabilities.
