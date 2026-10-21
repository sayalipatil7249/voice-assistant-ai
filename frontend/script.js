const API_URL = "http://127.0.0.1:8000/voice";

const micButton = document.getElementById("micButton");
const micButtonText = document.getElementById("micButtonText");
const stopButton = document.getElementById("stopButton");
const stateLabel = document.getElementById("stateLabel");
const statusText = document.getElementById("statusText");
const timerEl = document.getElementById("timer");
const orb = document.getElementById("orb");
const responseAudio = document.getElementById("responseAudio");
const conversation = document.getElementById("conversation");
const emptyState = document.getElementById("emptyState");
const clearButton = document.getElementById("clearButton");

let mediaRecorder = null;
let audioChunks = [];
let stream = null;
let timerInterval = null;
let seconds = 0;
let lastAudioUrl = null;

function setState(state, label, status) {
  document.body.classList.remove("recording", "processing", "speaking");
  if (state) document.body.classList.add(state);
  stateLabel.textContent = label;
  statusText.textContent = status;
}

function updateTimer() {
  const mins = String(Math.floor(seconds / 60)).padStart(2, "0");
  const secs = String(seconds % 60).padStart(2, "0");
  timerEl.textContent = `${mins}:${secs}`;
}

function startTimer() {
  seconds = 0;
  updateTimer();
  timerInterval = setInterval(() => {
    seconds++;
    updateTimer();
  }, 1000);
}

function stopTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
}

function addMessage(role, text) {
  if (emptyState) emptyState.remove();

  const message = document.createElement("div");
  message.className = `message ${role.toLowerCase()}`;

  const label = document.createElement("div");
  label.className = "label";
  label.textContent = role === "USER" ? "YOU" : "NOVA";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  message.append(label, bubble);
  conversation.appendChild(message);
  conversation.scrollTop = conversation.scrollHeight;
}

async function startRecording() {
  try {
    // Ask the browser for microphone permission and receive the audio stream.
    stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // MediaRecorder captures the microphone stream into small audio chunks.
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
      if (event.data.size > 0) audioChunks.push(event.data);
    };

    mediaRecorder.onstop = processRecording;
    mediaRecorder.start();

    setState("recording", "Listening...", "Listening");
    micButtonText.textContent = "Recording...";
    micButton.setAttribute("aria-label", "Stop recording");
    stopButton.hidden = false;
    startTimer();
  } catch (error) {
    console.error(error);
    setState("", "Microphone permission is required", "Microphone error");
    alert("Could not access the microphone. Please allow microphone permission in your browser.");
  }
}

function stopRecording() {
  if (!mediaRecorder || mediaRecorder.state === "inactive") return;

  mediaRecorder.stop();
  stopTimer();
  stopButton.hidden = true;

  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
}

async function processRecording() {
  // Create one audio Blob from all MediaRecorder chunks.
  const blob = new Blob(audioChunks, { type: mediaRecorder.mimeType || "audio/webm" });

  // FormData packages the audio file for FastAPI's UploadFile parameter.
  const formData = new FormData();
  formData.append("audio", blob, "voice.webm");

  setState("processing", "Thinking...", "Processing");
  micButton.disabled = true;
  micButtonText.textContent = "Processing...";

  try {
    // Send the recorded audio to the existing FastAPI /voice endpoint.
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData
    });

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }

    // The backend returns a WAV FileResponse, so read it as a Blob.
    const responseBlob = await response.blob();

    // Convert the Blob into a browser-playable temporary URL.
    if (lastAudioUrl) URL.revokeObjectURL(lastAudioUrl);
    lastAudioUrl = URL.createObjectURL(responseBlob);

    responseAudio.src = lastAudioUrl;
    responseAudio.currentTime = 0;

    setState("speaking", "Assistant is speaking...", "Speaking");
    micButtonText.textContent = "Start speaking";

    // Play Piper's generated WAV response automatically.
    await responseAudio.play();
  } catch (error) {
    console.error(error);
    setState("", "Something went wrong", "Connection error");
    micButtonText.textContent = "Try again";
    alert("Could not reach the FastAPI server. Make sure Uvicorn is running and CORS is configured.");
  } finally {
    micButton.disabled = false;
  }
}

responseAudio.addEventListener("play", () => {
  setState("speaking", "Assistant is speaking...", "Speaking");
});

responseAudio.addEventListener("ended", () => {
  setState("", "How can I help you?", "Ready");
  micButtonText.textContent = "Start speaking";
  timerEl.textContent = "00:00";
});

responseAudio.addEventListener("error", () => {
  setState("", "Audio playback failed", "Playback error");
  micButton.disabled = false;
});

micButton.addEventListener("click", () => {
  if (mediaRecorder && mediaRecorder.state === "recording") {
    stopRecording();
  } else if (!micButton.disabled) {
    startRecording();
  }
});

stopButton.addEventListener("click", stopRecording);

clearButton.addEventListener("click", () => {
  conversation.innerHTML = `
    <div class="empty-state" id="emptyState">
      <div class="empty-icon">✦</div>
      <p>Your conversation will appear here.</p>
      <span>Press the microphone and start talking.</span>
    </div>
  `;
  responseAudio.pause();
  responseAudio.removeAttribute("src");
  setState("", "How can I help you?", "Ready");
  timerEl.textContent = "00:00";
});

window.addEventListener("beforeunload", () => {
  if (lastAudioUrl) URL.revokeObjectURL(lastAudioUrl);
});
