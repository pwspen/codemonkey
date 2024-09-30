# import anthropic
# import os

# client = anthropic.Anthropic()

# message = client.messages.create(
#     model="claude-3-haiku-20240307",
#     max_tokens=1000,
#     messages=[
#         {"role": "user", "content": "A sonnet about the ocean."},
#     ]
# )
# print(message.content)

#def request(self, content, model='llama3.1:8b'):
#        return ollama.chat(model=model, messages=[{'role': 'user', 'content': content}])['message']['content']

import requests
import json
import os
import time
import ollama

OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]

def openrouter_request(prompt, type='code'):
    while True:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            },
            data=json.dumps({
                "model": "meta-llama/llama-3.2-11b-vision-instruct:free", # Optional
                "messages": [
                {
                    "role": "user",
                    "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    #   {
                    #     "type": "image_url",
                    #     "image_url": {
                    #       "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                    #     }
                    #   }
                    ]
                }
                ]
                
            })
        )
        response = response.json()
        if "choices" in response:
            response_text = response["choices"][0]["message"]["content"]
            if type == 'code':
                return response_text
            elif type == 'json':
                return extract_between_braces(response_text)
        else: # Probably API rate limiting
            #debug(response)
            print("API rate limited..")
            time.sleep(2)
            continue

def debug(*args):
    for i, arg in enumerate(args, 1):
        print(arg)

def extract_between_braces(s):
    start = s.find('{')
    end = s.rfind('}')
    if start != -1 and end != -1 and start < end:
        return s[start:end+1]
    return None

def flatten_nested_dict(input_dict): # Puts all classname keys at first level, with no duplicates 
    result = {}
    
    def recursive_process(d):
        if not isinstance(d, dict):
            return d
        
        new_dict = {}
        for key, value in d.items():
            if not (key == "desc" or key == "funcs"):
                if isinstance(value, dict):
                    result[key] = recursive_process(value)
                else:
                    result[key] = value
            else:
                new_dict[key] = value
        return new_dict

    result.update(recursive_process(input_dict))
    return result

def remove_desc_funcs(input_dict): # Removes "desc" and "func" key/values from flattened dict
    result = {}
    for key, value in input_dict.items():
        if isinstance(value, dict):
            result[key] = {k: v for k, v in value.items() if k not in ["desc", "funcs"]}
        else:
            result[key] = value
    return result

# Test the function
# test_dict = {"name1": {"name2": {"name3": "value1"}, "desc": {}}, "name4": {"desc": "value2", "funcs": {"f1": 6, "f2": 7}}}
# flattened = process_nested_dict(test_dict)
# print(flattened)
# removed = remove_desc_funcs(flattened)
# print(removed)
