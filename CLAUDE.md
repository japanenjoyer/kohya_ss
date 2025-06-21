# Kohya_ss Training Workflow Documentation

## VTuber/Anime Character LoRA Training Guide

### Overview
This document outlines the proven workflow for training LoRA models for VTuber and anime characters using kohya_ss, with specific emphasis on using WD14 tagger for caption generation.

### Why WD14 Tagger Over Claude/Other APIs

**Key Advantages:**
1. **No content restrictions** - Handles all types of anime/VTuber content professionally
2. **Designed for anime** - Understands anime-specific tags and conventions
3. **Game-aware** - Recognizes characters from games (FFXIV, FGO, etc.)
4. **Consistent format** - Outputs standardized booru-style tags
5. **Runs locally** - No API costs or rate limits
6. **No refusals** - Treats all images as training data without moral judgments

### Directory Structure
```
kohya_ss/
├── train_data/
│   └── character_name/
│       └── 10_character_name/
│           ├── image1.png
│           ├── image1.txt (caption)
│           └── ...
```

### Step-by-Step Workflow

#### 1. Prepare Images
```bash
# Create directory structure
mkdir -p train_data/character_name/10_character_name

# Copy images (supports PNG, JPG)
cp /path/to/images/*.png train_data/character_name/10_character_name/
```

#### 2. Generate Captions with WD14 Tagger

Create and use this script (`tag_character_wd14.sh`):
```bash
#!/bin/bash
source venv/bin/activate
cd /path/to/kohya_ss

# Backup existing captions if any
mkdir -p train_data/character_name/10_character_name/backup_captions
cp train_data/character_name/10_character_name/*.txt train_data/character_name/10_character_name/backup_captions/ 2>/dev/null || true

# Run WD14 tagger
python sd-scripts/finetune/tag_images_by_wd14_tagger.py \
    train_data/character_name/10_character_name \
    --repo_id "SmilingWolf/wd-v1-4-convnext-tagger-v2" \
    --batch_size 1 \
    --thresh 0.35 \
    --general_threshold 0.35 \
    --character_threshold 0.45 \
    --caption_extension .txt \
    --remove_underscore \
    --undesired_tags "realistic,photo,simple_background,white_background" \
    --character_tags_first \
    --caption_separator ", " \
    --onnx \
    --force_download
```

#### 3. Add Character Name to Captions

Create script to prepend character name (`add_character_prefix.py`):
```python
#!/usr/bin/env python3
from pathlib import Path

character_name = "character_name_here"  # Change this
caption_dir = Path(f"train_data/{character_name}/10_{character_name}")

for txt_file in caption_dir.glob("*.txt"):
    with open(txt_file, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    
    if not content.lower().startswith(character_name):
        new_content = f"{character_name}, {content}"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ Added '{character_name}' to {txt_file.name}")
```

#### 4. Training Configuration

Create `train_character_lora_config.toml`:
```toml
[general]
enable_bucket = true

[[datasets]]
resolution = 768  # Use 768 or 1024 for detailed characters
batch_size = 1

  [[datasets.subsets]]
  image_dir = '/path/to/kohya_ss/train_data/character_name/10_character_name'
  caption_extension = '.txt'
  num_repeats = 10  # Adjust based on image count (10 for 50-100 images)

[network_args]
network_module = 'networks.lora'
network_dim = 128  # 32-128 for characters, higher = more detail
network_alpha = 64

[optimizer_args]
learning_rate = 0.0001
lr_scheduler = 'cosine_with_restarts'
lr_warmup_steps = 0
lr_scheduler_num_cycles = 1

[training_args]
max_train_epochs = 10
save_every_n_epochs = 2
save_model_as = 'safetensors'
save_last_n_epochs = 3
keep_tokens = 0
clip_skip = 2
prior_loss_weight = 1
max_token_length = 225
xformers = true
max_data_loader_n_workers = 0
persistent_data_loader_workers = false
seed = 42
mixed_precision = 'fp16'

[sample_args]
sample_every_n_epochs = 1
sample_prompts = "character_name, 1girl, solo, looking at viewer"

[saving_args]
output_dir = './output'
output_name = 'character_name_lora'
save_precision = 'fp16'
```

#### 5. Training Script

Create `train_character.sh`:
```bash
#!/bin/bash
source venv/bin/activate
cd /path/to/kohya_ss

MODEL_PATH="./models/checkpoints/v1-5-pruned-emaonly-fp16.safetensors"

python sd-scripts/train_network.py \
  --config_file="./train_character_lora_config.toml" \
  --pretrained_model_name_or_path="$MODEL_PATH" \
  --logging_dir="./logs" \
  --enable_bucket \
  --min_bucket_reso=256 \
  --max_bucket_reso=1024 \
  --bucket_reso_steps=64
```

### Required Dependencies
```bash
# For WD14 tagger with ONNX (faster, no TensorFlow needed)
pip install onnx onnxruntime
```

### Tips for VTuber/Anime Training

1. **Image Selection**
   - Include variety: different outfits, poses, expressions
   - 30-100 images is usually sufficient
   - Mix SFW and NSFW if character has both

2. **Caption Quality**
   - WD14 tags are ideal for anime style
   - Always include character name as first tag
   - Don't worry about NSFW tags - they help model accuracy

3. **Training Parameters**
   - Higher resolution (768-1024) for detailed characters
   - Network dim 64-128 for character complexity
   - 10 epochs usually sufficient

4. **Testing**
   - Test with prompts like: "character_name, 1girl, solo, various_outfits"
   - Check if character features are consistent

### Common Issues & Solutions

**Issue**: Claude or other APIs refuse to caption certain images
**Solution**: Use WD14 tagger - it has no content restrictions

**Issue**: Large image files (>5MB)
**Solution**: WD14 handles them automatically, or pre-resize to 1024x1024

**Issue**: Inconsistent character features
**Solution**: Ensure character name is first tag in all captions

### Example Results
WD14 successfully tags all content types:
- `rinni, 1girl, solo, animal ears, rabbit ears, nude, onsen`
- `rinni, 1girl, nipples, spread legs, forest, mushroom`
- Handles explicit content professionally without refusals

This approach has been tested and proven effective for VTuber and anime character training.