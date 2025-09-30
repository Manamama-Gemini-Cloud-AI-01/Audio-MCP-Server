# Audio MCP Server
[![smithery badge](https://smithery.ai/badge/@GongRzhe/Audio-MCP-Server)](https://smithery.ai/server/@GongRzhe/Audio-MCP-Server)

An MCP (Model Context Protocol) server that provides audio input/output capabilities for AI assistants. This server enables the AI to interact with your computer's audio system, including recording from microphones, playing audio through speakers, and integrating with the Google Gemini API.

## Features

- **List Audio Devices**: View all available microphones and speakers on your system.
- **Record Audio**: Capture audio from any microphone with customizable duration and quality.
- **Audio File Playback**: Play audio files through your speakers.
- **Gemini Conversation**: Initiate a voice-based conversation with the Google Gemini API.
- **Text-to-Speech**: (Placeholder for future implementation)

## Requirements

- Python 3.8 or higher
- Audio input/output devices on your system
- A Google Gemini API key (for the `gemini_conversation` tool)

## Installation

### Installing via Smithery

To install Audio Interface Server automatically via [Smithery](https://smithery.ai/server/@GongRzhe/Audio-MCP-Server):

```bash
npx -y @smithery/cli install @GongRzhe/Audio-MCP-Server
```

### Manual Installation
1. Clone this repository or download the files to your computer:

```bash
git clone https://github.com/GongRzhe/Audio-MCP-Server.git
cd Audio-MCP-Server
```

2. Create a virtual environment and install dependencies:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Or use the included setup script to automate installation:

```bash
python setup_mcp.py
```

## Configuration

To use this server, you need to set the `GOOGLE_API_KEY` environment variable with your Google Gemini API key. You can do this by creating a `.env` file in the project root:

```
GOOGLE_API_KEY="YOUR_API_KEY_HERE"
```

## Usage

After setting up the server, you can interact with it using an MCP-compatible client.

Try asking the AI:

- "What microphones and speakers are available on my system?"
- "Record 5 seconds of audio from my microphone."
- "Start a conversation with Gemini."

## Available Tools

### `list_audio_devices()`

Lists all available audio input and output devices on your system.

### `record_audio(duration, sample_rate, channels, device_index)`

Records audio from your microphone.

- `duration`: Recording duration in seconds (default: 5)
- `sample_rate`: Sample rate in Hz (default: 44100)
- `channels`: Number of audio channels (default: 1)
- `device_index`: Specific input device index to use (default: system default)

### `play_audio_file(file_path, device_index)`

Plays an audio file through your speakers.

- `file_path`: Path to the audio file
- `device_index`: Specific output device index to use (default: system default)

### `gemini_conversation(duration, ...)`

Initiates a conversation with the Gemini API. It records audio, sends it to Gemini (currently as a simulated transcript), and returns the text response.

- **Note:** This tool requires a `GOOGLE_API_KEY`.

### `play_audio(text, voice)`

Placeholder for text-to-speech functionality.

- `text`: The text to convert to speech
- `voice`: The voice to use (default: "default")


## Troubleshooting

### No devices found

If no audio devices are found, check:
- Your microphone and speakers are properly connected
- Your operating system recognizes the devices
- You have the necessary permissions to access audio devices

### Playback issues

If audio playback isn't working:
- Check your volume settings
- Ensure the correct output device is selected

### Server connectivity / Gemini Errors

If you have issues with the server or Gemini tools:
- Verify your `GOOGLE_API_KEY` is correct in the `.env` file.
- Ensure you have the `google-generativeai` package installed (`pip install google-generativeai`).
- Check your internet connection.

## License

MIT

## Acknowledgments

- Built using the [Model Context Protocol](https://modelcontextprotocol.io/)
- Uses [sounddevice](https://python-sounddevice.readthedocs.io/) and [soundfile](https://pysoundfile.readthedocs.io/) for audio processing
- Integrates with the [Google Gemini API](https://ai.google.dev/)

---

*Note: This server provides tools that can access your microphone and speakers. Always review and approve tool actions before they execute.*