from TTS.api import TTS

# Load XTTS-v2 model
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

# Generate speech using your recorded voice
tts.tts_to_file(
    text="Hello, My name is Sayali Patil. And i was completed my btech degree from KIT's College of Engineering, Kolhapur. My Academedic CGPA is 8.18.i have good knowledge of python , java , sql also i am learning the AI . I had work on projects like Mental health chatbot , AI Resume Analyzer , Rag application , etc. Now I am looking for an opportunity where i can apply my technical skills. Thank You!!",
    speaker_wav="python_reference.wav",  #Use this recording as the reference for the speaker's voice
    language="en",
    speed=1.25,
    file_path="xtts_test.wav"
)

print("XTTS voice generation completed!")