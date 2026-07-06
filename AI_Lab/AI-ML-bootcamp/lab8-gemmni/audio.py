from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

audio = client.files.upload(
    file="speech.mp3"
)

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {
            "type":"audio",
            "uri":audio.uri,
            "mime_type":audio.mime_type
        },
        {
            "type":"text",
            "text":"Transcribe this audio."
        }
    ]
)

print(interaction.output_text)