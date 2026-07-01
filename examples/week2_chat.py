#!/usr/bin/env python

import argparse
import httpx


def post_request(addr: str, messages: list, temperature: float, max_tokens: int):
    query_dict = {
        "model": "llama3.1:8b",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    return httpx.post(addr, json=query_dict, timeout=None)


def print_response(title: str, response):
    print(f"\n=== {title} ===")

    if response.status_code != 200:
        print(f"Status: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    print(data["choices"][0]["message"]["content"])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--addr",
        type=str,
        default="http://localhost:8000/v1/chat/completions",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # -------------------------------------------------
    # Single-turn conversation
    # -------------------------------------------------
    messages = [
        {
            "role": "user",
            "content": "Hello! Tell me about vector databases.",
        }
    ]

    response = post_request(args.addr, messages, 0.7, 100)
    print_response("Single Turn", response)

    # -------------------------------------------------
    # Multi-turn conversation
    # -------------------------------------------------
    conversation = [
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello!"},
        {"role": "user", "content": "What did I just say?"},
    ]

    response = post_request(args.addr, conversation, 0.7, 100)
    print_response("Multi Turn", response)

    # -------------------------------------------------
    # System Prompt
    # -------------------------------------------------
    system_messages = [
        {
            "role": "system",
            "content": "You are a helpful RAG assistant. Be concise.",
        },
        {
            "role": "user",
            "content": "Explain embeddings.",
        },
    ]

    response = post_request(args.addr, system_messages, 0.7, 100)
    print_response("System Prompt", response)

    # -------------------------------------------------
    # Temperature comparison
    # -------------------------------------------------
    prompt = [
        {
            "role": "user",
            "content": "Write one sentence about artificial intelligence.",
        }
    ]

    response = post_request(args.addr, prompt, 0.0, 100)
    print_response("Temperature = 0.0", response)

    response = post_request(args.addr, prompt, 1.0, 100)
    print_response("Temperature = 1.0", response)

    # -------------------------------------------------
    # max_tokens comparison
    # -------------------------------------------------
    response = post_request(args.addr, prompt, 0.7, 20)
    print_response("max_tokens = 20", response)

    response = post_request(args.addr, prompt, 0.7, 100)
    print_response("max_tokens = 100", response)