import json
import sys
import random
import os
import re
import time

# from skr_web_api import Submission
class Submission():
    def __init__(self, a, b):
        pass

email = ""#os.environ['EMAIL']
apikey = ""#os.environ['API_KEY']
inst = Submission(email, apikey)


def get_AA(text):
    inst.init_mm_interactive(text)
    response = inst.submit()
    mappings = {}
    if response.status_code == 200:
        content = response.content.decode().split("\n")
        for line in content[1:]:
            m = line.split("|")
            if len(m) > 1 and m[1] == "AA":
                offset, length = tuple(int(x) for x in m[8].split(":"))
                word = text[offset: offset + length]
                if word not in mappings:
                    mappings[word] = m[3]
    else:
        raise NotImplementedError
    
    return mappings

def load_AA_list(datum):
    AA = {}
    AA.update(get_AA(datum['body']))
    for answer in datum['exact_answer']:
        AA.update(get_AA(answer[0]))
    for snippet in datum['snippets']:
        AA.update(get_AA(snippet))
    return AA

def load_AA_factoid(datum):
    AA = {}
    AA.update(get_AA(datum['body']))
    AA.update(get_AA(datum['exact_answer'][0]))
    for snippet in datum['snippets']:
        AA.update(get_AA(snippet))
    return AA

def load_AA(dataset):
    AA = {}
    for datum in dataset:
        if datum['type'] == 'list':
            AA.update(load_AA_list(datum))
        elif datum['type'] == 'factoid':
            AA.update(load_AA_factoid(datum))
    return AA


def canonize(text, AA):
    for word, new_word in AA.items():
        text = re.sub(rf"\b{word}\b", new_word, text)
    return text

def preprocess_list(datum, AA):
    processed = []
    i = 1
    qid = datum['id']

    question = canonize(datum['body'], AA)

    answers = [canonize(a[0], AA) for a in datum['exact_answer']]
    
    for snippet in datum['snippets']:
        snippet = canonize(snippet['text'], AA)
        for answer in answers:
            ind = snippet.find(answer)
            if ind > -1:
                new_entry = {'id': f'{qid}_{i:04}', 'question': question,
                             'answers': {'text': [answer], 'answer_start': [ind]},
                             'type': datum['type'], 'context': snippet}
                processed.append(new_entry)
                i += 1
    return processed

def preprocess_factoid(datum, AA):
    processed = []
    i = 1
    qid = datum['id']

    question = canonize(datum['body'], AA)

    for snippet in datum['snippets']:
        snippet = canonize(snippet['text'], AA)
        answer = canonize(datum['exact_answer'][0], AA)

        ind = snippet.find(answer)
        if ind > -1:
            new_entry = {'id': f'{qid}_{i:04}', 'question': question, 
                         'answers': {'text': [answer], 'answer_start': [ind]},
                         'type': datum['type'], 'context': snippet}
            processed.append(new_entry)
            i += 1
    return processed

def preprocess_dataset(dataset, AA):
    processed = []
    for datum in dataset:
        if datum['type'] == 'list':
            processed.extend(preprocess_list(datum, AA))
        elif datum['type'] == 'factoid':
            processed.extend(preprocess_factoid(datum, AA))
    return processed


if __name__ == "__main__":
    infile = "BioASQ-training11b/training11b.json"
    x = json.load(open(infile))

    # Load the acronyms/abbreviations dict
    # AA = load_AA(x['questions'])
    AA = {}

    # Process the file
    processed = preprocess_dataset(x['questions'], AA)
    out = {'data': processed}
    with open('train_file.json', 'w') as f:
        json.dump(out, f, indent=4)

    # Split training file
    x = json.load(open("train_file.json"))
    data = x['data']
    random.Random(11797).shuffle(data)
    split_index = int(len(data)*0.8)
    train_data = data[:split_index]
    test_data = data[split_index:]

    output_train = {"data": train_data}
    output_test = {"data": test_data}

    with open('train_file_80.json', 'w') as f:
        json.dump(output_train, f)
    with open('test_file_80.json', 'w') as f:
        json.dump(output_test, f)