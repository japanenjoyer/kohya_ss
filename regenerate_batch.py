#!/mnt/c/Users/jcook/git/kohya_ss/venv/bin/python
"""
Regenerate captions in small batches
"""
import sys
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
    
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    
    # Aggressive resizing for large images
    max_dimension = 1024
    if img.width > max_dimension or img.height > max_dimension:
        ratio = min(max_dimension/img.width, max_dimension/img.height)
        new_width = int(img.width * ratio)
        new_height = int(img.height * ratio)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=85)
    img_byte_arr.seek(0)
    return base64.b64encode(img_byte_arr.read()).decode('utf-8')

def generate_caption(image_path):
    """Generate a caption for a single image using Claude"""
    base64_image = encode_image(image_path)
    
    prompt = """Create an artistic training caption for a fantasy character named Rinni. She is a moon-themed character. Include "rinni" in the caption. Focus on artistic elements like color, composition, lighting, and general aesthetic. Keep it under 75 words. Use elegant, fantasy language suitable for artistic training data."""
    
    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,
            temperature=0.7,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_image}},
                    {"type": "text", "text": prompt}
                ]
            }]
        )
        return message.content[0].text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    image_dir = Path("/mnt/c/Users/jcook/git/kohya_ss/train_data/rinni/10_rinni")
    os.chdir(image_dir)
    
    # Get batch number from command line
    batch_size = 5
    batch_num = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    
    # Find simple captions
    simple_captions = []
    for txt_file in Path(".").glob("*.txt"):
        with open(txt_file, 'r', encoding='utf-8') as f:
            if f.read().startswith("rinni, anime girl, vtuber"):
                simple_captions.append(txt_file)
    
    simple_captions.sort()
    
    # Process batch
    start = batch_num * batch_size
    end = min(start + batch_size, len(simple_captions))
    batch = simple_captions[start:end]
    
    if not batch:
        print(f"No more captions to process (batch {batch_num})")
        return
    
    print(f"Processing batch {batch_num} ({start+1}-{end} of {len(simple_captions)})")
    
    for i, caption_file in enumerate(batch, 1):
        image_path = caption_file.with_suffix('.png')
        if not image_path.exists():
            image_path = caption_file.with_suffix('.jpg')
        
        print(f"[{i}/{len(batch)}] Processing {image_path.name}...")
        
        caption = generate_caption(image_path)
        if caption:
            with open(caption_file, 'w', encoding='utf-8') as f:
                f.write(caption)
            print(f"    ✓ {caption[:60]}...")
        else:
            print(f"    ✗ Failed")
        
        time.sleep(1)
    
    print(f"\nBatch {batch_num} complete! Next batch: {batch_num + 1}")

if __name__ == "__main__":
    main()