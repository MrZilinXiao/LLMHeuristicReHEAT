import google.generativeai as palm

palm.configure(api_key="XXX")

import json
import backoff
from tqdm import tqdm
from itertools import product
from datetime import datetime
from common_prompt_kit import save_to_csv_jsonl, prompt_model


@backoff.on_exception(backoff.expo, RuntimeError)
def submit_palm(model_name, prompt, system_msg=None, temp=0.0, debug=False):
    if system_msg is None:
        system_msg = "You are a helpful assistant."

    response=palm.chat(
            model=model_name,  # should be `models/chat-bison-001`
            messages=[prompt], 
            temperature=temp, 
            context=system_msg
    )
    try:
        if debug:
            print(prompt)
            print("-----------------------------------")
            print(response.candidates[0]['content'])
    
        ret = {
            'submitted_prompt': prompt,
            'choices': [{'message': {'content': response.candidates[0]['content']}}]
        }
    except IndexError:
        print(f"Error response: {response}")
        return {"error": "No response from the model due to safety filter."}
    
    return ret


if __name__ == "__main__":
    start_time = datetime.now().strftime('%Y%m%d%H%M%S')
    with open('test_cases_0320.jsonl', 'r') as f:
        test_cases = f.readlines()
        test_cases = [json.loads(line) for line in test_cases]
        
    system_msg = "You are a helpful assistant who is good at choosing from multiple choices or ranking items."
    reasoning_method = ['category_prompt', 'general_prompt']

    for endpoint, prompt_type in product(['models/chat-bison-001'], reasoning_method):
        print(f"Testing {endpoint} with {prompt_type}...")
        for test_case_id, test_case in enumerate(tqdm(test_cases)):
            test_case[prompt_type] = prompt_model(submit_palm, endpoint, prompt_type, 
                                                test_case['test_case'], test_case['type'], 
                                                system_msg, debug=True, test_case_id=test_case_id)
        save_to_csv_jsonl(test_cases, f"{endpoint}_{prompt_type}_{start_time}")
        # complete, remove prompt_type from test_cases
        for test_case in test_cases:
            test_case.pop(prompt_type)