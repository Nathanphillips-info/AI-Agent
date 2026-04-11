import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types 
from prompts import SYSTEM_PROMPT 
from functions.call_functions import available_functions, call_function, function_map
import sys

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    for _ in range(0, 20):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents= messages,
            config=types.GenerateContentConfig(
                tools = [available_functions], 
                system_instruction=SYSTEM_PROMPT,
            temperature=0
            ),
        )
        
        if response.candidates:
            for i in response.candidates:
                messages.append(i.content)

        usage = response.usage_metadata
        if usage is None:
            raise RuntimeError("GEMINI_API_KEY failed to run")
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {usage.prompt_token_count}")
            print(f"Response tokens: {usage.candidates_token_count}")
        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise RuntimeError("Error: result of function could not be completed")
                if not function_call_result.parts[0].function_response:
                    raise RuntimeError("Error: result of the function could not be found")
                if not function_call_result.parts[0].function_response.response:
                    raise ValueError("Error: no response from the executed function")    

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result.parts[0])
            messages.append(types.Content(role="user", parts=function_responses))

        else:
            print(response.text)
            return
    
    print("Maximum number of iterations reached, could not complete action")
    sys.exit(1)

if __name__ == "__main__":
    main()


