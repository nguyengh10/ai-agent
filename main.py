import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

from openai import OpenAI
import argparse

def main():
    if api_key is None:
        raise RuntimeError("api key not found")

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
    )

    # use argparse to get command line arguments 
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages=[
        {"role": "user", "content": args.user_prompt}
    ]
    

    # get response object
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages
    )
    if response.usage is None:
        raise RuntimeError("failed api request")
    
    # print token usage and response
    if args.verbose:
        print(f"User prompt: {messages[0]["content"]}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
