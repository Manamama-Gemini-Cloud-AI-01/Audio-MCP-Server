import pytest
from unittest.mock import AsyncMock, patch
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from datetime import datetime
import numpy as np

# Import the functions from the module to be tested
# Assuming audio_server_exp.py is in the parent directory
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from audio_server_exp import list_audio_devices, record_audio, play_audio_file, gemini_conversation, DEFAULT_SAMPLE_RATE, DEFAULT_CHANNELS, DEFAULT_DURATION

@pytest.fixture
def mock_sounddevice():
    with patch('sounddevice.query_devices') as mock_query_devices, \
         patch('sounddevice.rec') as mock_rec, \
         patch('sounddevice.wait') as mock_wait, \
         patch('sounddevice.play') as mock_play:
        yield mock_query_devices, mock_rec, mock_wait, mock_play

@pytest.fixture
def mock_soundfile():
    with patch('soundfile.write') as mock_write, \
         patch('soundfile.read') as mock_read:
        yield mock_write, mock_read

@pytest.fixture
def mock_pathlib():
    with patch('pathlib.Path.mkdir') as mock_mkdir:
        yield mock_mkdir

@pytest.fixture
def mock_datetime():
    with patch('audio_server_exp.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2025, 8, 5, 10, 0, 0)
        yield mock_dt

@pytest.fixture
def mock_os_environ():
    with patch('os.environ.get') as mock_get:
        yield mock_get

@pytest.fixture
def mock_genai():
    with patch('audio_server_exp.genai') as mock_genai_module:
        mock_genai_module.configure = AsyncMock()
        mock_chat_session = AsyncMock()
        mock_chat_session.send_message = AsyncMock(return_value=AsyncMock(last="Simulated Gemini response."))
        mock_genai_module.ChatSession.return_value = mock_chat_session
        yield mock_genai_module

# --- Test Cases ---

@pytest.mark.asyncio
async def test_list_audio_devices_success(mock_sounddevice):
    mock_query_devices, _, _, _ = mock_sounddevice
    mock_query_devices.return_value = [
        {'name': 'Mic 1', 'max_input_channels': 2, 'max_output_channels': 0},
        {'name': 'Speaker 1', 'max_input_channels': 0, 'max_output_channels': 2},
        {'name': 'Mic 2', 'max_input_channels': 1, 'max_output_channels': 0},
    ]

    result = await list_audio_devices()

    assert "INPUTDEVICES (MICROPHONES):" in result
    assert "0: Mic 1 (Channels: 2)" in result
    assert "1: Mic 2 (Channels: 1)" in result
    assert "OUTPUTDEVICES (SPEAKERS):" in result
    assert "0: Speaker 1 (Channels: 2)" in result
    mock_query_devices.assert_called_once()

@pytest.mark.asyncio
async def test_record_audio_success(mock_sounddevice, mock_soundfile, mock_pathlib, mock_datetime):
    mock_query_devices, mock_rec, mock_wait, _ = mock_sounddevice
    mock_write, _ = mock_soundfile
    mock_mkdir = mock_pathlib

    mock_rec.return_value = np.zeros((int(DEFAULT_DURATION * DEFAULT_SAMPLE_RATE), DEFAULT_CHANNELS))
    mock_query_devices.return_value = [
        {'name': 'Mic 1', 'max_input_channels': 2, 'max_output_channels': 0}
    ]

    result = await record_audio(duration=DEFAULT_DURATION)

    mocked_datetime_str = mock_datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    expected_filename = f"audio_{mocked_datetime_str}_{DEFAULT_DURATION}s.ogg"
    expected_absolute_path = str(Path("audio") / expected_filename)

    assert "Audio recorded and saved to:" in result
    assert expected_absolute_path in result

    mock_rec.assert_called_once_with(
        int(DEFAULT_DURATION * DEFAULT_SAMPLE_RATE),
        samplerate=DEFAULT_SAMPLE_RATE,
        channels=DEFAULT_CHANNELS,
        device=None
    )
    mock_wait.assert_called_once()
    mock_mkdir.assert_called_once_with(exist_ok=True)
    mock_write.assert_called_once() # We'll check args more precisely in a real scenario

@pytest.mark.asyncio
async def test_record_audio_invalid_device_index(mock_sounddevice):
    mock_query_devices, _, _, _ = mock_sounddevice
    mock_query_devices.return_value = [
        {'name': 'Mic 1', 'max_input_channels': 2, 'max_output_channels': 0}
    ]

    result = await record_audio(device_index=999) # Invalid index

    assert "Error: Invalid device index 999. Use list_audio_devices tool to see available devices." in result

@pytest.mark.asyncio
async def test_record_audio_zero_duration(mock_sounddevice, mock_soundfile, mock_pathlib, mock_datetime):
    mock_rec, mock_wait = mock_sounddevice[1], mock_sounddevice[2]
    mock_write, _ = mock_soundfile
    mock_mkdir = mock_pathlib

    result = await record_audio(duration=0)

    assert "Audio recorded and saved to:" in result # Still returns success message for 0 duration
    mock_rec.assert_called_once_with(0, samplerate=DEFAULT_SAMPLE_RATE, channels=DEFAULT_CHANNELS, device=None)
    mock_wait.assert_called_once()
    mock_mkdir.assert_called_once_with(exist_ok=True)
    mock_write.assert_called_once() # sf.write is still called, but with empty data

@pytest.mark.asyncio
async def test_play_audio_file_success(mock_sounddevice, mock_soundfile):
    mock_query_devices, mock_rec, mock_wait, mock_play = mock_sounddevice
    mock_write, mock_read = mock_soundfile

    mock_read.return_value = (np.zeros((100, 1)), DEFAULT_SAMPLE_RATE) # Dummy audio data
    mock_query_devices.return_value = [
        {'name': 'Speaker 1', 'max_input_channels': 0, 'max_output_channels': 2}
    ]

    # Create a dummy file path for the test
    dummy_file_path = "/tmp/dummy_audio.ogg"
    with patch('os.path.exists', return_value=True):
        result = await play_audio_file(file_path=dummy_file_path)

    assert f"Successfully played audio file: {dummy_file_path}" in result
    mock_read.assert_called_once_with(dummy_file_path)
    mock_play.assert_called_once()
    mock_wait.assert_called_once()

@pytest.mark.asyncio
async def test_play_audio_file_not_found(mock_sounddevice, mock_soundfile):
    mock_query_devices, _, _, _ = mock_sounddevice
    mock_write, mock_read = mock_soundfile

    mock_query_devices.return_value = [
        {'name': 'Speaker 1', 'max_input_channels': 0, 'max_output_channels': 2}
    ]

    # Ensure os.path.exists returns False
    with patch('os.path.exists', return_value=False):
        result = await play_audio_file(file_path="/nonexistent/file.ogg")

    assert "Error: File not found at /nonexistent/file.ogg" in result
    mock_read.assert_not_called()

@pytest.mark.asyncio
async def test_play_audio_file_invalid_device_index(mock_sounddevice, mock_soundfile):
    mock_query_devices, _, _, _ = mock_sounddevice
    mock_write, mock_read = mock_soundfile

    mock_query_devices.return_value = [
        {'name': 'Speaker 1', 'max_input_channels': 0, 'max_output_channels': 2}
    ]

    # Create a dummy file path for the test
    dummy_file_path = "/tmp/dummy_audio.ogg"
    with patch('os.path.exists', return_value=True):
        result = await play_audio_file(file_path=dummy_file_path, device_index=999) # Invalid index

    assert "Error: Invalid device index 999. Use list_audio_devices tool to see available devices." in result
    mock_read.assert_not_called()

@pytest.mark.asyncio
async def test_gemini_conversation_success(mock_sounddevice, mock_os_environ, mock_genai, mock_pathlib, mock_datetime):
    mock_query_devices, mock_rec, mock_wait, _ = mock_sounddevice
    mock_mkdir = mock_pathlib
    mock_get = mock_os_environ
    mock_genai_module = mock_genai

    mock_get.return_value = "dummy_api_key"
    mock_rec.return_value = np.zeros((int(DEFAULT_DURATION * DEFAULT_SAMPLE_RATE), DEFAULT_CHANNELS))
    mock_query_devices.return_value = [
        {'name': 'Mic 1', 'max_input_channels': 2, 'max_output_channels': 0}
    ]

    result = await gemini_conversation(duration=DEFAULT_DURATION)

    mocked_datetime_str = mock_datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    expected_filename = f"audio_{mocked_datetime_str}_{DEFAULT_DURATION}s.ogg"
    expected_absolute_path = str(Path("audio") / expected_filename)

    assert "Real-time conversation with Gemini completed:" in result
    assert "User (simulated transcript): \"Hello Gemini, can you tell me about yourself?\"" in result
    assert "Simulated Gemini response: I am Gemini, a conversational AI." in result
    assert f"Audio saved to: {expected_absolute_path}" in result

    mock_get.assert_called_once_with("GOOGLE_API_KEY")
    mock_genai_module.configure.assert_called_once_with(api_key="dummy_api_key")
    mock_genai_module.ChatSession.assert_called_once_with(model="models/gemini-2.0-flash")
    mock_genai_module.ChatSession.return_value.send_message.assert_called_once_with("Hello Gemini, can you tell me about yourself?")
    mock_rec.assert_called_once()
    mock_wait.assert_called_once()
    mock_mkdir.assert_called_once_with(exist_ok=True)

@pytest.mark.asyncio
async def test_gemini_conversation_no_api_key(mock_os_environ):
    mock_get = mock_os_environ
    mock_get.return_value = None # Simulate no API key

    result = await gemini_conversation()

    assert "No API key provided. Please provide a valid Google AI API key" in result
    mock_get.assert_called_once_with("GOOGLE_API_KEY")

@pytest.mark.asyncio
async def test_gemini_conversation_record_audio_failure(mock_sounddevice, mock_os_environ, mock_genai):
    mock_query_devices, mock_rec, _, _ = mock_sounddevice
    mock_get = mock_os_environ
    mock_genai_module = mock_genai

    mock_get.return_value = "dummy_api_key"
    mock_rec.side_effect = Exception("Recording failed") # Simulate recording failure
    mock_query_devices.return_value = [
        {'name': 'Mic 1', 'max_input_channels': 2, 'max_output_channels': 0}
    ]

    result = await gemini_conversation()

    assert "Failed to record audio: Error recording audio: Recording failed" in result
    mock_rec.assert_called_once()

@pytest.mark.asyncio
async def test_gemini_conversation_genai_not_available():
    with patch('audio_server_exp.GENAI_AVAILABLE', False):
        result = await gemini_conversation()

    assert "Google Generative AI package is not installed." in result
