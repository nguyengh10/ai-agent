import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    # get absolute path to target directory
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    # check whether target directory is inside working directory
    valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not valid_target_file:
        return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')

    # target directory is not a directory
    if os.path.isdir(target_file):
        return (f'Error: Cannot write to "{file_path}" as it is a directory')

    # create directory if it's missing
    os.makedirs(working_dir_abs, exist_ok=True)

    try:
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except:
        return f'Error: could not open {file_path}'

