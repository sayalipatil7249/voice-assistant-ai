#stt model(i.e. whisper) using openai-whisper package that gives us the code/tools to work with Whisper.
import whisper 
#1.Load Base Whisper Model 
model = whisper.load_model("base")

#3.create temporary file to save the uploaded audio temporarily.
import tempfile    #tempfile is the built-in module used to create temporary files 
import os
#2.Convert Speech to text 
async def transcribe_audio(audio):
    #2.1:create unique temporary file 
    with tempfile.NamedTemporaryFile(delete= False , suffix=".mpeg") as temp_file:
        audio_data = await audio.read()    #reads the actual audio data from the UploadFile.
        temp_file.write(audio_data)        #Write those bytes into our temporary file
        temp_path = temp_file.name         #Get the temporary file's path...i.e. temp_path contians that location where that temp file is stored 

    #2.1:first decode the audio file before giving to the transcribe/whisper using ffmpeg 

    try:
        #2.2:give audio file to whisper to convert audio into text
        result = model.transcribe(temp_path)
        #2.3:Extract text
        text = result["text"].strip()

        #2.4:return text
        return text
    
    finally:
        #2.5: remove the temporary file after the whisper reads it
        os.remove(temp_path)
    
     


