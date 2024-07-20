import os
import pandas
import json
from typing import List, Dict

MULTI_CHOICE_PROMPT = "For multiple-choice questions, choose the one that you think is best, even if you think more than one option will work, choose the one that you think is best. The answer should be accompanied by the number I gave for each option. For example, when the options are [1] choice1; [2] choice2; [3] choice3, if [1] choice1 is the correct answer, the answer format is [1] choice1. "
RANK_PROPMT = "For ranking questions, provide a ranking, and make distinctions even if you think multiple options may have the same position in the ranking. When displaying the answer, you need to provide the number assigned to each option in the original question. For example, when the options are [1] choice1; [2] choice2; [3] choice3. If you think [2] ranks before [1], and [1] ranks before [3], the answer format is [2] choice2 > [1] choice1 > [3] choice3. "

CATEGORY_PROMPT = {
    "Base Rate Fallacy": "Please answer this question based on your statistical probability knowledge, the conditional probability of an event needs to take into account the overall base rate (or prior probability) of that event. ", 
    "Conjunction Fallacy": "Please answer this question based on your statistical probability knowledge, the probability of two specific conditions occurring simultaneously is not higher than that of one specific condition. ", 
    "Disjunction Fallacy": "Please answer this question based on your statistical probability knowledge, the probability of a subset of events cannot be higher than the probability of the entire event. ",
    "Insensitivity to Sample Size": "Please answer this question based on your statistical probability knowledge, changes in small samples tend to have a more pronounced effect on the overall statistics than changes in large samples. ", 
    "Misconceptions of Chance": "Please answer this question based on your statistical probability knowledge, the probabilities of each independent event are not related to each other.", 
    "Regression Fallacy": "Please answer this question based on your statistical probability knowledge, a natural relationship between two variables does not imply causation.", 
    "General": "Please answer this question based on your statistical probability knowledge."
}

# 5-shots
FEW_SHOT_TEMPLATE = {
    "Base Rate Fallacy": [
        {
            "query": """Suppose we know that the number of graduate students is sorted from high to low as follows: [2] Social science and social work > [4] Humanities and education > [7] Library science > [5] Law > [9] Medicine > [6] Business administration > [1] Physical and life sciences > [3] Computer science > [8] Engineering. The number of people at the top and bottom of the ranking will be quite different.
Tom W. is of high intelligence, although lacking in true creativity. He has a need for order and clarity, and for neat and tidy systems in which every detail finds its appropriate place. His writing is rather dull and mechanical, occasionally enlivened by somewhat corny puns and by flashes of imagination of the sci-fi type. He has a strong drive for competence. He seems to feel little sympathy for other people and does not enjoy interacting with others. Self-centered, he nonetheless has a deep moral sense. The preceding personality sketch of Tom W. was written during Tom's senior year in high school by a psychologist, on the basis of projective tests. Tom W. is currently a graduate student.
Please rank the following nine fields of graduate specialization in order of the likelihood that Tom W. is now a graduate student in each of these fields. The nine fields given were [1] Physical and life sciences, [2] Social science and social work, [3] Computer science, [4] humanities and education, [5] law, [6] Business administration, [7] Library science, [8] Engineering, and [9] Medicine. """, 
            "answer": "[2] Social science and social work > [7] Library science > [5] Law > [9] Medicine > [4] Humanities and education > [6] Business administration > [1] Physical and life sciences > [3] Computer science > [8] Engineering", 
            "question_id": 0
        }, {
        "query": "A doctor performs a test that is 99% accurate, and you test positive for the disease. However, the incidence of the disease is 1/10,000. How do you think you will get the disease? Choose between the following two probabilities: [1] greater than 50 percent, [2] less than 50 percent.", 
        "answer": "[2] less than 50 percent.", 
        "question_id": 1   # excel line number minus 2
        }, {
        "query": """A cab was involved in a hit-and-run accident at night. Two cab companies, the Green and the Blue, operate in the city. 85% of the cabs in the city are Green and 15% are Blue. A witness identified the cab as Blue. The court tested the reliability of the witness under the same circumstances that existed on the night of the accident and concluded that the witness correctly identified each one of the two colors 80% of the time and failed 20% of the time. What is the probability that the cab involved in the accident was Blue rather than Green? Knowing that this witness identified it as Blue, choose between the following two probabilities: [1] greater than 50 percent, [2] less than 50 percent.""", 
        "answer": "[2] less than 50 percent.", 
        "question_id": 3, 
        }, 
        {
        "query": "In a city, the rate of traffic accidents is 990 accidents per 1,000 vehicles. Now, there is a new traffic safety prediction system that predicts accidents with a 95% false alarm rate (i.e., the probability of incorrectly predicting that an accident will occur), but also has an accuracy rate of 5%. If this system predicts that a particular vehicle will have an accident, what is the probability that this vehicle will actually have an accident? Choose between the following two probabilities: [1] greater than 50 percent, [2] less than 50 percent.", 
        "answer": "[1] greater than 50 percent.", 
        "question_id": 6, 
        }, {
        "query": "Suppose that in a university, students are divided into two main types of majors: science majors and humanities majors. Science majors make up the vast majority of the overall student body. Now, there is a belief that science majors are usually more detail-oriented, while humanities majors are better at critical thinking. If we randomly encountered a student who was good at critical thinking, would that student be more likely to be from a science major or a humanities major? [1] science major, [2] humanities major.", 
        "answer": "[1] science major.", 
        "question_id": 9,
        }
    ], 
    "Conjunction Fallacy": [
        {
            "query": "Bill is 34 years old. He is intelligent, but unimaginative, compulsive, and generally lifeless. In school, he was strong in mathematics but weak in social studies and humanities. We have eight statements below: [1] Bill is a physician who plays poker as a hobby. [2] Bill is an architect. [3] Bill is an accountant. [4] Bill plays jazz as a hobby. [5] Bill surfs as a hobby. [6] Bill is a reporter. [7] Bill is an accountant who plays jazz as a hobby. [8] Bill climbs mountains for a hobby. Ranked the eight statements associated with each description by the degree to which Bill resembles the typical member of that class.",
            "answer": "[1] Bill is a physician who plays poker as a hobby. > [6] Bill is a reporter. > [3] Bill is an accountant. > [5] Bill surfs as a hobby.> [4] Bill plays jazz for a hobby. > [2] Bill is an architect > [7] Bill is an accountant who plays jazz for a hobby. > [8] Bill climbs mountains for a hobby.", 
            "question_id": 47,
        }, 
        {
            "query": "Linda is 31 years old, single, outspoken, and very bright. She majored in philosophy. As a student, she was deeply concerned with issues of discrimination and social justice, and also participated in anti-nuclear demonstrations. We have eight statements below. [1] Linda is a teacher in elementary school. [2] Linda works in a bookstore and takes Yoga classes. [3] Linda is active in the feminist movement. [4] Linda is a psychiatric social worker. [5] Linda is a member of the League of Women Voters. [6] Linda is a bank teller. [7] Linda is an insurance salesperson. [8] Linda is a bank teller and is active in the feminist movement. Ranked the eight statements associated with each description by the degree to which Linda resembles the typical member of that class. ",
            "answer": "[3] Linda is active in the feminist movement. > [1] Linda is a teacher in elementary school. > [4] Linda is a psychiatric social worker. > [5] Linda is a member of the League. > [6] Linda is a bank teller. > [8] Linda is a bank teller and is active in the feminist movement. > [2] Linda works in a bookstore and takes Yoga classes. > [7] Linda is an insurance salesperson.",
            "question_id": 50,
        }, 
        {
            "query": "Jack is a 28-year-old male. He is intelligent, creative, and likes to think independently, but he usually doesn't care much about the details. In school, he excels in science and math but is relatively weak in literature and the arts. Based on the following descriptions, rank the likelihood, from most likely to least likely, that Jack will pursue the following careers or have the following hobbies: [1] Jack is a software engineer. [2] Jack is an artist. [3] Jack is a mechanical engineer. [4] Jack plays video games in his spare time. [5] Jack enjoys hiking as a hobby. [6] Jack is a writer. [7] Jack is a mechanical engineer and plays video games in his spare time. [8] Jack enjoys painting as a hobby. ", 
            "answer": "[3] Jack is a mechanical engineer. > [4] Jack plays video games in his spare time. > [7] Jack is a mechanical engineer and plays video games in his spare time. > [1] Jack is a software engineer. > [2] Jack is an artist. > [6] Jack is a writer. > [8] Jack enjoys painting as a hobby. > [5] Jack enjoys hiking as a hobby.",
            "question_id": 62
        }, 
        {
            "query": "Sandra is a 31 year old female. She is outgoing, sociable, and curious about new things. She majored in psychology and minored in statistics in college. She enjoys outdoor activities and reading science fiction. Based on the following descriptions, rank the likelihood, from most likely to least likely, that Sandra would have the following occupations or have the following hobbies: [1] Sandra is a psychologist. [2] Sandra is a data analyst. [3] Sandra is a teacher. [4] Sandra does photography in her spare time. [5] Sandra enjoys cycling as a hobby. [6] Sandra is a writer. [7] Sandra is a teacher and does photography in her spare time. [8] Sandra enjoys cooking as a hobby. ", 
            "answer": "[1] Sandra is a psychologist. > [2] Sandra is a data analyst. > [3] Sandra is a teacher. > [4] Sandra does photography in her spare time. > [6] Sandra is a writer. > [7] Sandra is a teacher and does photography in her spare time. > [5] Sandra enjoys cycling as a hobby. > [8] Sandra enjoys cooking as a hobby.",
            "question_id": 68
        }, 
        {
            "query": "Tom is a 40 year old male. He is conscientious, detail oriented, and has a strong aptitude for numbers and logical analysis. In college, he majored in finance and was not interested in courses in history or political science. In his spare time he enjoys outdoor activities and reading history books. Based on the following descriptions, rank the likelihood, from most likely to least likely, that Tom would pursue the following careers or have the following hobbies: [1] Tom is an accountant. [2] Tom is a historian. [3] Tom is a banker. [4] Tom plays board games in his spare time. [5] Tom enjoys hiking as a hobby. [6] Tom is a software developer. [7] Tom is a banker and plays board games in his spare time. [8] Tom enjoys gardening as a hobby. ",
            "answer": "[1] Tom is an accountant. > [4] Tom plays board games in his spare time. > [3] Tom is a banker. > [7] Tom is a banker and plays board games in his spare time. > [6] Tom is a software developer. > [2] Tom is a historian. > [5] Tom enjoys hiking as a hobby. > [8] Tom enjoys gardening as a hobby.",
            "question_id": 71
        }
    ], 
    "Disjunction Fallacy": [
        {
            "query": "It is quite possible for something to be included in more than one option listed. For example, suppose the list is of foodstuffs, and one option is “frozen foods,” while another is “desserts”. In this case, do not interpret “frozen foods” as “frozen foods excluding deserts,” nor interpret “desserts” as “desserts which are not frozen”—“ice cream” qualifies as both “frozen food” and “dessert.” Danielle is sensitive and introspective. In high school, she wrote poetry secretly. Did her military service as a teacher. Though beautiful, she has little social life, since she prefers to spend her time reading quietly at home rather than partying. What does she study, rank the answer below from most possible to least. [1] Literature, [2] Humanities, [3] Physics, [4] Natural science. ", 
            "answer": "[2] Humanities > [1] Literature > [4] Natural science > [3] Physics",
            "question_id": 93
        }, 
        {
            "query": "It is quite possible for something to be included in more than one option listed. For example, suppose the list is of foodstuffs, and one option is “frozen foods,” while another is “desserts”. In this case, do not interpret “frozen foods” as “frozen foods excluding deserts,” nor interpret “desserts” as “desserts which are not frozen”—“ice cream” qualifies as both “frozen food” and “dessert.” Gidi is 23 years old, he wears the latest fashions, and drives a new sports car. He spends time in discotheques and expensive pubs, and is a social butterfly. He is occasionally mentioned in the gossip columns. Where does he live, choose only one answer below. [1] Tel Aviv, [2] Dan Metropolitan Area, [3] Hadar ha’Camel, [4] The North of Israel.", 
            "answer": "[2] Dan Metropolitan Area.",
            "question_id": 96
        }, 
        {
            "query": "It is quite possible for something to be included in more than one option listed. For example, suppose the list is of foodstuffs, and one option is “frozen foods,” while another is “desserts”. In this case, do not interpret “frozen foods” as “frozen foods excluding deserts,” nor interpret “desserts” as “desserts which are not frozen”—“ice cream” qualifies as both “frozen food” and “dessert.” Eldar is 23 years old, he dresses modestly and wears sandals year-round, even in winter. He is tanned from outdoor work. He spends his leisure time hiking in the countryside. Where does he live, rank the answer below from most possible to least. [1] Kibbutz Rosh Ha’Nikra, [2] The North of Israel, [3] North Tel Aviv, [4] Dan Metropolitan Area.", 
            "answer": "[2] The North of Israel > [1] Kibbutz Rosh Ha’Nikra > [4] Dan Metropolitan Area > [3] North Tel Aviv",
            "question_id": 99
        }, 
        {
            "query": 'It is quite possible for something to be included in more than one option listed. For example, suppose the list is of foodstuffs, and one option is “frozen foods,” while another is “desserts”. In this case, do not interpret “frozen foods” as “frozen foods excluding deserts,” nor interpret “desserts” as “desserts which are not frozen”—“ice cream” qualifies as both “frozen food” and “dessert.” Eli, 39 years old, a professor of Greek Philosophy and Ethics, he holds socialist views. Following the Lebanon War he became politically active, while remaining a "bleeding heart." Where is he active, choose only one answer below. [1] Peace Now, [2] A peace movement, [3] Gush Emunim, [4] A national movement.',
            "answer": "[2] A peace movement.", 
            "question_id": 104, 
        }, 
        {
            "query": "It is quite possible for something to be included in more than one option listed. For example, suppose the list is of foodstuffs, and one option is “frozen foods,” while another is “desserts”. In this case, do not interpret “frozen foods” as “frozen foods excluding deserts,” nor interpret “desserts” as “desserts which are not frozen”—“ice cream” qualifies as both “frozen food” and “dessert.” Yossi was recently discharged from service in Intelligence. Outstanding high school student, who once won a national math competition. Pedantic and careful, with a good head for numbers. A computer nut. Shy and reserved, a loner. What does he study, choose only one answer below. [1] Statistics, [2] Social science, [3] Hebrew language, [4] Humanities.", 
            "answer": "[2] Social science.", 
            "question_id": 112, 
        }
    ], 
    "Insensitivity to Sample Size": [
        {
            "query": "Approximately 45 babies are born in the large hospital while 15 babies are born in the small hospital. Half (50%) of all babies born in general are boys. However, the percentage changes from 1 day to another. For a 1-year period, each hospital recorded the days on which >60% of the babies born were boys. The question posed is: Which hospital do you think recorded more such days? Just choose the most probable answer below: [1] The larger hospital. [2] The smaller hospital. [3] About the same (that is, within 5% of each other). ", 
            "answer": "[2] The smaller hospital.",
            "question_id": 140
        }, 
        {
            "query": "Suppose there are two classes, a large class, and a small class. The large class has 30 students and the small class has 8 students. Each student is randomly given a card with either red (50%) or blue (50%) color. The question is which class is likely to have more days of red card records than 60% of the class over the course of a year. Just choose the most probable answer below: [1] Large class. [2] Small class. [3] Both classes were about the same (i.e. the difference between the two was within 5%).", 
            "answer": "[2] Small class.", 
            "question_id": 142, 
        }, 
        {
            "query": "Suppose you are investigating weather changes in two cities. One is a large city with millions of people; the other is a small town with only a few thousand people. Over the course of a year, you record how many days in each city the temperature exceeds 30°C (86°F). The question is, which location is more likely to record more days over 30°C during the year? Just choose the most probable answer below: [1] Large city. [2] A small town. [3] Both are about the same (i.e., the difference between the two is within 5%). [4] Depends.", 
            "answer": "[4] Depends.", 
            "question_id": 144,
        }, 
        {
            "query": "Imagine there are two banks of different sizes. One is a large international bank and the other is a small local bank. Each bank records the number of transaction anomaly reports per day over the course of a year. The large bank processes about 10000 transactions per day, while the small bank processes about 1000 transactions per day. The exception reports rate for both banks is 5%. The question is: Which bank was more likely to record a greater percentage of transaction exception reports over 10% on more days during the year? Just choose the most probable answer below: [1] Large international banks. [2] Small local banks. [3] Both banks were about the same (i.e., within 5% of each other).", 
            "answer": "[2] Small local banks.", 
            "question_id": 149,
        }, 
        {
            "query": "Consider two florists of different sizes for a customer feedback survey. One is a large florist that serves hundreds of customers per day; the other is a small corner florist that serves about 30 customers per day. Each florist recorded daily customer satisfaction ratings over a period of one year. The large florist was known for its variety and quick service, while the small florist was known for its personalized service and unique flower arrangements. The question is: Which florist was more likely to record customer satisfaction ratings above 95% on more days during the year? Just choose the most probable answer below: [1] Large florist. [2] Small corner florist. [3] Both florists were about the same (i.e., the difference between the two was within 5%). [4] Depends.",
            "answer": "[4] Depends.", 
            "question_id": 168,
        }
    ], 
    "Misconceptions of Chance": None, 
    "Regression Fallacy": None 
}

ONE_SHOT_TEMPLATE = {
    "Base Rate Fallacy": {
        "query": "A doctor performs a test that is 99% accurate, and you test positive for the disease. However, the incidence of the disease is 1/10,000. How do you think you will get the disease? Choose between the following two probabilities: [1] greater than 50 percent, [2] less than 50 percent.", 
        "answer": "[2] less than 50 percent.", 
        "question_id": 1   # excel line number minus 2
    }, 
    # one-shot for ranking question is problematic, as the answer itself is incomplete;
    "Conjunction Fallacy": {
        "query": "Bill is 34 years old. He is intelligent, but unimaginative, compulsive, and generally lifeless. In school, he was strong in mathematics but weak in social studies and humanities. We have eight statements below: [1] Bill is a physician who plays poker as a hobby. [2] Bill is an architect. [3] Bill is an accountant. [4] Bill plays jazz as a hobby. [5] Bill surfs as a hobby. [6] Bill is a reporter. [7] Bill is an accountant who plays jazz as a hobby. [8] Bill climbs mountains for a hobby. Ranked the eight statements associated with each description by the degree to which Bill resembles the typical member of that class. The answer should accompanied by the numbers I give for each option.", 
        "answer": "[1] Bill is a physician who plays poker as a hobby. > [6] Bill is a reporter. > [3] Bill is an accountant. > [5] Bill surfs as a hobby.> [4] Bill plays jazz for a hobby. > [2] Bill is an architect > [7] Bill is an accountant who plays jazz for a hobby. > [8] Bill climbs mountains for a hobby.", 
        "question_id": 47, 
    }, 
    "Disjunction Fallacy": {
        "query": "It is quite possible for something to be included in more than one option listed. For example, suppose the list is of foodstuffs, and one option is “frozen foods,” while another is “desserts”. In this case, do not interpret “frozen foods” as “frozen foods excluding deserts,” nor interpret “desserts” as “desserts which are not frozen”—“ice cream” qualifies as both “frozen food” and “dessert.” Danielle sensitive and introspective. In high school, she wrote poetry secretly. Did her military service as a teacher. Though beautiful, she has little social life, since she prefers to spend her time reading quietly at home rather than partying. What does she study, rank the answer below from most possible to least. [1] Literature, [2] Humanities, [3] Physics, [4] Natural science.",
        "answer": "[2] Humanities > [1] Literature > [4] Natural science > [3] Physics", 
        "question_id": 93
    }, 
    "Insensitivity to Sample Size": {
        "query": "Approximately 45 babies are born in the large hospital while 15 babies are born in the small hospital. Half (50%) of all babies born in general are boys. However, the percentage changes from 1 day to another. For a 1-year period, each hospital recorded the days on which >60% of the babies born were boys. The question posed is: Which hospital do you think recorded more such days? Just choose the most probable answer below: [1] The larger hospital. [2] The smaller hospital. [3] About the same (that is, within 5% of each other). ", 
        "answer": "[2] The smaller hospital.",
        "question_id": 140
    }, 
    # question_type with None -> no one-shot for this type
    "Misconceptions of Chance": None, 
    "Regression Fallacy": None 
}

# save one jsonl for evaluation; save one csv for visualization
csv_headers = ['test_case', 'type', 'ground_truth', 'input_output', 'cot', 'cot_self_consistency', 'tree_of_thoughts']

def save_to_csv_jsonl(output_list, filename):
    filename = filename.replace('/', '_')
    csv_filename = os.path.join('Output', filename + '.csv')
    jsonl_filename = os.path.join('Output', filename + '.jsonl')
    with open(jsonl_filename, 'w') as f:
        for line in output_list:
            f.write(json.dumps(line) + '\n')
    df = pandas.DataFrame(output_list)
    # skip headers that are not in the output
    real_headers = [header for header in csv_headers if header in df.columns]
    df.to_csv(csv_filename, index=False, columns=real_headers)
    
MULTI_AGENT_DEBATE_GLOBAL_CONFIG = None

# now do all tests in zero-shot manner; when needed, we can add 1-shot for each type of `Special` (Ranking, Choose 1, etc.)
def prompt_model(submit_func: callable, model_name, prompt_type, query, query_type=None, system_msg=None, temp=0.0, 
                 debug=False, test_case_id=None):
    """
    submit_func: callable, the function to submit the prompt to the model
    with the signature: [model_name, prompt, system_msg, temp, debug]
    """
    global MULTI_AGENT_DEBATE_GLOBAL_CONFIG
    # ignore external system_msg, use instruction_text as system_msg
    instruction_text = MULTI_CHOICE_PROMPT if not 'rank' in query.lower() else RANK_PROPMT
    if 'gpt' in model_name and prompt_type == 'cot':   # do not disturb gpt cot system_msg
        system_msg = system_msg
    else:
        system_msg = instruction_text
    
    if prompt_type == 'multiagent_debate':
        from Multi_Agents_Debate.interactive import Debate
        if MULTI_AGENT_DEBATE_GLOBAL_CONFIG is None:
            with open("Multi_Agents_Debate/code/utils/config4all.json", 'r') as f:
                MULTI_AGENT_DEBATE_GLOBAL_CONFIG = json.load(f)
        MULTI_AGENT_DEBATE_GLOBAL_CONFIG.pop('debate_topic', None)
        config = {
            'debate_topic': query, 
            **MULTI_AGENT_DEBATE_GLOBAL_CONFIG
        }
        print(f"Debate config: {config}")
        debate = Debate(num_players=3, model_name=model_name, openai_api_key=os.getenv("OPENAI_API_KEY"), config=config, temperature=0, sleep_time=0)
        debate_return = debate.run(return_debate_answer=True)
        ret = {
            'submitted_prompt': query,
            'choices': [{'message': {'content': debate_return.pop('debate_answer')}}],    # be compatible with OpenAI response
            'debate_metadata': debate_return
        }
        return ret
                
    elif prompt_type == 'category_prompt':
        query += "\n" + CATEGORY_PROMPT[query_type] + "\n"
        return submit_func(model_name, query, system_msg, temp=temp, debug=debug)
    
    elif prompt_type == 'general_prompt':  # general prompt
        query += "\n" + CATEGORY_PROMPT["General"] + "\n"
        return submit_func(model_name, query, system_msg, temp=temp, debug=debug)
    
    elif prompt_type == 'input_output':
        # query += f" {instruction_text}\n"
        return submit_func(model_name, query, system_msg, temp=temp, debug=debug)
    elif prompt_type == 'self_consistency':
        # query += " " + f" {instruction_text}\n"
        cot_responses = []
        for _ in range(5):
            cot_responses.append(submit_func(model_name, query, system_msg, temp=0.7, debug=debug))
        return cot_responses
    elif prompt_type.startswith('cot'):
        query += " " + "Let's think step by step, but don't give the answer directly."
        if prompt_type == 'cot':
            reasoning_response = submit_func(model_name, query, system_msg, temp=temp, debug=debug)
            if not 'error' in reasoning_response:
                query += reasoning_response['choices'][0]['message']['content']
                
                if 'gpt' in model_name:
                    query += instruction_text
                    
                query += " Therefore, the answer is "
                answer_response = submit_func(model_name, query, system_msg, temp=temp, debug=debug)
                return {
                    "reasoning": reasoning_response, 
                    "answer": answer_response, 
                    "choices": [{'message': {'content': answer_response['choices'][0]['message']['content'] if 'choices' in answer_response else answer_response['error']}}]
                }
            else:
                return {
                    "reasoning": reasoning_response, 
                    "answer": {"error": "No reasoning response."}, 
                    "choices": [{'message': {'content': reasoning_response['error']}}]
                }
                
    elif prompt_type.endswith('_shot'):
        system_msg = "You are a helpful assistant who answer questions with the format of the given demonstration."
        num_of_shots = int(prompt_type.split('_')[0])  # 1 ~ 5
        if FEW_SHOT_TEMPLATE[query_type] is None: 
            return {"error": "No one-shot demonstration for this type."}
        assert len(FEW_SHOT_TEMPLATE[query_type]) >= num_of_shots, "Not enough few-shot demonstrations for this type."
        few_shot_list: List[Dict[str, str]] = FEW_SHOT_TEMPLATE[query_type][:num_of_shots]
        few_shot_question_ids = [case['question_id'] for case in few_shot_list]
        if test_case_id is not None and test_case_id in few_shot_question_ids:
            return {"error": "This question is in the few-shot demonstration itself."}
        few_shot_text = "\n\n".join([f"{case['query']}\nAnswer: {case['answer']}\n" for case in few_shot_list])
        few_shot_text += f"Given the demonstration, answer the following question with the similar format. {instruction_text}\n{query}\nAnswer: "
        return submit_func(model_name, few_shot_text, system_msg, temp=temp, debug=debug)
        
    elif prompt_type == 'one_shot':
        raise NotImplementedError("Refer to k_shot.")
        
    elif prompt_type == 'tree_of_thoughts':
        raise NotImplementedError("Tree of Thoughts is not implemented yet.")