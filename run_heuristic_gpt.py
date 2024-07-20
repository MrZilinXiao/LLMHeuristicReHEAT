import json
import openai
from openai import OpenAI
import backoff
from tqdm import tqdm
from itertools import product
from datetime import datetime
from common_prompt_kit import save_to_csv_jsonl, prompt_model
import os
import argparse

client = OpenAI(
  api_key = os.environ['OPENAI_API_KEY']
)

@backoff.on_exception(backoff.expo, (openai.RateLimitError, RuntimeError, openai.APIStatusError))
def submit_openai(model_name, prompt, system_msg=None, temp=0.0, debug=False):
    if system_msg is None:
        system_msg = "You are a helpful assistant."

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt}
        ], 
        temperature=temp   # API default: 1.0
    )
    if response.choices[0].index is None:
        raise RuntimeError("OpenAI response does not contain index.")
    # {'id': 'chatcmpl-WkGxaw9TFxXWLogbnJBC5C6Bv6',
    #  'choices': [{'finish_reason': 'stop',
    #    'index': 0,
    #    'logprobs': None,
    #    'message': {'content': 'The 2020 World Series was played at the Globe Life Field in Arlington, Texas. The decision to play the series at a neutral site was made as part of the adjustments to the Major League Baseball schedule due to the COVID-19 pandemic. The Globe Life Field was the new home stadium for the Texas Rangers and was chosen as the neutral site for the World Series.',
    #     'role': 'assistant',
    #     'function_call': None,
    #     'tool_calls': None}}],
    #  'created': 1706764809,
    #  'model': 'gpt-3.5-turbo',
    #  'object': 'chat.completion',
    #  'system_fingerprint': None,
    #  'usage': {'completion_tokens': 0, 'prompt_tokens': 0, 'total_tokens': 0}}
    if debug:
        print(prompt)
        print("-----------------------------------")
        print(response.choices[0].message.content)
    ret = {
        'submitted_prompt': prompt,
        **response.model_dump()
    }
    return ret


if __name__ == "__main__":
    start_time = datetime.now().strftime('%Y%m%d%H%M%S')
    with open('test_cases_0320.jsonl', 'r') as f:
        test_cases = f.readlines()
        test_cases = [json.loads(line) for line in test_cases]
        
    system_msg = "You are a helpful assistant who is good at choosing from multiple choices or ranking items."
    openai_endpoint = ['gpt-4-0613', 'gpt-3.5-turbo-0613', ]
    reasoning_method = ['cot', 'input_output', '1_shot', '2_shot', '3_shot', '4_shot', '5_shot', 'self_consistency']
    # reasoning_method = ['category_prompt', 'general_prompt']
    for endpoint, prompt_type in product(openai_endpoint, reasoning_method):
        print(f"Testing {endpoint} with {prompt_type}...")
        for test_case_id, test_case in enumerate(tqdm(test_cases)):
            test_case[prompt_type] = prompt_model(submit_openai, endpoint, prompt_type, 
                                                test_case['test_case'], test_case['type'], 
                                                system_msg, debug=True, test_case_id=test_case_id)
        save_to_csv_jsonl(test_cases, f"{endpoint}_{prompt_type}_{start_time}")
        # complete, remove prompt_type from test_cases
        for test_case in test_cases:
            test_case.pop(prompt_type)