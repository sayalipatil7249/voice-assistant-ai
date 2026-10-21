from app.services.tts import generate_speech


text = "Hello, my name is Sayali. This is my voice assistant.Thank You!!"

output_path = generate_speech(text)

print("Speech generated successfully!")
print("Audio file:", output_path)