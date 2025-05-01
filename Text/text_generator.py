import requests
import json

# URL of LLM server
url = "http://127.0.0.1:1234"

def get_response(prompt: str) -> str:
    # Define the payload 
    data = {
        "prompt": prompt,
        "temperature": 0.7
    }

    # Send a POST request
    response = requests.post(f"{url}/v1/completions", json=data)

    # Check and parse the response
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"
