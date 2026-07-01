def test_chat_completion_success(client):
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "llama3.1:8b",
            "messages": [
                {
                    "role": "user",
                    "content": "Hello!"
                }
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "choices" in data
    assert len(data["choices"]) == 1
    assert "message" in data["choices"][0]
    assert "content" in data["choices"][0]["message"]


def test_chat_completion_empty_messages(client):
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "llama3.1:8b",
            "messages": [],
        },
    )

    assert response.status_code in (400, 422)


def test_chat_completion_usage_statistics(client):
    response = client.post(
        "/v1/chat/completions",
        json={
            "model": "llama3.1:8b",
            "messages": [
                {
                    "role": "user",
                    "content": "Hello!"
                }
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "usage" in data
    assert "prompt_tokens" in data["usage"]
    assert "completion_tokens" in data["usage"]
