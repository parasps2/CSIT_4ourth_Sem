from ollama import chat

response = chat(
    model="qwen2.5vl:7b",
    messages=[
        {
            "role": "user",
            "content": "Describe this construction site.",
            "images": [r"ollma\site.jpg"],
        }
    ],
)

print(response["message"]["content"])