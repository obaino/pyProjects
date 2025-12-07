import os
import sys
import requests

API_KEY = os.environ.get("PERPLEXITY_API_KEY")
if not API_KEY:
    sys.exit("PERPLEXITY_API_KEY is not set. Please export it in your shell.")

API_URL = "https://api.perplexity.ai/chat/completions"
MODEL = "sonar-pro"  # or another Sonar model name [web:89]

def ask_perplexity(prompt, history):
    """
    Send the current user prompt + previous turns as chat history.
    """
    messages = history + [{"role": "user", "content": prompt}]

    resp = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": messages,
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    answer = data["choices"][0]["message"]["content"]
    return answer

def main():
    print("Perplexity interactive chat. Type 'exit' or Ctrl+C to quit.\n")
    history = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant for a macOS user with basic Python "
                "knowledge. Answer briefly and clearly."
            ),
        }
    ]

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break

        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            break
        if not user_input:
            continue

        try:
            answer = ask_perplexity(user_input, history)
        except Exception as e:
            print(f"[Error contacting Perplexity: {e}]")
            continue

        print("\nAssistant:\n" + answer + "\n")

        # Update history so the model keeps context
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
