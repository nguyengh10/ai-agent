import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": ("Read the contents of a file within the working directory. "
            "Returns up to the first 10,000 characters of the file. "
            "Use this when the user asks to open, read, inspect, or view "
            "the contents of a specific file."),
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": ("The path to the file to read, specified relative "
                        "to the working directory.")
                }
            }
        }
    }
}

def get_file_content(working_directory: str, file_path: str) -> str:
    # get absolute path to target directory
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # check whether target directory is inside working directory
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')

    # target directory is not a directory
    if not os.path.isfile(target_file):
        return (f'Error: File not found or is not a regular file: "{file_path}"')

    try:
        file_content_string = ""
        with open(target_file, "r") as f:
            file_content_string = f.read(10000)
            # After reading the first MAX_CHARS...
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
    except:
        return f"Error: cannot open {file_path}"

    return file_content_string