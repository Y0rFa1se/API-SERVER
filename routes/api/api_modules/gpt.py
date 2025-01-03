import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def render_requests(system: str, requests: str) -> dict:
    return [{
        "role": "system",
        "content": system
    },
    {
        "role": "user",
        "content": requests
    }]

async def render_system_requests(system: str) -> dict:
    return [{
        "role": "system",
        "content": system
    }]

async def render_requests_with_image(system: str, requests: str, image_url: str) -> dict:
    return [{
        "role": "system",
        "content": system
    },
    {
        "role": "user",
        "content": requests
    },
    {
        "role": "user",
        "content": [{
            "type": "image_url",
            "image_url": {
                "url": image_url
            }
        }]
    }]

async def openai_request(password: str, query: list, model: str="gpt-4o-mini") -> str:
    if password != os.getenv("GUEST_PASSWORD"):
        return "Invalid password"
    
    completion = openai.chat.completions.create(
        model=model,
        messages=query,
        stream=False
    )

    return completion.choices[0].message.content