#!/mnt/c/Users/jcook/git/kohya_ss/venv/bin/python
"""
Simple caption generator for Rinni - creates basic captions as a fallback
"""
import os
from pathlib import Path

def create_simple_caption(image_name):
    """Create a simple caption based on filename"""
    # Base caption
    caption = "rinni, anime girl, vtuber"
    
    # Add context based on filename
    if "Luna" in image_name or "luna" in image_name:
        caption += ", moon goddess, celestial aura, lunar magic"
    elif "Studio" in image_name:
        caption += ", studio setting, professional lighting"
    elif "blue" in image_name:
        caption += ", blue outfit, elegant dress"
    elif "relaxing" in image_name:
        caption += ", relaxing pose, casual setting"
    elif "Gameplay" in image_name:
        caption += ", gaming, streaming, moonbun community"
    elif "SPOILER" in image_name:
        caption += ", special outfit, exclusive content"
    elif "Bun" in image_name or "bun" in image_name:
        caption += ", bunny theme, rabbit ears"
    elif "Summer" in image_name:
        caption += ", summer outfit, seasonal attire"
    else:
        caption += ", fantasy setting, ethereal beauty"
    
    return caption

def main():
    image_dir = Path("/mnt/c/Users/jcook/git/kohya_ss/train_data/rinni/10_rinni")
    
    # Get all image files
    image_files = list(image_dir.glob("*.png")) + list(image_dir.glob("*.jpg"))
    
    print(f"Creating simple captions for {len(image_files)} images...")
    
    created = 0
    for image_path in image_files:
        caption_path = image_path.with_suffix('.txt')
        
        if not caption_path.exists():
            caption = create_simple_caption(image_path.name)
            with open(caption_path, 'w', encoding='utf-8') as f:
                f.write(caption)
            created += 1
            print(f"✓ {image_path.name}")
    
    print(f"\nCreated {created} captions!")

if __name__ == "__main__":
    main()