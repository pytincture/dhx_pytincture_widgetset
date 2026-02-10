"""Quick probe to validate tool calling through multiaiproxy."""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime

from multiproxy import multiaiproxy


def build_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": "get_current_date",
                "description": "Return the current local date on the server.",
                "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Return the current local time on the server.",
                "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
            },
        },
        {
            "type": "function",
            "function": {
                "name": "echo",
                "description": "Echo back a provided message.",
                "parameters": {
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                    "required": ["message"],
                    "additionalProperties": False,
                },
            },
        },
    ]


def tool_handlers():
    def get_current_date(_args):
        now = datetime.now().astimezone()
        return {"date": now.strftime("%Y-%m-%d")}

    def get_current_time(_args):
        now = datetime.now().astimezone()
        return {"time": now.strftime("%H:%M:%S")}

    def echo(args):
        return {"message": (args or {}).get("message", "")}

    return {
        "get_current_date": get_current_date,
        "get_current_time": get_current_time,
        "echo": echo,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Tool-call probe for multiaiproxy.")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))
    parser.add_argument(
        "--prompt",
        default="What is today's date? Use the appropriate tool.",
    )
    parser.add_argument(
        "--tool-choice",
        default="",
        help="Force a tool call (tool name).",
    )
    args = parser.parse_args()

    proxy = multiaiproxy()
    tools = build_tools()
    handlers = tool_handlers()
    proxy.register_tools(tool_handlers=handlers)

    system = (
        "You must call the appropriate tool to answer questions about date/time or echo. "
        "Do not answer without using tools."
    )
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": args.prompt},
    ]

    tool_choice = None
    if args.tool_choice:
        tool_choice = {"type": "function", "function": {"name": args.tool_choice}}

    print(f"Model: {args.model}")
    print(f"Prompt: {args.prompt}")
    print(f"Tools: {[t['function']['name'] for t in tools]}")
    if tool_choice:
        print(f"Tool choice: {json.dumps(tool_choice)}")

    text = []
    for chunk in proxy.chat_stream(
        messages,
        model=args.model,
        tools=tools,
        tool_choice=tool_choice,
    ):
        if isinstance(chunk, dict):
            delta = ((chunk.get("choices") or [{}])[0].get("delta") or {})
            content = delta.get("content")
            if content:
                print(content, end="", flush=True)
                text.append(content)
        elif isinstance(chunk, str):
            print(chunk, end="", flush=True)
            text.append(chunk)

    print()
    if not text:
        print("No content streamed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
