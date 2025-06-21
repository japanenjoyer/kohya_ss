#!/bin/bash
# Training script for Rinni vtuber LoRA

# Activate virtual environment
source /mnt/c/Users/jcook/git/kohya_ss/venv/bin/activate

# Navigate to kohya_ss directory
cd /mnt/c/Users/jcook/git/kohya_ss

# Set model path - using the v1.5 model you have
MODEL_PATH="./models/checkpoints/v1-5-pruned-emaonly-fp16.safetensors"

# Run the training
python sd-scripts/train_network.py \
  --config_file="./train_rinni_fixed.toml" \
  --pretrained_model_name_or_path="$MODEL_PATH" \
  --logging_dir="./logs" \
  --enable_bucket \
  --min_bucket_reso=256 \
  --max_bucket_reso=1024 \
  --bucket_reso_steps=64

echo "Training complete! Check the output directory for your Rinni LoRA."