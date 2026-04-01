import os
from google import genai
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Allows AI Agent to write python code to a file within its working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the file path where the agent is allowed to write python files",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content that specifies what the agent should write code to accomplish",    
            ),
        },
    ),
)



def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        
        parent_path = os.path.dirname(abs_file_path)
        os.makedirs(parent_path, exist_ok=True)
        
        if os.path.isdir(abs_file_path):
            f'Error: Cannot write to "{file_path}" as it is a directory'
        
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error Writing to file:{e}'
    
