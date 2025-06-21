#!/bin/bash
# Use WD14 tagger to generate tags for Rinni images

# Activate virtual environment
source /mnt/c/Users/jcook/git/kohya_ss/venv/bin/activate

# Navigate to kohya_ss directory
cd /mnt/c/Users/jcook/git/kohya_ss

# Create backup of existing captions
echo "Creating backup of existing captions..."
mkdir -p train_data/rinni/10_rinni/backup_captions
cp train_data/rinni/10_rinni/*.txt train_data/rinni/10_rinni/backup_captions/ 2>/dev/null || true

# Run WD14 tagger
echo "Running WD14 tagger on Rinni images..."
python sd-scripts/finetune/tag_images_by_wd14_tagger.py \
    train_data/rinni/10_rinni \
    --repo_id "SmilingWolf/wd-v1-4-convnext-tagger-v2" \
    --force_download \
    --batch_size 1 \
    --thresh 0.35 \
    --general_threshold 0.35 \
    --character_threshold 0.45 \
    --caption_extension .txt \
    --remove_underscore \
    --undesired_tags "realistic,photo,simple_background,white_background" \
    --always_first_tags "rinni" \
    --character_tags_first \
    --caption_separator ", " \
    --onnx

echo "Tagging complete!"
echo "Original captions backed up to: train_data/rinni/10_rinni/backup_captions/"