import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import *
import json

def main():
    if api_key is None:
        raise RuntimeError("api key not found")

    # get model
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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    
    # let the agent iterate on a task until done
    for _ in range(20):
        # call the model and get response object
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        # get function calls
        message = response.choices[0].message
        # update message history with agent's response
        messages.append(message)

        if response.usage is None:
            raise RuntimeError("failed api request")

        # handle function calls
        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                result_message = call_function(tool_call, args.verbose)

                # add function calls to message history
                messages.append(result_message)

                # if content is empty
                if not result_message["content"]:
                    raise Exception("Error: function call failed")
        # no function call -> final response
        else:
            print("Final response:")
            # handle verbose
            if args.verbose:
                print(f"User prompt: {messages[1]["content"]}")
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")
                print(f"-> {result_message['content']}")
            print(response.choices[0].message.content)
            return
            
    # no response after max iterations
    print("Error: agent reached maximum iterations")
    sys.exit(10)
    
    
    


if __name__ == "__main__":
    main()
