from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import CORS_ORIGINS

#1.Create FastAPI application 
app = FastAPI(
    title="Nova Voice Assistant",
    description="A local voice assistant powered by Whisper, Qwen, and XTTS-v2.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#2.Include that router into main application
from app.api.routes import router
#connect that router to the application
app.include_router(router)

