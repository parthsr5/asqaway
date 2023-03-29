import json
from collections import defaultdict
from tqdm import tqdm

from pymetamap import MetaMap

CONF_THRESH = 0.2


metamap_base_dir = '/home/sourjyadip/asqaway/umls/public_mm/'
metamap_bin_dir = 'bin/metamap20'
metamap_pos_server_dir = 'bin/skrmedpostctl'
metamap_wsd_server_dir = 'bin/wsdserverctl'

metam = MetaMap.get_instance(metamap_base_dir + metamap_bin_dir)

def get_cuis(text):
    cuis = {}
    concepts, _ = metam.extract_concepts([text],
                                         word_sense_disambiguation = True,
                                         composite_phrase = 1)
    for con in concepts:
        if hasattr(con, 'mm'):
            cuis.add(con.cui)
    return cuis

if __name__ == "__main__":
    prediction_file = ""
    with open(prediction_file, "r") as f:
        predictions = json.load(f)

    question_file = ""
    with open(question_file, "r") as f:
        questions = json.load(f)

    # Combine all predictions for same question
    preds = defaultdict(list)
    for id, pred in predictions.items():
        real_id = id.split("_")[0]
        preds[real_id].extend(pred)

    # Check for overlapping CIDs and keep if non-overlapping
    answers = {}
    for id, pred in preds.items():
        pred = sorted(pred, key=lambda x: x['probability'], reverse=True)
        cui_set = set()
        answers[id] = []

        # get answers
        for p in pred:
            if p['probability'] < CONF_THRESH:
                break
            p_cui_set = get_cuis(p['text'])
            if cui_set.isdisjoint(p_cui_set):
                answers[id].append(p)
                cui_set = cui_set.union(p_cui_set)
        
        # # update original question
        # for i, q in enumerate(questions['questions']):
        #     if q['id'] == id:
        #         break
        # if questions['questions'][i]['type'] == 'list':
        #     questions['questions'][0]['exact_answer'] = [[ans] for ans in answers]
        # elif questions['questions'][i]['type'] == 'factoid':
        #     questions['questions'][0]['exact_answer'] = [[ans] for ans in answers[:5]]
    
    with open("final_answers.json", "w") as f:
        json.dump(answers, f, indent=4)
