import json
from collections import defaultdict
from tqdm import tqdm

import concurrent
from concurrent.futures import ThreadPoolExecutor, as_completed

CONF_THRESH = 0.0


models = "biom-electra biom-albert biobert".split()
split = "eval"
MAX_THREADS = 32

def remove_synonyms(id, pred):
    pred = sorted(pred, key=lambda x: x['probability'], reverse=True)
    cui_set = set()
    answers = []

    # get answers
    for p in pred:
        if p['probability'] < CONF_THRESH:
            break
        if p['text'] not in {p_['text'] for p_ in answers}:
            answers.append(p)
    return id, answers

if __name__ == "__main__":
    for model in models:
        print("*"*5, model, split, "*"*5)
        prediction_file = f"{model}/{split}_nbest_predictions.json"
        with open(prediction_file, "r") as f:
            predictions = json.load(f)

        # question_file = ""
        # with open(question_file, "r") as f:
        #     questions = json.load(f)

        # Combine all predictions for same question
        preds = defaultdict(list)
        for id, pred in predictions.items():
            real_id = id.split("_")[0]
            preds[real_id].extend(pred)

        # Check for overlapping CIDs and keep if non-overlapping
        answers = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            futures = []
            for id, pred in tqdm(list(preds.items()), desc="Submitting Jobs, remove_synonyms"):            
                futures.append(executor.submit(remove_synonyms, id, pred))

            for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Running Jobs"):
                id, ans = future.result()
                answers[id] = ans

            # # update original question
            # for i, q in enumerate(questions['questions']):
            #     if q['id'] == id:
            #         break
            # if questions['questions'][i]['type'] == 'list':
            #     questions['questions'][0]['exact_answer'] = [[ans] for ans in answers]
            # elif questions['questions'][i]['type'] == 'factoid':
            #     questions['questions'][0]['exact_answer'] = [[ans] for ans in answers[:5]]

        with open(f"{model}/final_answers_{split}_{CONF_THRESH}_naive.json", "w") as f:
            json.dump(answers, f, indent=4)
