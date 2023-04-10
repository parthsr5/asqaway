import json
import random
import os
import re
from tqdm import tqdm
import pdb

import concurrent
from concurrent.futures import ThreadPoolExecutor, as_completed

MAX_THREADS = 32

def canonize(text, AA):
    for word, new_word in sorted(AA.items(), key=lambda x: len(x[0]), reverse=True):
        new_word = new_word.replace("\\u", "\\\\u")
        try:
            text = re.sub(f"\\b{word}\\b", new_word, text)
        except Exception as e:
            print("word:", word)
            print("new_word:", new_word)
            print("text:", text)
            print(e)
            print()
    return text

def preprocess_yesno(datum, AA):
    processed = []
    qid = datum['id']

    question = datum['body']#canonize(datum['body'], AA)

    answer = 1 if datum['exact_answer'] == 'yes' else 0
    context = ' '.join(snippet['text'] for snippet in datum['snippets'])
        
    new_entry = {'id': f'{qid}', 'sentence1': question, 'sentence2': context, 
                    'label': answer, 'type': datum['type']}
    processed.append(new_entry)
    return processed

def preprocess_dataset(dataset, AA):
    processed = []
    for datum in tqdm(dataset):
        if datum['type'] == 'yesno':
            processed.extend(preprocess_yesno(datum, AA))
    return processed

def generate_splits(dataset):
    data = dataset['data']
    s = set()
    for i in data:
        s.add(i['id'][:i['id'].find('_')])
    q_list = list(s)
    random.Random(11797).shuffle(q_list)
    split_index = int(len(q_list)*0.8)
    train_q = q_list[:split_index]
    test_q = q_list[split_index:]
    train_data = {"data": []}
    test_data = {"data": []}
    for i in data:
        q_id = i['id'][:i['id'].find('_')]
        if q_id in train_q:
            train_data['data'].append(i)
        elif q_id in test_q:
            test_data['data'].append(i)
    return train_data, test_data

if __name__ == "__main__":
    infile = "BioASQ-training11b/training11b.json"
    x = json.load(open(infile))

    # Load the acronyms/abbreviations dict
    if not os.path.exists("umls_data.json"):
        AA = {}
        # AA = load_AA(x['questions'])
        try:
            with open('umls_data.json', 'w') as f:
                print('Length of AA -', len(AA))
                json.dump(AA, f)
        except Exception as e: print(e)
    else:
        AA = json.load(open('umls_data.json'))

    # Process the file
    processed = preprocess_dataset(x['questions'], AA)
    out = {'data': processed}
    with open('train_file_yesno.json', 'w') as f:
        json.dump(out, f, indent=4)
    train_data, test_data = generate_splits(out)
    with open('train_file_80_yesno.json', 'w') as f:
        json.dump(train_data, f)
    with open('test_file_80_yesno.json', 'w') as f:
        json.dump(test_data, f)