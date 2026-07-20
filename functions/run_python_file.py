import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": ("Run a Python script. Use this whenever the user asks to run, execute, "
            "launch, or test a Python file."),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": ("The path to the Python file to execute, specified "
                        "relative to the working directory."),
                },
                "args": {
                    "type": "array",
                    "description": ("A list of command-line arguments to pass to the "
                        "Python script. Omit or provide an empty list if "
                        "no arguments are needed."),
                    "items": {
                        "type": "string"
                    }
                }
            },
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    # get absolute path to target directory
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # check whether target directory is inside working directory
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')

    # target directory is not a directory
    if not os.path.isfile(target_file):
        return (f'Error: "{file_path}" does not exist or is not a regular file')

    # not a python file
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'

    # build run command
    command = ["python", target_file]
    if args:
        command.extend(args)

    # run command
    try:
        process_output = subprocess.run(command, capture_output=True, text=True, timeout=30)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    # exited with nonzero return code
    if process_output.returncode != 0:
        return f"Process exited with code {process_output.returncode}"

    if process_output.stdout is None and process_output.stderr is None:
        return "No output produced"

    return f"STDOUT: {process_output.stdout}\nSTDERR: {process_output.stderr}"

    