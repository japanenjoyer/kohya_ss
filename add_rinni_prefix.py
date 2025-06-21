#!/mnt/c/Users/jcook/git/kohya_ss/venv/bin/python
"""
Add 'rinni' to the beginning of each caption if it's not already there
"""
from pathlib import Path

def main():
    caption_dir = Path("/mnt/c/Users/jcook/git/kohya_ss/train_data/rinni/10_rinni")
    
    for txt_file in caption_dir.glob("*.txt"):
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Check if 'rinni' is already at the beginning
        if not content.lower().startswith('rinni'):
            # Add 'rinni' at the beginning
            new_content = f"rinni, {content}"
            
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✓ Added 'rinni' to {txt_file.name}")
        else:
            print(f"  {txt_file.name} already has 'rinni'")
    
    print("\nDone!")

if __name__ == "__main__":
    main()