from functions.check_valid_path import check_valid_path
import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        full_path = check_valid_path("file", working_directory, file_path)
    except Exception as e:
        return f"Error: {e}"

    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(f.read()) > MAX_CHARS:
                file_content_string += f"[...File {file_path} truncated at 10000 characters]"
    except Exception as e:
        return f"Error: {e}"
    
    return file_content_string

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Opens a file and returns its contents as a string, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that we would like to read from. Must be within the working directory file tree.",
            ),
        },
    ),
)
