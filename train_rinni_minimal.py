#!/usr/bin/env python3
import os
import sys

# Add sd-scripts to path
sys.path.insert(0, 'sd-scripts')

# Set environment to avoid some import issues
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Run training directly
if __name__ == "__main__":
    sys.argv = [
        'train_network.py',
        '--pretrained_model_name_or_path=/mnt/c/Users/jcook/git/ComfyUI/models/checkpoints/v1-5-pruned-emaonly-fp16.safetensors',
        '--train_data_dir=train_data',
        '--output_dir=./output',
        '--output_name=rinni_vtuber_lora',
        '--save_model_as=safetensors',
        '--max_train_epochs=10',
        '--learning_rate=1e-4',
        '--network_module=networks.lora',
        '--network_dim=128',
        '--network_alpha=64',
        '--mixed_precision=fp16',
        '--save_every_n_epochs=2',
        '--caption_extension=.txt',
        '--resolution=768',
        '--train_batch_size=1',
        '--enable_bucket',
        '--cache_latents'
    ]
    
    # Import and run
    from train_network import main
    main(sys.argv[1:])