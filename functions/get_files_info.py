import os

def get_files_info(working_directory: str, directory: str=".") -> str:
    # get absolute path to target directory
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    # initialize output
    directory_name = "current" if directory=="." else directory
    res = [f"Result for '{directory_name}' directory:"]

    # check whether target directory is inside working directory
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        res.append(f'    Error: Cannot list "{directory}" as it is outside the permitted working directory')

    # target directory is not a directory
    elif not os.path.isdir(target_dir):
        res.append(f'    Error: "{directory}" is not a directory')

    # found target directory in working directory
    else:
        
        # get files in directory
        items = os.listdir(target_dir)
        res.extend([""] * len(items))

        # get attributes of files
        sizes = [os.path.getsize(os.path.join(target_dir, file)) for file in items]
        is_dir = [os.path.isdir(os.path.join(target_dir, file)) for file in items]

        # format output
        for i in range(len(items)):
            res[i+1] = f"  - {items[i]}: file_size={sizes[i]} bytes, is_dir={is_dir[i]}"
    return "\n".join(res)