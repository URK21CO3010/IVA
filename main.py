from cloudflare_text_generator import generate_text
from cloudflare_image_generator import generate_image
from cloudflare_image_describer import describe_image
import json


instructions = f'''

Instructions:

{open('IVA/instructions/common_instruction.txt', 'r').read()}

{open('IVA/instructions/primary_llm_instruction.txt', 'r').read()}

Here are the available models:
{open('IVA/models.txt', 'r').read()}

'''

prompt = "Explain what an LLM is in 2 sentences. Then, generate an image of an apple. Then, explain the image."

response = generate_text(prompt, instructions)

print(f'''
PROMPT : {prompt}

TASK DISTRIBUTION : 
{response}
      ''')


tasks = json.loads(response)

intermediate_responses = {}

for task_id in tasks.keys():
    print(tasks[task_id])

    prompt = tasks[task_id]['prompt']

    prompt_words = prompt.split()

    for index in range(len(prompt_words)):
        if prompt_words[index][0] == '<':
            prompt_words[index] = intermediate_responses[prompt_words[index]]
    
    prompt = ' '.join(prompt_words)
    
    if tasks[task_id]['type'] == 'txt2txt':
        intermediate_responses[f"<output{task_id}>"] = generate_text(prompt = prompt, instructions = open('IVA/instructions/common_instruction.txt', 'r').read(), model = tasks[task_id]['model'])
        print(intermediate_responses)

    elif tasks[task_id]['type'] == 'txt2img':
        intermediate_responses[f"<output{task_id}>"] = generate_image(prompt = prompt)
        print(intermediate_responses)
    
    elif tasks[task_id]['type'] == 'img2txt':
        prompt = tasks[task_id]['prompt']

        prompt_words = prompt.split()

        for index in range(len(prompt_words)):
            if prompt_words[index][0] == '<':
                prompt = intermediate_responses[prompt_words[index]]

        intermediate_responses[f"<output{task_id}>"] = describe_image(image_path = prompt)
        print(intermediate_responses)