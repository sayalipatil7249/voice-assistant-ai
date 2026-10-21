# Nova frontend

This static page records microphone audio and sends it to the FastAPI backend at `http://127.0.0.1:8000/voice`.

Follow setup instructions in the [project README](../README.md), then serve this folder locally:

```powershell
python -m http.server 5500
```

Open <http://127.0.0.1:5500>. The backend CORS defaults include this origin. Browser microphone access requires localhost or HTTPS.
