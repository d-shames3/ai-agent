import os
from functions.check_valid_path import check_valid_path
from google.genai import types

def get_files_info(working_directory, directory=None):
    dir_name = working_directory if directory is None or directory == "." else directory
    
    try:
        full_path = check_valid_path("directory", working_directory, directory)
    except Exception as e:
        return f"Error: {e}"

    try:
        dir_list = os.listdir(full_path)
        data = f"Results for {dir_name} directory:\n"

        for obj in dir_list:
            obj_path = os.path.join(full_path, obj)
            size = os.path.getsize(obj_path)
            type = os.path.isdir(obj_path)        
            line = f'- {obj}: file_size={size} bytes, is_dir={type}\n'
            data += line    

        return data
    
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
