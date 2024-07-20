import json
import os
# os.environ['REPLICATE_API_TOKEN'] = 'XXX'

import backoff
from tqdm import tqdm
from itertools import product
from datetime import datetime
from common_prompt_kit import save_to_csv_jsonl, prompt_model
import replicate
import httpx


# @backoff.on_exception(backoff.expo, (replicate.exceptions.ModelError, RuntimeError, httpx.ReadTimeout))
def submit_llama(model_name, prompt, system_msg=None, temp=0.0, debug=False):
    if system_msg is None:
        system_msg = "You are a helpful assistant."
    do_sample = temp > 0.0
    if not do_sample:
        temp = 0.01
    output = replicate.run(
        model_name,   # should only be `meta/llama-2-70b-chat`
        input={
            "debug": False,
            "top_p": 1,
            "prompt": prompt,
            "temperature": temp,
            "system_prompt": system_msg,
            "max_new_tokens": 1000,
            "min_new_tokens": -1,
            "prompt_template": "[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n{prompt} [/INST]",
            "do_sample": do_sample,
        },
    )
        
    response = ''.join(output)
    
    if debug:
        print(prompt)
        print("-----------------------------------")
        print(response)
    ret = {
        'submitted_prompt': prompt,
        'choices': [{'message': {'content': response}}]   # be compatible with OpenAI response
    }
    return ret


if __name__ == "__main__":
    start_time = datetime.now().strftime('%Y%m%d%H%M%S')
    with open('test_cases_0320.jsonl', 'r') as f:
        test_cases = f.readlines()
        test_cases = [json.loads(line) for line in test_cases]
        
    system_msg = "You are a helpful assistant who is good at choosing from multiple choices or ranking items."
    # reasoning_method = ['1_shot', 'input_output', 'cot', 'self_consistency']
    # reasoning_method = ['self_consistency']
    reasoning_method = ['input_output', '1_shot', '2_shot', '3_shot', '4_shot', '5_shot', 'self_consistency']

    for endpoint, prompt_type in product(['meta/llama-2-70b-chat'], reasoning_method):
        print(f"Testing {endpoint} with {prompt_type}...")
        for test_case_id, test_case in enumerate(tqdm(test_cases)):
            test_case[prompt_type] = prompt_model(submit_llama, endpoint, prompt_type, 
                                                test_case['test_case'], test_case['type'], 
                                                system_msg, debug=True, test_case_id=test_case_id)
        save_to_csv_jsonl(test_cases, f"{endpoint}_{prompt_type}_{start_time}")
        # complete, remove prompt_type from test_cases
        for test_case in test_cases:
            test_case.pop(prompt_type)