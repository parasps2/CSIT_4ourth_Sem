from google import genai

client = genai.Client(api_key="YOUR_API_KEY")

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input=[
        {
            "type":"video",
            "uri":"https://www.youtube.com/watch?v=9hE5-98ZeCg"
        },
        {
            "type":"text",
            "text":"Summarize this YouTube video."
        }
    ]
)

print(interaction.output_text)