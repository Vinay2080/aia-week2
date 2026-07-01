#!/usr/bin/env python

import argparse
import httpx


def post_request(addr: str, messages: list, temperature: float = 0.7, max_tokens: int = 100):
    query_dict = {
        "model": "llama3.1:8b",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    return httpx.post(addr, json=query_dict, timeout=None)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--addr",
        type=str,
        default="http://localhost:8000/v1/chat/completions",
    )

    parser.add_argument(
        "--chat",
        type=str,
        nargs="*",
        default=[],
        help="Conversation messages.",
    )

    parser.add_argument(
        "--system-prompt",
        type=str,
        default="",
        help="Optional system prompt.",
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
    )

    parser.add_argument(
        "--max-tokens",
        type=int,
        default=100,
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    messages = []

    if args.system_prompt:
        messages.append(
            {
                "role": "system",
                "content": args.system_prompt,
            }
        )

    if args.chat:
        for i, text in enumerate(args.chat):
            role = "user" if i % 2 == 0 else "assistant"
            messages.append(
                {
                    "role": role,
                    "content": text,
                }
            )
    else:
        # Demonstration conversation (5 turns)
        messages = [
            {
                "role": "system",
                "content": "You are a helpful RAG assistant.",
            },
            {
                "role": "user",
                "content": "Hi",
            },
            {
                "role": "assistant",
                "content": "Hello!",
            },
            {
                "role": "user",
                "content": "What is your name?",
            },
            {
                "role": "assistant",
                "content": "I'm an AI assistant.",
            },
            {
                "role": "user",
                "content": "Explain embeddings in one sentence.",
            },
        ]

    response = post_request(
        args.addr,
        messages,
        args.temperature,
        args.max_tokens,
    )

    data = response.json()

    print(data["choices"][0]["message"]["content"])