import os

# Define better names based on what I saw in the images
rename_map = {
    "chinese_food_1.jpg": "udon_vegetable_soup_clear_broth.jpg",
    "chinese_food_3.jpg": "orange_glazed_shrimp_broccoli_white_rice.jpg",
    "chinese_food_4.jpg": "shrimp_pad_thai_rice_noodles_bean_sprouts.jpg",
    "chinese_food_5.jpg": "chinese_food_5.jpg",  # Still need to see this one
    "dumplings_1.jpg": "fried_spring_rolls_golden_crispy_sweet_chili_sauce.jpg",
    "dumplings_2.jpg": "steamed_gyoza_dumplings_sesame_seeds_wooden_bowl.jpg",
    "rice_dish_1.jpg": "yellow_biryani_rice_lime_cilantro_garnish.jpg",
    "rice_dish_2.jpg": "rice_dish_2.jpg",  # Still need to see this one
    "noodle_dish_1.jpg": "vietnamese_bun_bo_hue_spicy_beef_noodle_soup.jpg",
    "noodle_soup_1.jpg": "noodle_soup_1.jpg",  # Already fairly descriptive
}

# Paths
dest_dir = "/mnt/c/Users/jcook/git/kohya_ss/train_data/image/1_food"

# Perform the renaming
print("Renaming files with better descriptions...")
renamed_count = 0
errors = []

for old_name, new_name in rename_map.items():
    if old_name != new_name:  # Only rename if we have a new name
        old_path = os.path.join(dest_dir, old_name)
        new_path = os.path.join(dest_dir, new_name)
        
        if os.path.exists(old_path):
            # Also rename the caption file
            old_caption = old_path.replace('.jpg', '.txt')
            new_caption = new_path.replace('.jpg', '.txt')
            
            try:
                # Check if target already exists
                if os.path.exists(new_path):
                    print(f"Warning: {new_name} already exists, skipping")
                    continue
                    
                os.rename(old_path, new_path)
                if os.path.exists(old_caption):
                    os.rename(old_caption, new_caption)
                print(f"Renamed: {old_name} -> {new_name}")
                renamed_count += 1
            except Exception as e:
                error_msg = f"Error renaming {old_name}: {e}"
                print(error_msg)
                errors.append(error_msg)

print(f"\nTotal files renamed: {renamed_count}")
if errors:
    print("\nErrors encountered:")
    for error in errors:
        print(f"  - {error}")

# Now update captions for renamed files
print("\nUpdating captions for renamed files...")
caption_updates = {
    "udon_vegetable_soup_clear_broth": "food, japanese soup, udon noodles, clear broth, fresh vegetables, tofu, cucumber slices, red chili, healthy soup",
    "orange_glazed_shrimp_broccoli_white_rice": "food, chinese american, orange glazed shrimp, steamed broccoli, white rice, citrus sauce, restaurant presentation",
    "shrimp_pad_thai_rice_noodles_bean_sprouts": "food, thai cuisine, pad thai, shrimp, rice noodles, bean sprouts, lime wedge, traditional thai street food",
    "fried_spring_rolls_golden_crispy_sweet_chili_sauce": "food, spring rolls, golden crispy wrapper, fried appetizer, sweet chili sauce, salad garnish, asian appetizer",
    "steamed_gyoza_dumplings_sesame_seeds_wooden_bowl": "food, japanese gyoza, steamed dumplings, sesame seeds, wooden bowl, chopsticks, traditional presentation",
    "yellow_biryani_rice_lime_cilantro_garnish": "food, indian biryani, yellow spiced rice, lime wedge, cilantro garnish, aromatic rice dish, bay leaf",
    "vietnamese_bun_bo_hue_spicy_beef_noodle_soup": "food, vietnamese soup, bun bo hue, rice noodles, spicy broth, beef slices, fresh herbs, lime"
}

for base_name, caption in caption_updates.items():
    caption_file = os.path.join(dest_dir, base_name + '.txt')
    try:
        with open(caption_file, 'w') as f:
            f.write(caption)
        print(f"Updated caption for: {base_name}")
    except Exception as e:
        print(f"Error updating caption for {base_name}: {e}")

print("\nRenaming complete!")