import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import SYSTEM_PROMPT
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file

load_dotenv(dotenv_path=".envrc")
api_key = os.environ.get("GEMINI_API_KEY")

def main():
    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, help="add a prompt for the LLM to process")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()
    prompt = args.prompt
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    call_gemini(client, messages, args, available_functions)

def call_gemini(
        client: genai.Client,
        messages: list[types.Content],
        args: argparse.Namespace,
        available_functions: types.Tool,
        model: str="gemini-2.0-flash-001"
) -> None:

    try:
        response = client.models.generate_content(
            model=model,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=SYSTEM_PROMPT,
            )
        )
        if args.verbose:
            print(f"User prompt: {args.prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)
        if response.function_calls:
            for call in response.function_calls:
                print(f"Calling function: {call.name}({call.args})")
        
    except Exception as e:
        print(e)



if __name__ == "__main__":
    main()
