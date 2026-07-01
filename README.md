# Week 2: OpenAI-Compatible Chat API

## Overview

Understand the API internals, build a multi-turn chat client with system prompt support, and write your first API tests.

## Tasks

### 1. Code Reading Session
- Open `api/app/routes.py` and read the `chat_completions()` function
- Identify the three phases: (1) format conversion OpenAI→Ollama, (2) Ollama call, (3) response conversion Ollama→OpenAI
- Open `api/app/models.py` and understand Pydantic validation for requests/responses
- Trace how `ChatCompletionRequest` validates incoming JSON automatically
- Open `api/app/ollama_client.py` and see how the HTTP client wrapper works

### 2. Test the Endpoint
- Create `examples/week2_chat.py` to test various scenarios
- Test single-turn conversation: one user message
- Test error handling: invalid model name, empty messages array
- Test parameter variations: temperature 0.0 vs 1.0, different max_tokens values
- Use httpx to make POST requests to `http://localhost:8000/v1/chat/completions`
- Parse the response JSON and extract the answer: `data["choices"][0]["message"]["content"]`

### 3. Add Conversation History
- Modify `examples/week2_chat.py` to support multi-turn conversations
- Send messages array with history:
  ```json
  [
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello!"},
    {"role": "user", "content": "What's your name?"}
  ]
  ```
- Verify the model remembers context from previous messages
- Experiment: how many turns can you maintain coherent conversation?

### 4. Add System Prompt Support
- Test that system prompts work:
  ```json
  [
    {"role": "system", "content": "You are a helpful RAG assistant"},
    {"role": "user", "content": "Hello"}
  ]
  ```
- Include a system prompt at the start of the conversation. The system prompt should be sent with every request.
- Verify the model follows system instructions
- Try different system prompts: "Be concise", "Explain like I'm 5", "Focus on technical accuracy"

### 5. Write Tests
- Create `api/tests/test_chat.py`
- Test successful request returns 200 and correct JSON structure
- Test invalid request (empty messages) returns 400 error
- Test response includes usage statistics (`prompt_tokens`, `completion_tokens`)
- Run tests: `make test`

## Submission

Submit to autograder:
- `examples/week2_chat.py` — script demonstrating multi-turn conversation
- `api/tests/test_chat.py` — test file with at least 3 test functions

The autograder will:
1. Run your tests and verify they pass
2. Check that conversation script maintains message history correctly
3. Test your endpoint with various inputs and verify OpenAI-compatible responses
4. Verify system prompts are properly passed through to Ollama
