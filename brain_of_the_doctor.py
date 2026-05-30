from groq import Groq
import base64
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def analyze_image_with_query(query, model, image_path):
    client = Groq(api_key=GROQ_API_KEY)

    # Encode image in base64
    with open(image_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode("utf-8")

    # Send both text and image in a single "content" array
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
            ]
        }
    ]

    chat_completion = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return chat_completion.choices[0].message.content