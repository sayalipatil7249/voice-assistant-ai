from fastapi import APIRouter   #so APIRoter is the router object that groups related API endpoints 
from app.services.stt import transcribe_audio   #here we connect the stt file to fastapi
from fastapi.responses import FileResponse   #needs to send that file itself back to whoever made the request
from pydantic import BaseModel
from app.services.tts import generate_speech
from app.services.llm import generate_response

router = APIRouter()

#1.lets create the first api ...voice api 
from fastapi import UploadFile

#1.API for Speech To Text
@router.post("/voice")
async def receive_voice(audio: UploadFile):

    # Step 1: Convert voice to text
    text = await transcribe_audio(audio)

    # Step 2: Send text to LLM
    response = generate_response(text)

    # Step 3: Convert LLM response to speech
    audio_path = generate_speech(response)

    # Step 4: Return the generated audio
    return FileResponse(
        audio_path,
        media_type="audio/wav",
        filename="response.wav"
    )

#2.API for Text To Speech 
class SpeechRequest(BaseModel):
    text:str   #the input text should be a string ...here it checks type 

@router.post("/speak")
async def speak(request: SpeechRequest):
    output_path = generate_speech(request.text)

    #Don't return JSON. Send this audio file back to the client.
    return FileResponse(
        output_path,
        media_type="audio/wav",
        filename="response.wav"
    )