from app.services.llm import generate_response

question = "What is machine learning?"

response = generate_response(question)

print("Question:", question)
print("Answer:", response)