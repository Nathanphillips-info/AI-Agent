import os



def get_files_info(working_directory, directory="."):
    working_directory = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory, directory))
    # Will be True or False
    valid_target_dir = os.path.commonpath([working_directory, target_dir]) == working_directory
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(target_dir) is False:
        return f'Error: "{directory}" is not a directory'

    items = os.listdir(target_dir)
    for item_name in items:
        item_path = os.path.join(target_dir, item_name)
    