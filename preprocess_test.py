import json
import random
import os
import re
from tqdm import tqdm
import pdb

import concurrent
from concurrent.futures import ThreadPoolExecutor, as_completed

from pymetamap import MetaMap


metamap_base_dir = '/home/sourjyadip/asqaway/umls/public_mm/'
metamap_bin_dir = 'bin/metamap20'
metamap_pos_server_dir = 'bin/skrmedpostctl'
metamap_wsd_server_dir = 'bin/wsdserverctl'
MAX_THREADS = 32

metam = MetaMap.get_instance(metamap_base_dir + metamap_bin_dir)


def get_AA(text):
    mappings = {}
    concepts, _ = metam.extract_concepts([text],
                                         word_sense_disambiguation = True,
                                         composite_phrase = 1)
    for con in concepts:
        if hasattr(con, 'aa'):
            # print(con)
            offset, length = tuple(int(x) for x in con.pos_info.split(":"))
            # print(type(offset), type(length), offset, length)
            # pdb.set_trace()
            word = con.short_form
            if word not in mappings:
                mappings[word] = con.long_form
    return mappings

def load_AA_list(datum):
    AA = {}
    AA.update(get_AA(datum['body']))
    for snippet in datum['snippets']:
        AA.update(get_AA(snippet['text']))
    return AA

def load_AA_factoid(datum):
    AA = {}
    AA.update(get_AA(datum['body']))
    for snippet in datum['snippets']:
        AA.update(get_AA(snippet['text']))
    return AA

def load_AA(dataset):
    AA = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        for datum in tqdm(dataset, desc='Submitting Jobs'):
            if datum['type'] == 'list': futures.append(executor.submit(load_AA_list, datum))
                # AA.update(load_AA_list(datum))
            elif datum['type'] == 'factoid': futures.append(executor.submit(load_AA_factoid, datum))
                # AA.update(load_AA_factoid(datum))
        print(len(futures), 'jobs to process')
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Running Jobs"):
            AA.update(future.result())
    return AA


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

def preprocess_list(datum, AA):
    processed = []
    i = 1
    qid = datum['id']

    question = canonize(datum['body'], AA)
    
    for snippet in datum['snippets']:
        snippet = canonize(snippet['text'], AA)
        new_entry = {'id': f'{qid}_{i:04}', 'question': question,
                        # 'answers': {'text': [answer], 'answer_start': [ind]},
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

        new_entry = {'id': f'{qid}_{i:04}', 'question': question, 
                        # 'answers': {'text': [answer], 'answer_start': [ind]},
                        'type': datum['type'], 'context': snippet}
        processed.append(new_entry)
        i += 1
    return processed

def preprocess_dataset(dataset, AA):
    processed = []
    for datum in tqdm(dataset):
        if datum['type'] == 'list':
            processed.extend(preprocess_list(datum, AA))
        elif datum['type'] == 'factoid':
            processed.extend(preprocess_factoid(datum, AA))
    return processed


if __name__ == "__main__":
    infile = "BioASQ-training11b/training11b.json"
    x = json.load(open(infile))

    # Load the acronyms/abbreviations dict
    if not os.path.exists("umls_data.json"):
        AA = load_AA(x['questions'])
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
    with open('train_file.json', 'w') as f:
        json.dump(out, f, indent=4)
