set -x

export NCCL_DEBUG=WARN
export WANDB_API_KEY='your-wandb-api-key'
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export TOKENIZERS_PARALLELISM=true

export FINE_GRAINED_SCHEMA=True

cd train/PRIME/training/

PROJECT_NAME='PRIME'
EXPERIMENT_NAME='llama3.2-3b-srl'
DATA_PATH=../../data
SFT_MODEL_PATH=meta-llama/Llama-3.2-3B-Instruct
CKPT_PATH=../../results


python3 -m verl.trainer.main_ppo \
    data.train_files=["$DATA_PATH/train_with_tool_ToS.parquet"] \
    data.val_files=["$DATA_PATH/val_with_tool_ToS.parquet"] \
    data.train_batch_size=32 \
    data.val_batch_size=64 \
    data.max_prompt_length=8196 \
    data.max_response_length=2048 \
    actor_rollout_ref.model.path=$SFT_MODEL_PATH \
    actor_rollout_ref.actor.optim.lr=5e-7 \
    actor_rollout_ref.actor.ppo_mini_batch_size=32 \
    actor_rollout_ref.actor.ppo_micro_batch_size=8 \
    actor_rollout_ref.actor.fsdp_config.param_offload=True \
    actor_rollout_ref.actor.fsdp_config.grad_offload=True \
    actor_rollout_ref.actor.fsdp_config.optimizer_offload=True \
    actor_rollout_ref.model.use_remove_padding=True \
    actor_rollout_ref.actor.entropy_coeff=0. \
    actor_rollout_ref.rollout.log_prob_micro_batch_size=32 \
    actor_rollout_ref.rollout.tensor_model_parallel_size=1 \
    actor_rollout_ref.rollout.name=vllm \
    actor_rollout_ref.rollout.gpu_memory_utilization=0.7 \
    actor_rollout_ref.ref.log_prob_micro_batch_size=32 \
    actor_rollout_ref.ref.fsdp_config.param_offload=True \
    algorithm.kl_ctrl.kl_coef=0.00 \
    trainer.logger=['console','wandb'] \
    trainer.project_name=$PROJECT_NAME \
    trainer.experiment_name=$EXPERIMENT_NAME \
    trainer.default_local_dir=$CKPT_PATH/$EXPERIMENT_NAME \
    trainer.n_gpus_per_node=8 \
    trainer.nnodes=1 \
    trainer.save_freq=16 \
    trainer.test_freq=16 \
    trainer.total_epochs=1 \
    data.n_samples=4 \
    data.filter_accuracy=True \
    data.accuracy_lower_bound=0.2 \
    data.accuracy_upper_bound=0.9999 \
    algorithm.adv_estimator=rloo \
    algorithm.adv_params.verifier_gamma=1.0 \
    algorithm.adv_params.reward_model_gamma=1.0 \
    reward_model.rm_type=prime \
    reward_model.rm_coef=5 \
    reward_model.prime_model.path=$SFT_MODEL_PATH  \
    reward_model.prime_model.ref_path=$SFT_MODEL_PATH  \
    reward_model.model.input_tokenizer=null \
    reward_model.prime_model.use_remove_padding=True \
    reward_model.prime_granularity=token \
    reward_model.micro_batch_size=8 \
    reward_model.mini_batch_size=32 \
    reward_model.prime_model.update=after \
    reward_model.prime_model.beta_train=0.05 \
    reward_model.prime_model.optim.lr=1e-6 \
    reward_model.prime_model.optim.grad_clip=10.0 \
    reward_model.prime_model.input_tokenizer=null \
    trainer.default_local_dir=$CKPT_PATH/$PROJECT_NAME/$EXPERIMENT_NAME \
