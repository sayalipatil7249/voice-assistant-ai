from gtts import gTTS

# Text that we want to convert into speech
text = """
Good morning. My name is Sayali.
I am a Computer Science and Engineering graduate.
I am currently working on an AI-based voice assistant.
"""

# Create an Indian English voice
tts = gTTS(
    text=text,
    lang="en",
    tld="co.in"
)

# Save the generated speech
tts.save("indian_voice.mp3")

print("Indian English voice generated successfully!")