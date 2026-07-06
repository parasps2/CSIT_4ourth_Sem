from ollama import chat

response = chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": "Explain what AI is in simple words."
        }
    ]
)

print(response["message"]["content"])