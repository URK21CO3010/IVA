import requests
import base64
import mimetypes

api_token = "qCG7bKtoI9jFDGcRmXGJKWWE8gkwF0aYU3VjbOL5"
account_id = "bd65ac2dd59b6c5a4ce5b1b8c67d0397"

# API Endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/llava-hf/llava-1.5-7b-hf"

headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

def describe_image(image_path):
    with open(image_path, "rb") as f:
        image_bytes = list(f.read())  # Convert to list of integers

    payload = {
        "image": image_bytes,  # raw byte array (list of integers)
        "prompt": "Generate a caption for this image",
        "max_tokens": 512
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json().get("result")['description']
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None