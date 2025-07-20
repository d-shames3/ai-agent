from functions.check_valid_path import check_valid_path
import os

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
