import requests


API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/bd65ac2dd59b6c5a4ce5b1b8c67d0397/ai/run/"
headers = {"Authorization": "Bearer zR4YKSImLooU61Id87LMxjO92x2iuOwr_CbILeeI"}

def read_file(path):
    return open(path, 'r').read()

def get_response(prompt, instructions = ['common'], memory = "", model = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"):
    for instruction in instructions:
        instruction_content = read_file(f'Instructions/{instruction}.txt')
    inputs = [
        { "role": "system", "content": instruction_content},
        { "role": "user", "content": memory + '\n' + prompt }
    ]
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()['result']['response']
