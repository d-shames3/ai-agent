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
from functions.call_function import call_python_function

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
        model: str="gemini-2.5-flash"
) -> None:
    
    messages_copy = messages.copy()
    i = 19
    while i > 0:
        try:
            response = client.models.generate_content(
                model=model,
                contents=messages_copy,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=SYSTEM_PROMPT,
                )
            )
            if args.verbose:
                print(f"User prompt: {args.prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            
            function_calls = []
            for candidate in response.candidates:
                messages_copy.append(candidate.content)
                for part in candidate.content.parts:
                    if part.function_call:
                        function_calls.append(part.function_call)
            if response.function_calls:
                for call in response.function_calls:
                    if call not in function_calls:
                        function_calls.append(call)
            if not function_calls and response.text is not None:
                print(response.text)
                break
            if function_calls:
                for call in function_calls:
                    try:
                        output = call_python_function(call, verbose=True if args.verbose else False)
                        if not output.parts[0].function_response.response:
                            raise Exception("error fatal")
                        messages_copy.append(
                            types.Content(role="user", parts=[types.Part(text=str(output.parts[0].function_response.response))])
                        )
                        if args.verbose:
                            print(f"-> {output.parts[0].function_response.response}")
                    except Exception as e:
                        print({e})
            i-=1
        except Exception as e:
            print(e)
            break



if __name__ == "__main__":
    main()
