import requests


API_BASE_URL = "https://api.cloudflare.com/client/v4/accounts/bd65ac2dd59b6c5a4ce5b1b8c67d0397/ai/run/"
headers = {"Authorization": "Bearer zR4YKSImLooU61Id87LMxjO92x2iuOwr_CbILeeI"}

def read_file(path):
    return open(path, 'r').read()

def get_response(prompt, instructions = ['common'], memory = "", model = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"):
    all_instructions = ""
    for instruction in instructions:
        instruction_content = read_file(f'Instructions/{instruction}.txt')
        all_instructions += instruction_content + '\n'

    final_instruction = f"""
Instructions:
{all_instructions}

    """

    if len(memory) > 0:
        final_instruction += f"""
Conversation History:
{memory}

        """

    inputs = [
        { "role": "system", "content": final_instruction},
        { "role": "user", "content": prompt }
    ]
    input = { "messages": inputs }
    response = requests.post(f"{API_BASE_URL}{model}", headers=headers, json=input)
    return response.json()['result']['response']