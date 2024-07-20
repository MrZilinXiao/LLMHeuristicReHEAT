# self-consistency major voting evaluation script
from eval_kit.eval_0219 import route_to_eval_func
import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser(description='Run evaluation on the given input file')
    parser.add_argument('--input_file', type=str, default="Output/gpt-4_self_consistency_20240305110504.jsonl", help='The input file to evaluate')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    input_file = args.input_file
    with open(input_file, 'r') as f:
        test_cases = f.readlines()
        test_cases = [json.loads(line) for line in test_cases]
    total = len(test_cases)
    avail = 0
    correct = 0
    saved_cases = []
    
    query_type = 'self_consistency'
    print(f"Query type: {query_type}")
    
    for case_id, case in enumerate(test_cases):
        try:
            # for self consistency, we count it as correct if the majority of the 10 responses are correct
            responses = case[query_type]  # a list of 10 responses
            correct_count = 0
            for response in responses:
                result = route_to_eval_func(case_id)(response['choices'][0]['message']['content'])
                if result is None:   # eval function not available, skip all the rest
                    continue
                if result:
                    correct_count += 1
            result = correct_count >= (len(responses) / 2) if result is not None else None
        except KeyError as e:
            if 'error' in case[query_type]:
                result = None
                print(f"Error in case {case_id}: {case[query_type]['error']}")
            else:
                raise e
        if result is not None:
            avail += 1
            if result:
                correct += 1
        case['correct'] = result
        saved_cases.append(case)
    
    with open(input_file.replace('.jsonl', '_evaluated.jsonl').replace('Output', 'Eval_Results'), 'w') as f:
        for line in saved_cases:
            f.write(json.dumps(line) + '\n')
    
    print(f"Total: {total}, Available: {avail}, Correct: {correct}, Accuracy: {correct / avail}")