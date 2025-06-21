#!/mnt/c/Users/jcook/git/kohya_ss/venv/bin/python
"""
Regenerate simple captions with Claude API
"""
import os
import base64
import time
from anthropic import Anthropic
from pathlib import Path
from PIL import Image
import io

client = Anthropic()

def encode_image(image_path):
    """Encode image to base64 for API, resizing if necessary"""
    img = Image.open(image_path)
    
    # Convert RGBA to RGB if necessary
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    
    # Start with original size
    quality = 95
    max_size = 4.5 * 1024 * 1024  # 4.5MB to be safe
    
    # Save to bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=quality)
    
    # If too large, resize incrementally
    scale = 1.0
    while img_byte_arr.tell() > max_size and scale > 0.3:
        scale *= 0.85
        new_width = int(img.width * scale)
        new_height = int(img.height * scale)
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        img_byte_arr = io.BytesIO()
        resized_img.save(img_byte_arr, format='JPEG', quality=85)
    
    img_byte_arr.seek(0)
    return base64.b64encode(img_byte_arr.read()).decode('utf-8')

def generate_caption(image_path, image_name):
    """Generate a caption for a single image using Claude"""
    base64_image = encode_image(image_path)
    media_type = "image/jpeg"
    
    prompt = """You are creating a training caption for a vtuber named Rinni. She is a moon-themed bunny vtuber who calls her viewers "moonbuns". 
    The images are often from gaming contexts like FFXIV and Stellar Blade.
    
    Please create an elegant, fantasy-themed caption that:
    1. Describes what you see in the image
    2. Mentions "rinni" as the subject
    3. Uses poetic, moonlit language when appropriate
    4. Keeps it under 75 words
    5. Focuses on visual elements, outfit, pose, and atmosphere
    
    Just provide the caption text, nothing else."""
    
    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        
        return message.content[0].text.strip()
    
    except Exception as e:
        print(f"Error generating caption for {image_name}: {e}")
        return None

def main():
    image_dir = Path("/mnt/c/Users/jcook/git/kohya_ss/train_data/rinni/10_rinni")
    os.chdir(image_dir)
    
    # Find all simple captions
    simple_captions = []
    for txt_file in Path(".").glob("*.txt"):
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.startswith("rinni, anime girl, vtuber"):
                simple_captions.append(txt_file)
    
    print(f"Found {len(simple_captions)} simple captions to regenerate")
    
    # Process each one
    success = 0
    failed = []
    
    for i, caption_file in enumerate(simple_captions, 1):
        image_path = caption_file.with_suffix('.png')
        if not image_path.exists():
            image_path = caption_file.with_suffix('.jpg')
        
        if not image_path.exists():
            print(f"[{i}/{len(simple_captions)}] ✗ No image found for {caption_file}")
            continue
            
        print(f"[{i}/{len(simple_captions)}] Regenerating caption for {image_path.name}...")
        
        caption = generate_caption(image_path, image_path.name)
        
        if caption:
            with open(caption_file, 'w', encoding='utf-8') as f:
                f.write(caption)
            print(f"    ✓ New caption: {caption[:60]}...")
            success += 1
        else:
            print(f"    ✗ Failed to generate caption")
            failed.append(image_path.name)
        
        # Rate limiting
        time.sleep(2)
    
    print(f"\nRegeneration complete!")
    print(f"Successfully regenerated: {success}/{len(simple_captions)}")
    if failed:
        print(f"Failed images: {', '.join(failed)}")

if __name__ == "__main__":
    main()