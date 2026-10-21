from pathlib import Path
import tempfile
from TTS.api import TTS
from app.config import VOICE_REFERENCE_PATH

# XTTS-v2 model
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"   #loads XTTS-v2.

# Your recorded voice
REFERENCE_VOICE = VOICE_REFERENCE_PATH

# Load the model once when the application starts
tts = TTS(MODEL_NAME)
  

#build function to generate speech 
def generate_speech(text):
    if not REFERENCE_VOICE.is_file():
        raise FileNotFoundError(
            f"Voice reference not found: {REFERENCE_VOICE}. "
            "Set VOICE_REFERENCE_PATH to a local WAV recording."
        )

    # Create a unique temporary WAV file
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav",delete=False)

    output_path = temp_file.name  # Get the path of the temporary file

    temp_file.close() # Close the temporary file because Piper will write the audio to this path

    # Generate speech using your cloned voice
    tts.tts_to_file(
        text=text,
        speaker_wav=str(REFERENCE_VOICE),
        language="en",
        # speed=1.15,
        file_path=output_path
    )

    return output_path

    #Build the command that tells Piper which voice model to use and where to save the generated audio.
    # command = [
    #     "piper",                        #runs the Piper TTS program
    #     "--model", str(MODEL_PATH),     #"--model" → tells Piper which voice/model to use , #MODEL_PATH → path of our downloaded voice model
    #     "--output_file", output_path    #tells Piper where to save the generated speech
    # ]

    #Give text to piper 
    # result = subprocess.run(       #subprocess.run() => executes piper command and wait until it finishes. , result => CompletedProcess object contians information about executedcommand 
    #     command,  
    #     input=text,     #sends our text to Piper
    #     text=True       #tells Python that the input is normal text/string rather than raw bytes
    # )


    # return output_path  #Return the path of the generated audio file


