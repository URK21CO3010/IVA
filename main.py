from cloudflare_text_generator import generate_text
from cloudflare_image_generator import generate_image
from cloudflare_image_describer import describe_image
import json


instructions = f'''

Instructions:

{open('instructions/common_instruction.txt', 'r').read()}

{open('instructions/primary_llm_instruction.txt', 'r').read()}

Here are the available models:
{open('models.txt', 'r').read()}

'''

prompt = "Generate an image of a sports car, and write a short instagram caption for the car."

response = generate_text(prompt, instructions)

print(f'''
PROMPT : {prompt}

TASK DISTRIBUTION : 
{response}
      ''')


# tasks = json.loads(response)
tasks = response

intermediate_responses = {}

for task_id in tasks.keys():
    print(tasks[task_id], '\n')

    prompt = tasks[task_id]['prompt']

    prompt_words = prompt.split()

    for index in range(len(prompt_words)):
        if prompt_words[index][0] == '<':
            prompt_words[index] = intermediate_responses[prompt_words[index]]
    
    prompt = ' '.join(prompt_words)
    
    if tasks[task_id]['type'] == 'txt2txt':
        intermediate_responses[f"<output{task_id}>"] = generate_text(prompt = prompt, instructions = open('instructions/common_instruction.txt', 'r').read(), model = tasks[task_id]['model'])
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
        print(intermediate_responses, '\n')
