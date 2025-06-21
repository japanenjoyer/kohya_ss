import json
import requests
import time
import os
from datetime import datetime

# ComfyUI API settings
COMFYUI_URL = "http://127.0.0.1:8188"

# Load prompts
with open('chinese_food_prompts.json', 'r') as f:
    prompts_data = json.load(f)

def generate_image(positive_prompt, negative_prompt, dish_name, seed=None):
    """Send generation request to ComfyUI API"""
    
    # Basic workflow - you'll need to adjust this to match your workflow
    workflow = {
        "3": {  # KSampler
            "inputs": {
                "seed": seed or -1,
                "steps": 20,
                "cfg": 7,
                "sampler_name": "euler_a",
                "scheduler": "normal",
                "denoise": 1,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0]
            },
            "class_type": "KSampler"
        },
        "4": {  # Load Checkpoint
            "inputs": {
                "ckpt_name": "sd_v1.5.safetensors"  # Update with your model
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "5": {  # Empty Latent
            "inputs": {
                "width": 512,
                "height": 512,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
        },
        "6": {  # Positive prompt
            "inputs": {
                "text": positive_prompt,
                "clip": ["10", 1]  # From LoRA
            },
            "class_type": "CLIPTextEncode"
        },
        "7": {  # Negative prompt
            "inputs": {
                "text": negative_prompt,
                "clip": ["10", 1]  # From LoRA
            },
            "class_type": "CLIPTextEncode"
        },
        "8": {  # VAE Decode
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2]
            },
            "class_type": "VAEDecode"
        },
        "9": {  # Save Image
            "inputs": {
                "filename_prefix": f"chinese_food_{dish_name}",
                "images": ["8", 0]
            },
            "class_type": "SaveImage"
        },
        "10": {  # LoRA Loader
            "inputs": {
                "lora_name": "chinese_food_lora.safetensors",
                "strength_model": 0.8,
                "strength_clip": 0.8,
                "model": ["4", 0],
                "clip": ["4", 1]
            },
            "class_type": "LoraLoader"
        }
    }
    
    # Send to ComfyUI
    try:
        response = requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": workflow})
        return response.json()
    except Exception as e:
        print(f"Error: {e}")
        return None

def batch_generate_dishes(dishes_to_generate=None):
    """Generate images for multiple dishes"""
    
    if dishes_to_generate is None:
        dishes_to_generate = list(prompts_data['dishes'].keys())
    
    results = []
    
    for dish in dishes_to_generate:
        if dish in prompts_data['dishes']:
            print(f"\nGenerating: {dish}")
            positive = prompts_data['dishes'][dish]['positive']
            negative = prompts_data['dishes'][dish]['negative']
            
            # Add style modifiers
            positive += ", professional food photography, appetizing, well lit"
            
            result = generate_image(positive, negative, dish)
            results.append({"dish": dish, "result": result})
            
            # Wait a bit between generations
            time.sleep(2)
        else:
            print(f"Dish '{dish}' not found in prompts")
    
    return results

# Quick generation script
if __name__ == "__main__":
    print("Chinese Food Batch Generator")
    print("============================")
    print("\nOptions:")
    print("1. Generate all dishes")
    print("2. Generate specific dish")
    print("3. Custom prompt")
    
    choice = input("\nChoice (1-3): ")
    
    if choice == "1":
        batch_generate_dishes()
    elif choice == "2":
        print("\nAvailable dishes:")
        for dish in prompts_data['dishes'].keys():
            print(f"  - {dish}")
        dish_name = input("\nEnter dish name: ")
        batch_generate_dishes([dish_name])
    elif choice == "3":
        positive = input("Positive prompt: ")
        negative = input("Negative prompt: ")
        generate_image(positive, negative, "custom")
    
    print("\nDone! Check ComfyUI output folder for images.")