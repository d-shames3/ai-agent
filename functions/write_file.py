from functions.check_valid_path import check_valid_path
import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        full_path = check_valid_path("file", working_directory, file_path, True)
    except Exception as e:
        return f"Error: {e}"
    
    if not os.path.exists(working_directory):
        try:
            os.makedirs(working_directory)
        except Exception as e:
            return f"Error: {e}"
    
    try:
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Opens or creates a file and writes/overwrites its contents, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file that we would like to write. Must be within the working directory file tree. If it does not exist, we will create it.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="String containing the content we would like to write to the file."
            ),
        },
    ),
)
