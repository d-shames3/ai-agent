import os

def check_valid_path(type, working_directory, path=None):
    working_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_dir, path))

    if type == "directory":
        validation_func = os.path.isdir
        keyword = "list"
    else:
        validation_func = os.path.isfile
        keyword = "read"
        
    if not full_path.startswith(working_dir):
        raise Exception(f"Cannot {keyword} {path} as it is outside the permitted working directory")

    if not validation_func(full_path):
        raise Exception(f"Error: {path} is not a {type}")
    
    return full_path