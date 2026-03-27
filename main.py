import os, argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types 
from prompts import SYSTEM_PROMPT 
from functions.call_functions import available_functions

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
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents= messages,
        config=types.GenerateContentConfig(
            tools = [available_functions], 
            system_instruction=SYSTEM_PROMPT,
        temperature=0
        ),
    )


    usage = response.usage_metadata
    if usage is None:
        raise RuntimeError("GEMINI_API_KEY failed to run")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")
        print(response.text)
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

    else:
        print(response.text)

if __name__ == "__main__":
    main()
