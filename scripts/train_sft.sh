export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

python train/sft/trl_mix.py \
    --model_name meta-llama/Llama-3.2-3B-Instruct \
    --data_file ../data/mix_train.json \
    --output_dir results/llama3.2-3b-sft \
    --num_train_epochs 1 \
    --per_device_train_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --learning_rate 1e-5 \
    --max_seq_length 8192 \