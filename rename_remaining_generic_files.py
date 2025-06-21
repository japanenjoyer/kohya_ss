import os

# Define better names based on what I saw in the images
rename_map = {
    "chinese_food_5.jpg": "shrimp_ramen_bowl_soft_boiled_eggs_snap_peas.jpg",
    "rice_dish_2.jpg": "steamed_momos_dumplings_tibetan_style_dipping_sauces.jpg",
    "hot_pot_1.jpg": "teriyaki_meatballs_spaghetti_cast_iron_skillet.jpg",
    "lo_mein_1.jpg": "dan_dan_noodles_bok_choy_spicy_meat_sauce.jpg",
    "general_tso_chicken_1.jpg": "general_tsos_chicken_crispy_glazed.jpg",
    "orange_chicken_1.jpg": "orange_chicken_crispy_citrus_glaze.jpg",
    "ramen_1.jpg": "japanese_ramen_noodle_soup_traditional.jpg",
    "spring_rolls_1.jpg": "crispy_spring_rolls_golden_fried.jpg",
    "stir_fry_vegetables_1.jpg": "mixed_vegetable_stir_fry_colorful.jpg",
    "wonton_soup_1.jpg": "wonton_soup_clear_broth_traditional.jpg",
    "wontons_1.jpg": "steamed_wontons_chinese_dumplings.jpg",
    "noodle_soup_1.jpg": "asian_noodle_soup_vegetables_broth.jpg"
}

# Path to the training directory
dest_dir = "/mnt/c/Users/jcook/git/kohya_ss/train_data/image/1_food"

# Perform the renaming
print("Renaming remaining generic files...")
renamed_count = 0
errors = []

for old_name, new_name in rename_map.items():
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

# Now update captions for renamed files
print("\nUpdating captions for renamed files...")
caption_updates = {
    "shrimp_ramen_bowl_soft_boiled_eggs_snap_peas": "food, ramen bowl, instant ramen elevated, shrimp, soft boiled eggs, snap peas, sesame seeds, japanese fusion",
    "steamed_momos_dumplings_tibetan_style_dipping_sauces": "food, momos, tibetan dumplings, steamed, pleated wrapper, dipping sauces, traditional himalayan cuisine",
    "teriyaki_meatballs_spaghetti_cast_iron_skillet": "food, fusion dish, teriyaki glazed meatballs, spaghetti noodles, cast iron skillet, asian italian fusion",
    "dan_dan_noodles_bok_choy_spicy_meat_sauce": "food, sichuan noodles, dan dan mian, spicy meat sauce, bok choy, sesame paste, scallions, authentic chinese",
    "general_tsos_chicken_crispy_glazed": "food, general tso chicken, crispy fried chicken, sweet spicy glaze, chinese american classic",
    "orange_chicken_crispy_citrus_glaze": "food, orange chicken, crispy battered chicken, tangy orange glaze, chinese american favorite",
    "japanese_ramen_noodle_soup_traditional": "food, japanese ramen, wheat noodles, savory broth, traditional toppings, authentic japanese",
    "crispy_spring_rolls_golden_fried": "food, spring rolls, crispy golden wrapper, deep fried, chinese appetizer, crunchy texture",
    "mixed_vegetable_stir_fry_colorful": "food, vegetable stir fry, colorful mixed vegetables, wok hei, healthy chinese dish",
    "wonton_soup_clear_broth_traditional": "food, wonton soup, pork wontons, clear chicken broth, traditional chinese soup",
    "steamed_wontons_chinese_dumplings": "food, wontons, steamed dumplings, chinese dim sum, traditional preparation",
    "asian_noodle_soup_vegetables_broth": "food, noodle soup, asian style, vegetable broth, comfort food, traditional preparation"
}

for base_name, caption in caption_updates.items():
    caption_file = os.path.join(dest_dir, base_name + '.txt')
    try:
        with open(caption_file, 'w') as f:
            f.write(caption)
        print(f"Updated caption for: {base_name}")
    except Exception as e:
        print(f"Error updating caption for {base_name}: {e}")

print("\nAll generic filenames have been updated!")

# Final check for any remaining generic names
print("\nChecking for any remaining generic filenames...")
remaining_generic = []
for filename in os.listdir(dest_dir):
    if filename.endswith('.jpg'):
        if any(pattern in filename for pattern in ['_1.jpg', '_2.jpg', '_3.jpg', '_4.jpg', '_5.jpg']) and not any(skip in filename for skip in ['_bing_', '_nana_']):
            remaining_generic.append(filename)

if remaining_generic:
    print(f"Found {len(remaining_generic)} files that might still be generic:")
    for f in remaining_generic[:10]:  # Show first 10
        print(f"  - {f}")
else:
    print("No more generic filenames found!")