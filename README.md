# Nova Voice Assistant

Nova is a local, browser-based voice assistant. The frontend records microphone audio and sends it to a FastAPI backend. The backend transcribes it with OpenAI Whisper, generates a reply with Qwen 2.5 1.5B Instruct, synthesizes speech with Coqui XTTS-v2, and returns a WAV file for playback.

## How it works

```text
Browser microphone → POST /voice → Whisper transcription → Qwen response → XTTS-v2 speech → WAV playback
```

The current `/voice` endpoint returns audio only. It does not return the transcription or generated reply as text, so the conversation panel does not display those values yet. The `/speak` endpoint accepts text and returns synthesized audio.

## Project layout

```text
app/
  main.py             FastAPI app and CORS configuration
  config.py           Environment based settings
  api/routes.py       /voice and /speak endpoints
  services/stt.py     Whisper transcription
  services/llm.py     Qwen response generation
  services/tts.py     XTTS-v2 audio generation
frontend/             Static browser UI
```

## Requirements

- Python 3.10 or 3.11 is recommended. The TTS dependency may not install on newer Python versions.
- FFmpeg must be installed and available on `PATH`; Whisper uses it to decode browser audio.
- Model downloads require internet access the first time each service starts. Whisper, Qwen, and XTTS-v2 use substantial disk space and memory; a GPU can improve response time.
- A WAV voice reference is required by XTTS-v2. Use a recording you own or have permission to use. Keep it private: audio recordings are ignored by Git.

## Setup

Create and activate a virtual environment, then install the Python dependencies:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install FFmpeg separately for your operating system. Copy `.env.example` to `.env`, then set `VOICE_REFERENCE_PATH` to your local WAV sample if it is not named `en_v1_011.wav` in the project root. `.env` and audio files are excluded from version control.

Start the API from the project root:

```powershell
uvicorn app.main:app --reload
```

Start the static frontend in a second terminal:

```powershell
cd frontend
python -m http.server 5500
```

Open <http://127.0.0.1:5500>. The API docs are at <http://127.0.0.1:8000/docs>. CORS defaults allow the frontend on ports 5500 and 3000; set `CORS_ORIGINS` to a comma-separated list of exact origins when using a different frontend URL.

## API

### `POST /voice`

Multipart form upload with a field named `audio`. Returns generated `audio/wav`.

### `POST /speak`

JSON request body:

```json
{"text": "Hello from Nova."}
```

Returns generated `audio/wav`.

## Notes

- Model weights and caches are downloaded by the ML libraries at runtime; do not commit them.
- The root `test_*.py` files are manual experiments that load models or make external requests, not an automated test suite.
- This is a local project starter. Before exposing it to a network, add authentication, upload size and duration limits, request timeouts, and deployment-specific CORS origins.

## License

No license is included yet. Choose and add a license before redistributing or accepting outside contributions.
