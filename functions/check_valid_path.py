import os

def check_valid_path(type, working_directory, path=None, write_mode=False):
    working_dir = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_dir, path))

    match type:
        case "directory":
            validation_func = os.path.isdir
            keyword = "list"
        case "file":
            validation_func = os.path.isfile
            if not write_mode:
                keyword = "read"
            else:
                keyword = "write"
        case "exec":
            validation_func = os.path.exists
            keyword = "execute"
            if not full_path.endswith(".py"):
                raise Exception(f"{path} is not a Python file.\n")

    if not full_path.startswith(working_dir):
        raise Exception(f'Cannot {keyword} "{path}" as it is outside the permitted working directory\n')

    if not write_mode:
        if not validation_func(full_path):
            if type != "exec":
                raise Exception(f"{path} is not a {type}\n")
            else: 
                raise Exception(f'File "{path}" not found\n')

    
    return full_path
