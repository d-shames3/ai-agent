from functions.check_valid_path import check_valid_path
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        _ = check_valid_path("exec", working_directory, file_path)
    except Exception as e:
        return f"Error: {e}"
    
    command = ["uv", "run", file_path]
    print(command)
    if args:
        command.extend(args)
    
    try:
        result = subprocess.run(
            command, 
            timeout=30, 
            capture_output=True, 
            cwd=working_directory
        )

        if not result:
            return "No output produced"
        
        output = ""
        
        if result.stdout:
            stdout = f"STDOUT: {result.stdout}\n"
            output += stdout
        
        if result.stderr:
            stderr = f"STDERR: {result.stderr}\n"
            output += stderr
        
        if result.returncode:
            return_code = f"Process exited with return code {result.returncode}\n"
            output += return_code

        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file using subprocess module and returns formatted output, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the executable. Must be within the file tree of the working directory. ",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of any additional arguments need to pass to the subprocess command.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)
