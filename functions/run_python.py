from functions.check_valid_path import check_valid_path
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = check_valid_path("exec", working_directory, file_path)
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
            return_code = f"Process exited with return code {e.returncode}\n"
            output += return_code

        return output
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
