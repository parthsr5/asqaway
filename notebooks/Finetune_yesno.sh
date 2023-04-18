python transformers/examples/pytorch/text-classification/run_glue.py \
    --model_name_or_path dmis-lab/biobert-base-cased-v1.1-squad \
    --tokenizer_name dmis-lab/biobert-base-cased-v1.1-squad \
    --do_train=True \
    --train_file train_file_80_yesno.json \
    --do_eval=True \
    --validation_file test_file_80_yesno.json \
    --do_predict=True \
    --test_file test_file_80_yesno.json \
    --num_train_epochs 5 \
    --save_strategy epoch \
    --evaluation_strategy epoch \
    --metric_for_best_model f1 \
    --load_best_model_at_end \
    --output_dir /content/biobert_yesno \
    --overwrite_output_dir

python transformers/examples/pytorch/text-classification/run_glue.py \
    --model_name_or_path sultan/BioM-ELECTRA-Base-SQuAD2 \
    --tokenizer_name sultan/BioM-ELECTRA-Base-SQuAD2 \
    --do_train=True \
    --train_file train_file_80_yesno.json \
    --do_eval=True \
    --validation_file test_file_80_yesno.json \
    --do_predict=True \
    --test_file test_file_80_yesno.json \
    --num_train_epochs 5 \
    --save_strategy epoch \
    --evaluation_strategy epoch \
    --metric_for_best_model f1 \
    --load_best_model_at_end \
    --output_dir /content/bioelectra_base_yesno \
    --overwrite_output_dir

python transformers/examples/pytorch/text-classification/run_glue.py \
    --model_name_or_path sultan/BioM-ALBERT-xxlarge-SQuAD2 \
    --tokenizer_name sultan/BioM-ALBERT-xxlarge-SQuAD2 \
    --do_train=True \
    --train_file train_file_80_yesno.json \
    --per_device_train_batch_size 4 \
    --do_eval=True \
    --validation_file test_file_80_yesno.json \
    --do_predict=True \
    --test_file test_file_80_yesno.json \
    --num_train_epochs 1 \
    --save_strategy epoch \
    --evaluation_strategy epoch \
    --metric_for_best_model f1 \
    --load_best_model_at_end \
    --output_dir /content/bioalbert_base_yesno \
    --fp16 \
    --overwrite_output_dir

cd /content
ls
# !cp biobert_base_yesno/ drive/MyDrive/11797
# !cp bioelectra_base_yesno/ drive/MyDrive/11797
# mv bioalbert_base_yesno/ drive/MyDrive/11797
