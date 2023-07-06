# Biomedical Question Answering using Transformer Ensembling
This is the code repository for "Biomedical Question Answering using Transformer Ensembling", by team ASQAway participating in the [BioASQ Task 11b Phase B](http://participants-area.bioasq.org/general_information/Task11b/) challenge. 


## Proposed Methodology
* Focus on Factoid, List, and Yes-No Questions of Task 11b Phase B
* Data Preprocessing - Bio-Medical Acronym expansion using [UMLS Metamap](https://www.nlm.nih.gov/research/umls/implementation_resources/metamap.html)
* Ensembling SOTA Transformer Models

## Task Overview
![Task Overview](task_overview.png)

## Repo Structure

    ├── data
    │   ├── train
    │   └── test_batches
    ├── model_results
    │   ├── biobert
    │   ├── biom-albert
    │   └── biom-electra
    ├── notebooks
    │   ├── exploratory_notebooks
    │   ├── Adversarial Finetuning_Eval.ipynb
    │   ├── Ensembling.ipynb
    │   ├── Model Finetuning_Eval.ipynb
    │   ├── Model Testing.ipynb
    │   └── ...
    ├── postprocess
    ├── preprocess
    ├── BioASQ-training11b.zip
    └── ...
    
## References
Biomedical Question Answering using Transformer Ensembling, CLEF 2023 - Raghav R, Jason Rauchwerk, Parth Rajwade, Tanay Gummadi, Eric Nyberg and Teruko Mitamura
```
(BibTex will be updated soon)
```

Overview of the BioASQ11 lab and corresponding BioASQ task
```
@inproceedings{BioASQ2023overview,
    title={{Overview of BioASQ 2023: The eleventh BioASQ challenge on Large-Scale Biomedical Semantic Indexing and Question Answering}},
    author={Nentidis, Anastasios and Katsimpras, Georgios and Krithara, Anastasia and Lima-López, Salvador and Farré-Maduell, Eulàlia and Gasco, Luis and Krallinger, Martin and Paliouras, Georgios},
    booktitle={ Experimental IR Meets Multilinguality, Multimodality, and Interaction. Proceedings of the Fourteenth International Conference of the CLEF Association (CLEF 2023)
}

@inproceedings{BioASQ2023task11bSynergy,
    title={{Overview of BioASQ Tasks 11b and Synergy11 in CLEF2023}},
    author={Nentidis, Anastasios and Katsimpras, Georgios and Krithara, Anastasia and Paliouras, Georgios},
    booktitle={Working Notes of CLEF 2023 - Conference and Labs of the Evaluation Forum}, year={2023}
}
```

BioASQ Task 11b dataset
```
@article{krithara2023bioasq,
    title={{BioASQ-QA: A manually curated corpus for Biomedical Question Answering}},
    author={Krithara, Anastasia and Nentidis, Anastasios and Bougiatiotis, Konstantinos and Paliouras, Georgios},
    journal={Scientific Data},
    volume={10},
    number={1},
    pages={170},
    year={2023},
    publisher={Nature Publishing Group UK London}
}
```
