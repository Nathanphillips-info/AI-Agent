import os
from dotenv import load_dotenv
from google import genai

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        )

    usage = response.usage_metadata
    if usage is None:
        raise RuntimeError("GEMINI_API_KEY failed to run")
    
    print(f"Prompt Tokens: {usage.prompt_token_count}")
    print(f"Usage Tokens: {usage.candidates_token_count}")
    print(response.text)

if __name__ == "__main__":
    main()
