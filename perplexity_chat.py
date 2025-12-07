import os
import requests

API_KEY = os.environ["PERPLEXITY_API_KEY"]

resp = requests.post(
    "https://api.perplexity.ai/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "model": "sonar-pro",
        "messages": [
            {"role": "user", "content": "Explain macOS Spaces in simple terms."}
        ],
    },
    timeout=60,
)

data = resp.json()
print(data["choices"][0]["message"]["content"])
