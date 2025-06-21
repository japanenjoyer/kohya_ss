import os

image_dir = "/mnt/c/Users/jcook/git/kohya_ss/train_data/image/1_food"

# Create caption files for each image
for filename in os.listdir(image_dir):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        base_name = os.path.splitext(filename)[0]
        caption_file = os.path.join(image_dir, base_name + '.txt')
        
        # Create a caption based on the filename
        # Replace underscores with spaces and clean up the text
        caption = base_name.replace('_', ' ')
        # Remove numbering like _1, _2 at the end
        caption = ' '.join(caption.split()[:-1]) if caption.split()[-1].isdigit() else caption
        
        # Add the trigger word "food" to each caption
        caption = f"food, {caption}"
        
        with open(caption_file, 'w') as f:
            f.write(caption)
        
print(f"Created caption files for images in {image_dir}")