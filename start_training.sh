#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export CUDA_VISIBLE_DEVICES=0

# Start training
accelerate launch --num_cpu_threads_per_process=2 sd-scripts/train_network.py \
  --pretrained_model_name_or_path="runwayml/stable-diffusion-v1-5" \
  --dataset_config="train_lora_config.toml" \
  --output_dir="./output" \
  --output_name="food_lora" \
  --save_model_as=safetensors \
  --prior_loss_weight=1 \
  --max_train_epochs=10 \
  --learning_rate=1e-4 \
  --unet_lr=1e-4 \
  --text_encoder_lr=5e-5 \
  --optimizer_type="AdamW8bit" \
  --xformers \
  --mixed_precision="fp16" \
  --cache_latents \
  --gradient_checkpointing \
  --save_every_n_epochs=2