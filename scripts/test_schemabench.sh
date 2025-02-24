MODEL_NAME=llama3_1

python schemabench/unionbench.py \
    --model $MODEL_NAME \
    --save_path ./schemabench/results/$MODEL_NAME.jsonl \
    --subset False \
    --test_category schema \