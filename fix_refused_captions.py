#!/mnt/c/Users/jcook/git/kohya_ss/venv/bin/python
"""
Fix refused captions with appropriate alternatives
"""
import os
from pathlib import Path

def create_appropriate_caption(filename):
    """Create an appropriate caption based on filename"""
    base = "rinni, ethereal moon goddess, fantasy character"
    
    # Add context based on filename
    if "vts" in filename.lower():
        return f"{base}, virtual streaming setup, celestial atmosphere, moonlit studio"
    elif "spoiler" in filename.lower():
        return f"{base}, exclusive design, special outfit, mystical appearance"
    elif "bun" in filename.lower():
        return f"{base}, bunny theme, lunar rabbit, celestial creature"
    elif "suit" in filename.lower():
        return f"{base}, elegant attire, formal outfit, sophisticated appearance"
    elif "summer" in filename.lower():
        return f"{base}, summer theme, seasonal design, warm atmosphere"
    elif "nude" in filename.lower() or "nsfw" in filename.lower():
        return f"{base}, artistic pose, ethereal form, celestial beauty"
    elif "dress" in filename.lower():
        return f"{base}, flowing dress, elegant garment, fantasy costume"
    elif "booba" in filename.lower() or "lewd" in filename.lower():
        return f"{base}, fantasy design, stylized appearance, artistic composition"
    else:
        return f"{base}, mystical presence, otherworldly beauty, fantasy art"

def main():
    image_dir = Path("/mnt/c/Users/jcook/git/kohya_ss/train_data/rinni/10_rinni")
    os.chdir(image_dir)
    
    # Find all refused captions
    refused_captions = []
    for txt_file in Path(".").glob("*.txt"):
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if "I apologize" in content or "I do not feel comfortable" in content:
                refused_captions.append(txt_file)
    
    print(f"Found {len(refused_captions)} refused captions to fix")
    
    # Fix each one
    for caption_file in refused_captions:
        # Find corresponding image
        image_name = caption_file.stem
        
        # Create appropriate caption
        new_caption = create_appropriate_caption(image_name)
        
        # Save it
        with open(caption_file, 'w', encoding='utf-8') as f:
            f.write(new_caption)
        
        print(f"✓ Fixed {caption_file.name}: {new_caption}")
    
    print(f"\nFixed all {len(refused_captions)} captions!")

if __name__ == "__main__":
    main()