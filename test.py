import requests

s = input()
while s != '0':
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",
            "prompt": s,
            "stream": False
        }
    )

    print(response.json()['response'])
    s = input()