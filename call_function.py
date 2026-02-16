from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
import json

working_directory='calculator'

def call_fuction(function_call_part,verbose=False):
    if verbose:
        print(f'Calling function: {function_call_part.name}({function_call_part.args})')
    else:
        print(f'Calling function: {function_call_part.name}')
    result=''
    if function_call_part.name=="get_files_info":
        result = get_files_info(working_directory,**function_call_part.args)
    if function_call_part.name=="get_file_content":
        result = get_file_content(working_directory,**function_call_part.args)
    if function_call_part.name=="run_python_file":
        result = run_python_file(working_directory,**function_call_part.args)
    if function_call_part.name=="write_file":
        result = write_file(working_directory,**function_call_part.args)
    
    if result=='' or result is None:
        return {
        "role": "tool",
        "name": function_call_part.name,
        "content": json.dumps({
            "error": f"Unknown function: {function_call_part.name}"
        })
        }
    return {
    "role": "tool",
    "name": function_call_part.name,
    "content": json.dumps({
        "result": result
    })
    }