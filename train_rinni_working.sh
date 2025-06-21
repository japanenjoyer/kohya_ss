#!/bin/bash

# Rinni VTuber LoRA Training Script
echo "Starting Rinni VTuber LoRA Training..."
echo "=================================="

# Activate virtual environment
source venv/bin/activate

# Create output directory if it doesn't exist
mkdir -p output

# Run training with command line arguments (like the working food script)
python sd-scripts/train_network.py \
  --pretrained_model_name_or_path="/mnt/c/Users/jcook/git/ComfyUI/models/checkpoints/v1-5-pruned-emaonly-fp16.safetensors" \
  --train_data_dir="train_data" \
  --output_dir="./output" \
  --output_name="rinni_vtuber_lora" \
  --save_model_as=safetensors \
  --max_train_epochs=10 \
  --learning_rate=1e-4 \
  --network_module=networks.lora \
  --network_dim=128 \
  --network_alpha=64 \
  --mixed_precision="fp16" \
  --save_every_n_epochs=2 \
  --caption_extension=".txt" \
  --resolution=768 \
  --train_batch_size=1 \
  --enable_bucket \
  --cache_latents

echo "=================================="
echo "Training complete! Check ./output/ for your Rinni LoRA."