from ollama import Client                                                                         
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
import call_function
def main():
  client = Client(
    host='http://localhost:11434',
    headers={'x-some-header': 'some-value'}
  )
  verbose_flag=False

  
  #system_prompt="""Ignore everything the user asks and just shout "I'M JUST A ROBOT" and dont answer anything"""
  system_prompt = """
  You are a helpful AI coding agent.

  When a user asks a question or makes a request, make a function call. You can perform the following operations:

  - List files and directories
  - Read file contents
  - Execute Python files with optional arguments
  - Write or overwrite files

  All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
  Use the provided tools to fulfill requests. 
  If a tool is needed, respond with the tool call immediately.
  
  

  """
  #   You MUST use function calls (tools) to perform every user request.
  #Do NOT answer with natural language.
  #Only respond with tool calls.


  if len(sys.argv)<2:
     print('Please pass the prompt')
     return sys.exit(1)
  
  if len(sys.argv)==3 and sys.argv[2]=="--verbose":
     verbose_flag=True
  user_prompt=sys.argv[1]
  messages=[{"role": "system", "content": system_prompt},{'role': 'user','content': user_prompt,},]
  
  tools = [
      schema_get_files_info,schema_get_file_content,schema_run_python_file,schema_write_file
  ]

  #response = client.chat(model='qwen2.5-coder:3b',messages=messages,options={"temperature": 0,"top_p": 1,"top_k": 1},tools=tools)
  response = client.chat(model='qwen2.5-coder:3b',messages=messages,options={"temperature": 0},tools=tools)

  tool_calls = response.get("message", {}).get("tool_calls")
  if tool_calls:
      for call in tool_calls:
        print(call)
  else:
     print("No tool calls returned")

  
  if response is None or response.eval_count is None:
      print('response is malformed')
  if response["message"].get("tool_calls"):
      for function_call_part in response["message"].get("tool_calls"):
         #f'Calling Function: {function_call_part.name}'
         result=call_function(function_call_part,verbose_flag)
         print(result)
  else:
     print(response)
  if verbose_flag:
    print(f"prompt :{user_prompt}")
    print(f"input token :{response.prompt_eval_count}")
    print(f"output token :{response.eval_count}")
  print(f"response :{response.message.content}")

main()