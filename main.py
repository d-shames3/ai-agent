import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
import sys

load_dotenv(dotenv_path=".envrc")
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, help="add a prompt for the LLM to process")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    try:
        args = parser.parse_args()
        prompt = args.prompt
        messages = [
            types.Content(role="user", parts=[types.Part(text=prompt)])
        ]
    except SystemExit as e:
        print("please provide the required prompt wrapped in quotations")
        sys.exit(1)

    def call_gemini(messages) -> None:

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages
            )
            if args.verbose:
                print(f"User prompt: {prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(response.text)
            
        except Exception as e:
            print(e)

    call_gemini(messages)
        

if __name__ == "__main__":
    main()
