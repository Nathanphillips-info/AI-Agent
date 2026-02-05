import os


def get_files_info(working_directory, directory="."):
    working_directory = os.path.abspath()
    os.path.join(working_directory, directory)