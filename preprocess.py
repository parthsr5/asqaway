import json
import sys
import random
import os
import re
import time

from skr_web_api import Submission

email = os.environ['EMAIL']
apikey = os.environ['API_KEY']
inst = Submission(email, apikey)

def preprocess_list(datum):
    processed = []
    i = 1
    qid = datum['id']

    # for answer in datum['exact_answer']:
    #   answer = answer[0]
    #   for snippet in datum['snippets']:
    #     snippet = snippet['text']
    datum['body'] = "List signaling molecules (ligands) that interact with the receptor (EGFR)"#datum['body'].replace('?', "")
    print(canonize(datum['body']))
    
    for snippet in datum['snippets'][1:]:
        snippet = snippet['text']
        print(canonize(snippet))
        exit()
        for answer in datum['exact_answer']:
            answer = answer[0].lower()

            ind = snippet.find(answer)
            if ind > -1:
                new_entry = {'id': f'{qid}_{i:04}', 'question': datum['body'], 'answers': [
                    {'text': answer, 'answer_start': ind}]}
                processed.append({'qas': [new_entry], 'context': snippet})
                i += 1
    return processed


def preprocess_factoid(datum):
    processed = []
    i = 1
    qid = datum['id']

    for snippet in datum['snippets']:
        snippet = snippet['text']
        answer = datum['exact_answer'][0]

        ind = snippet.find(answer)
        if ind > -1:
            new_entry = {'id': f'{qid}_{i:04}', 'question': datum['body'], 'answers': [
                {'text': answer, 'answer_start': ind}]}
            processed.append({'qas': [new_entry], 'context': snippet})
            i += 1
    return processed


def preprocess_dataset(dataset):
    processed = []
    for datum in dataset:
        if datum['type'] == 'list':
            processed.extend(preprocess_list(datum))
        elif datum['type'] == 'factoid':
            processed.extend(preprocess_factoid(datum))
    return processed

def canonize(text):
    print(text)
    inst.init_mm_interactive(text)
    response = inst.submit()
    mappings = {}
    if response.status_code == 200:
        content = response.content.decode().split("\n")
        for line in content[1:]:
            # print(line)
            m = line.split("|")
            if len(m) > 1:
                # if m[1] == "MMI":
                #     for expansion in m[8].split(","):
                #         offset, length = tuple(int(x) for x in expansion.split("/"))
                #         word = text[offset: offset + length]
                #         if word not in mappings:
                #             mappings[word] = m[3]
                if m[1] == "AA":
                    offset, length = tuple(int(x) for x in m[8].split(":"))
                    word = text[offset: offset + length]
                    if word not in mappings:
                        mappings[word] = m[3]
    else:
        raise NotImplementedError

    print(mappings)
    for word, new_word in mappings.items():
        text = text.replace(word, new_word)
    return text

if __name__ == "__main__":
    infile = "BioASQ-training11b/training11b.json"
    x = json.load(open(infile))

    processed = preprocess_dataset(x['questions'])
    out = {}
    out['data'] = []
    for i in x['data'][0]['paragraphs']:
        data = i['qas'][0]
        data['context'] = i['context']
        data['answers'] = data['answers'][0]
        data['answers']['answer_start'] = [data['answers']['answer_start']]
        data['answers']['text'] = [data['answers']['text']]
        out['data'].append(data)
    with open('train_file.json', 'w') as f:
        json.dump(out, f)

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
