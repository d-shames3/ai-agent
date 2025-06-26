import os
from dotenv import load_dotenv
from google import genai

load_dotenv(dotenv_path=".envrc")
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
        )
        print(response.text)
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
