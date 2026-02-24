import os



def get_files_info(working_directory, directory="."):
    try:    
        working_directory = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_directory, directory))
        # Will be True or False
        valid_target_dir = os.path.commonpath([working_directory, target_dir]) == working_directory
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) is False:
            return f'Error: "{directory}" is not a directory'

        items = os.listdir(target_dir)
        for file_name in os.listdir(target_dir):
            filepath = os.path.join(target_dir, file_name)
            is_dir = os.path.isdir(filepath)
            file_size = os.path.getsize(filepath)
            items.append(
                f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(items)
    except Exception as e:
        return f"Error listing files: {e}"