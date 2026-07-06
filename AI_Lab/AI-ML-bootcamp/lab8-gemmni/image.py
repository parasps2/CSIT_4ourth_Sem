from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

image = client.files.upload(
    file="cat.jpg"
)

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {
            "type":"image",
            "uri":image.uri,
            "mime_type":image.mime_type
        },
        {
            "type":"text",
            "text":"Describe this image."
        }
    ]
)

print(interaction.output_text)