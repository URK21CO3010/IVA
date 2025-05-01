import requests
import base64


# Retrieve API credentials from environment variables
api_token = "qCG7bKtoI9jFDGcRmXGJKWWE8gkwF0aYU3VjbOL5"
account_id = "bd65ac2dd59b6c5a4ce5b1b8c67d0397"


url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/bytedance/stable-diffusion-xl-lightning"

# Headers
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

def generate_image(prompt):

    # Data payload
    data = {
        "prompt": prompt
    }

    # Making the POST request
    response = requests.post(url, headers=headers, json=data)

    # Handling the response
    if response.status_code == 200:
        try:
            with open("output.png", "wb") as img_file:
                img_file.write(response.content)
            return 'output.png'



        except ValueError as e:
            print(f"JSON decoding failed: {e}")
            return None
    else:
        print(f"Failed to generate image: {response.status_code} - {response.text}")
        return None
