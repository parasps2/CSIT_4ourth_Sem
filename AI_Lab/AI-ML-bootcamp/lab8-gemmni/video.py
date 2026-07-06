from google import genai
import time

client = genai.Client(api_key="YOUR_API_KEY")

video = client.files.upload(
    file="video.mp4"
)

while not video.state or video.state.name != "ACTIVE":
    print("Processing...")
    time.sleep(5)
    video = client.files.get(name=video.name)

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {
            "type":"video",
            "uri":video.uri,
            "mime_type":video.mime_type
        },
        {
            "type":"text",
            "text":"Summarize this video."
        }
    ]
)

print(interaction.output_text)