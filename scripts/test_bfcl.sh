MODEL=/your/path/to/schemabench/train/results/llama3.2-3b-srl

bfcl generate \
    --model $MODEL \
    --test-category live \
    --num-gpus 8 \

bfcl evaluate \
    --model $MODEL \
    --test-category live \