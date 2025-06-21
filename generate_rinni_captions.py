#!/mnt/c/Users/jcook/git/kohya_ss/venv/bin/python
"""
Generate captions for Rinni vtuber images using Claude API
"""
import os
import base64
import time
from anthropic import Anthropic
from pathlib import Path
from PIL import Image
import io

# Initialize the Anthropic client
# You'll need to set your API key as an environment variable: ANTHROPIC_API_KEY
client = Anthropic()

def encode_image(image_path):
    """Encode image to base64 for API, resizing if necessary"""
    # Open the image
    img = Image.open(image_path)
    
    # Convert RGBA to RGB if necessary
    if img.mode == 'RGBA':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    
    # Check file size and resize if needed
    max_size = 4.5 * 1024 * 1024  # 4.5MB to be safe
    
    # Save to bytes and check size
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=95)
    
    # If too large, resize
    while img_byte_arr.tell() > max_size:
        # Reduce dimensions by 20%
        new_width = int(img.width * 0.8)
        new_height = int(img.height * 0.8)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save again
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=90)
    
    img_byte_arr.seek(0)
    return base64.b64encode(img_byte_arr.read()).decode('utf-8')

def generate_caption(image_path, image_name):
    """Generate a caption for a single image using Claude"""
    # Encode the image
    base64_image = encode_image(image_path)
    
    # Always use JPEG format after processing
    media_type = "image/jpeg"
    
    # Create the prompt
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
    # Directory containing the images
    image_dir = Path("/mnt/c/Users/jcook/git/kohya_ss/train_data/rinni/10_rinni")
    
    # Get all image files
    image_files = list(image_dir.glob("*.png")) + list(image_dir.glob("*.jpg"))
    
    print(f"Found {len(image_files)} images to caption")
    
    # Process each image
    for i, image_path in enumerate(image_files, 1):
        image_name = image_path.name
        caption_path = image_path.with_suffix('.txt')
        
        # Skip if caption already exists
        if caption_path.exists():
            print(f"[{i}/{len(image_files)}] Skipping {image_name} - caption already exists")
            continue
        
        print(f"[{i}/{len(image_files)}] Generating caption for {image_name}...")
        
        # Generate caption
        caption = generate_caption(image_path, image_name)
        
        if caption:
            # Save the caption
            with open(caption_path, 'w', encoding='utf-8') as f:
                f.write(caption)
            print(f"    ✓ Caption saved: {caption[:50]}...")
        else:
            print(f"    ✗ Failed to generate caption")
        
        # Rate limiting - Claude has rate limits, so we'll add a small delay
        time.sleep(2)
    
    print("\nCaption generation complete!")
    
    # Show summary
    total_captions = len(list(image_dir.glob("*.txt")))
    print(f"Total captions created: {total_captions}/{len(image_files)}")

if __name__ == "__main__":
    # Check if API key is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: Please set your ANTHROPIC_API_KEY environment variable")
        print("Example: export ANTHROPIC_API_KEY='your-api-key-here'")
        exit(1)
    
    main()