# Unit Test Plan for `audio_server_exp.py`

## Objective
To ensure the stability and correctness of the `audio_server_exp.py` functionalities, particularly after recent modifications that led to server instability. This plan focuses on isolating and testing individual components.

## 1. Test Framework
**Recommendation:** `pytest`
*   **Reasoning:** `pytest` is a popular, easy-to-use, and powerful testing framework for Python. It supports simple test functions, fixtures for setup/teardown, and excellent mocking capabilities.

## 2. Test File Location
**Recommendation:** Create a `tests` directory at the root of the `Audio-MCP-Server` project, and place the test file inside:
*   `/home/zezen/Downloads/GitHub/Audio-MCP-Server/tests/test_audio_server.py`

## 3. Mocking Strategy
Since `audio_server_exp.py` interacts with system audio devices and external APIs (Google Generative AI), it's crucial to use mocking to isolate unit tests from these external dependencies.
*   **`sounddevice` and `soundfile`:** These modules will be mocked to prevent actual audio recording/playback during tests. We will simulate their behavior (e.g., `sd.rec` returning dummy audio data, `sf.write` confirming file write without touching the disk).
*   **`pathlib.Path.mkdir`:** Mock this to ensure directory creation is simulated without actual filesystem changes during tests.
*   **`datetime.now()`:** Mock this to control timestamps for predictable filename generation.
*   **`os.environ.get`:** Mock this to control the `GOOGLE_API_KEY` environment variable for `gemini_conversation` tests.
*   **`google.generativeai` (if `GENAI_AVAILABLE` is True):** Mock `genai.configure`, `model.ChatSession`, and `chat_session.send_message` to simulate API responses without making actual network calls.

## 4. Test Cases

### 4.1. `list_audio_devices`
*   **Purpose:** Verify that the function correctly identifies and lists audio input and output devices.
*   **Test Cases:**
    *   `test_list_audio_devices_success`:
        *   Mock `sd.query_devices` to return a predefined list of dummy devices.
        *   Assert that the returned string contains expected device names and channel counts for both input and output.

### 4.2. `record_audio`
*   **Purpose:** Verify that audio is recorded and saved correctly to a file with the specified format and naming convention, and that error handling is robust.
*   **Test Cases:**
    *   `test_record_audio_success`:
        *   Mock `sd.rec` to return dummy audio data.
        *   Mock `Path("audio").mkdir` to ensure directory creation is simulated.
        *   Mock `sf.write` to verify it's called with the correct file path, recording data, and sample rate.
        *   Mock `datetime.now()` to control the timestamp in the filename.
        *   Assert that the function returns a success message containing the expected absolute file path.
    *   `test_record_audio_invalid_device_index`:
        *   Mock `get_audio_devices` to return a list of devices.
        *   Call `record_audio` with an out-of-bounds `device_index`.
        *   Assert that the function returns an error message indicating an invalid device index.
    *   `test_record_audio_zero_duration`:
        *   Call `record_audio` with `duration=0`.
        *   Assert that `sf.write` is not called (or handles zero-length audio gracefully).
        *   Assert the function returns an appropriate message.

### 4.3. `play_audio_file`
*   **Purpose:** Verify that audio files can be played back correctly and that error handling for non-existent files or invalid devices is robust.
*   **Test Cases:**
    *   `test_play_audio_file_success`:
        *   Create a dummy audio file (or mock `sf.read` to return dummy data).
        *   Mock `sd.play` and `sd.wait` to ensure playback is simulated.
        *   Assert that the function returns a success message.
    *   `test_play_audio_file_not_found`:
        *   Call `play_audio_file` with a non-existent file path.
        *   Assert that the function returns an error message indicating the file was not found.
    *   `test_play_audio_file_invalid_device_index`:
        *   Mock `get_audio_devices` to return a list of devices.
        *   Call `play_audio_file` with a valid file path but an out-of-bounds `device_index`.
        *   Assert that the function returns an error message indicating an invalid device index.

### 4.4. `gemini_conversation`
*   **Purpose:** Verify the function's interaction with `record_audio` and its handling of API keys and Gemini responses.
*   **Test Cases:**
    *   `test_gemini_conversation_success`:
        *   Mock `record_audio` to return a successful file path.
        *   Mock `os.environ.get` to return a dummy API key.
        *   Mock `google.generativeai` components to simulate a successful Gemini response.
        *   Assert that the function returns a message containing the simulated transcript, Gemini's response, and the recorded file path.
    *   `test_gemini_conversation_no_api_key`:
        *   Mock `os.environ.get` to return `None` for the API key.
        *   Assert that the function returns an error message about the missing API key.
    *   `test_gemini_conversation_record_audio_failure`:
        *   Mock `record_audio` to return an error message.
        *   Assert that the function returns an error message indicating the failure to record audio.
    *   `test_gemini_conversation_genai_not_available`:
        *   Temporarily set `GENAI_AVAILABLE = False` (or mock the import).
        *   Assert that the function returns the message about the Google Generative AI package not being installed.

## 5. Implementation Steps
1.  **Install `pytest` and `pytest-mock`:** `pip install pytest pytest-mock`
2.  **Create `tests/test_audio_server.py`:** Start with basic imports and a fixture for mocking.
3.  **Implement tests incrementally:** Add one test case at a time, ensuring it passes before moving to the next.
4.  **Run tests:** Execute `pytest` from the project root.

This plan provides a structured approach to testing the `audio_server_exp.py` file, which should help in identifying and fixing the current crash, and ensuring future stability.
