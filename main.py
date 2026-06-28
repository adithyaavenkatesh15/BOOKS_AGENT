#main.py
import os
import json
import requests
from dotenv import load_dotenv

from tools import book_search
from memory import load_memory, save_memory
from prompt import SYSTEM_PROMPT

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")

MODEL = "openai/gpt-oss-20b"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# -----------------------------
# Tool Schema
# -----------------------------
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "book_search",
            "description": "Search books by title, author, topic or keyword.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Book title, author, keyword or topic"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


def call_llm(messages):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "tools": TOOLS
    }

    response = requests.post(
        OPENROUTER_URL,
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    return response.json()


def run_tool(tool_call):

    tool_name = tool_call["function"]["name"]

    tool_args = json.loads(
        tool_call["function"]["arguments"]
    )

    if tool_name == "book_search":

        return book_search(
            tool_args["query"],
            GOOGLE_BOOKS_API_KEY
        )

    return "Unknown tool."


def agent_loop(user_input):

    memory = load_memory()

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(memory)

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    result = call_llm(messages)

    message = result["choices"][0]["message"]

    # Tool Calling
    if "tool_calls" in message and message["tool_calls"]:

        tool_call = message["tool_calls"][0]

        tool_result = run_tool(tool_call)

        messages.append(message)

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": "book_search",
                "content": tool_result
            }
        )

        # Ask the LLM to format the tool result nicely
        second_response = call_llm(messages)

        final_message = second_response["choices"][0]["message"]["content"]

        messages.append(
            {
                "role": "assistant",
                "content": final_message
            }
        )

        save_memory(messages[1:])

        return final_message

    final_answer = message.get(
        "content",
        "No response generated."
    )

    save_memory(messages[1:])

    return final_answer


if __name__ == "__main__":

    print("=" * 60)
    print("📚 Welcome to the Book Search Agent")
    print("=" * 60)

    print("\nExamples:")
    print("• Search Atomic Habits")
    print("• Find Harry Potter")
    print("• James Clear books")
    print("• Give me 5 Agentic AI books")
    print("• Best Python books")
    print("• Machine Learning books")
    print()

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:

            answer = agent_loop(user_input)

            print("\nAgent:")
            print(answer)
            print()

        except Exception as e:

            print("Error:", e)