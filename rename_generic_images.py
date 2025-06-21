import os
import shutil

# Define better names based on what I saw in the images
rename_map = {
    "chinese_food_1.jpg": "udon_vegetable_soup_clear_broth.jpg",
    "chinese_food_3.jpg": "orange_glazed_shrimp_broccoli_white_rice.jpg",
    "chinese_food_4.jpg": "chinese_food_4.jpg",  # Keep for now, need to see it
    "chinese_food_5.jpg": "chinese_food_5.jpg",  # Keep for now, need to see it
    "dumplings_1.jpg": "fried_spring_rolls_golden_crispy.jpg",
    "dumplings_2.jpg": "dumplings_2.jpg",  # Keep for now, need to see it
    "rice_dish_1.jpg": "yellow_biryani_rice_lime_garnish.jpg",
    "rice_dish_2.jpg": "rice_dish_2.jpg",  # Keep for now, need to see it
    "noodle_dish_1.jpg": "vietnamese_bun_bo_hue_spicy_beef_noodle_soup.jpg",
    "hot_pot_1.jpg": "hot_pot_1.jpg",  # Keep for now
    "lo_mein_1.jpg": "lo_mein_1.jpg",  # Keep for now
    "ramen_1.jpg": "ramen_1.jpg",  # Keep for now
    "spring_rolls_1.jpg": "spring_rolls_1.jpg",  # Keep for now
    "wonton_soup_1.jpg": "wonton_soup_1.jpg",  # Keep for now
    "wontons_1.jpg": "wontons_1.jpg",  # Keep for now
    "stir_fry_vegetables_1.jpg": "stir_fry_vegetables_1.jpg",  # Keep for now
    "general_tso_chicken_1.jpg": "general_tso_chicken_1.jpg",  # Already descriptive
    "orange_chicken_1.jpg": "orange_chicken_1.jpg"  # Already descriptive
}

# Paths
source_dir = "/mnt/c/Users/jcook/git/image-maker/selected_images"
dest_dir = "/mnt/c/Users/jcook/git/kohya_ss/train_data/image/1_food"

# First, let's check the remaining generic images before renaming
print("Checking remaining generic images...")
remaining = ["chinese_food_4.jpg", "chinese_food_5.jpg", "dumplings_2.jpg", "rice_dish_2.jpg"]

for img in remaining:
    if img in rename_map and rename_map[img] == img:
        print(f"Need to check: {img}")

# Perform the renaming for images we've identified
print("\nRenaming files with better descriptions...")
renamed_count = 0

for old_name, new_name in rename_map.items():
    if old_name != new_name:  # Only rename if we have a new name
        old_path = os.path.join(dest_dir, old_name)
        new_path = os.path.join(dest_dir, new_name)
        
        if os.path.exists(old_path):
            # Also rename the caption file
            old_caption = old_path.replace('.jpg', '.txt')
            new_caption = new_path.replace('.jpg', '.txt')
            
            try:
                os.rename(old_path, new_path)
                if os.path.exists(old_caption):
                    os.rename(old_caption, new_caption)
                print(f"Renamed: {old_name} -> {new_name}")
                renamed_count += 1
            except Exception as e:
                print(f"Error renaming {old_name}: {e}")

print(f"\nTotal files renamed: {renamed_count}")
print("\nNote: Some files were kept with generic names pending review.")