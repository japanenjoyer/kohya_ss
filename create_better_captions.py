import os

# Define detailed captions for specific images based on what I can see
caption_map = {
    "beef_and_broccoli_chinese_takeout_bing": "food, chinese food, beef and broccoli stir fry, glossy brown sauce, tender beef slices, fresh green broccoli florets, sesame seeds garnish, wok hei, takeout style",
    "brown_sugar_bubble_tea_boba_milk_nana": "food, bubble tea, brown sugar boba milk tea, creamy milk tea, caramel brown sugar swirls, black tapioca pearls, glass straw, taiwanese drink",
    "dim_sum_platter": "food, dim sum, chinese dumplings, bamboo steamer baskets, traditional dim sum presentation, multiple varieties, restaurant style",
    "california_roll_sushi_nana": "food, sushi, california roll, japanese cuisine, avocado, cucumber, crab, sesame seeds, maki roll",
    "char_siu_bao_steamed_bbq_pork_buns_bing": "food, chinese buns, char siu bao, steamed pork buns, fluffy white dough, bbq pork filling",
    "chicken_chow_mein_crispy_noodles_bing": "food, chinese noodles, chicken chow mein, crispy fried noodles, stir fried vegetables, chicken pieces",
    "chinese_cold_sesame_noodles_nana": "food, cold noodles, sesame noodles, chinese cuisine, sesame sauce, julienned vegetables, refreshing dish",
    "dan_dan_noodles_sichuan_spicy_bing": "food, sichuan noodles, dan dan mian, spicy sauce, ground meat, scallions, chili oil",
    "dumplings": "food, chinese dumplings, potstickers, jiaozi, pleated dough, golden brown bottom",
    "general_tso_chicken": "food, chinese american, general tso chicken, crispy fried chicken, sweet spicy glaze, broccoli garnish",
    "har_gow_crystal_shrimp_dumplings_bing": "food, dim sum, har gow, translucent wrapper, shrimp dumplings, pleated design, cantonese cuisine",
    "hot_pot": "food, chinese hot pot, communal dining, simmering broth, various ingredients, interactive meal",
    "kung_pao_chicken_sichuan_restaurant_bing": "food, sichuan cuisine, kung pao chicken, dried chilies, peanuts, diced chicken, spicy stir fry",
    "lo_mein": "food, chinese noodles, lo mein, soft wheat noodles, mixed vegetables, savory sauce",
    "mongolian_beef_pf_changs_recipe_bing": "food, mongolian beef, tender beef strips, scallions, sweet savory sauce, chinese american",
    "orange_chicken": "food, orange chicken, crispy battered chicken, tangy orange glaze, citrus flavor, chinese american",
    "pad_thai_noodles_authentic_nana": "food, thai cuisine, pad thai, rice noodles, tamarind sauce, peanuts, lime wedge, bean sprouts",
    "pineapple_fried_rice_thai_style_nana": "food, thai fried rice, pineapple fried rice, curry spices, fresh pineapple chunks, cashews",
    "pot_stickers_pan_fried_dumplings_bing": "food, potstickers, pan fried dumplings, crispy bottom, steamed top, chinese appetizer",
    "ramen": "food, japanese ramen, noodle soup, rich broth, chashu pork, soft boiled egg, nori, scallions",
    "spring_rolls": "food, spring rolls, crispy fried wrapper, vegetable filling, golden brown, chinese appetizer",
    "sushi_platter_assorted_nigiri_maki_nana": "food, sushi platter, assorted sushi, nigiri, maki rolls, sashimi, japanese cuisine, elegant presentation",
    "sweet_and_sour_pork_cantonese_bing": "food, cantonese cuisine, sweet and sour pork, battered pork, bell peppers, pineapple, vibrant red sauce",
    "wonton_soup": "food, wonton soup, clear broth, pork wontons, bok choy, chinese comfort food",
    "xiaolongbao_soup_dumplings_shanghai_bing": "food, shanghai dumplings, xiaolongbao, soup dumplings, pleated top, bamboo steamer"
}

# Default caption patterns for images not in the map
default_patterns = {
    "bubble_tea": "food, bubble tea, taiwanese drink, boba pearls, milk tea, refreshing beverage",
    "sushi": "food, japanese cuisine, sushi, fresh fish, rice, nori, wasabi, elegant presentation",
    "noodles": "food, asian noodles, savory sauce, fresh ingredients",
    "stir_fry": "food, stir fry dish, wok cooked, fresh vegetables, savory sauce",
    "soup": "food, asian soup, hot broth, fresh ingredients, comfort food",
    "rice": "food, fried rice, wok fried, mixed ingredients, asian cuisine",
    "chicken": "food, chicken dish, asian style, flavorful sauce",
    "beef": "food, beef dish, tender meat, asian preparation",
    "tofu": "food, tofu dish, vegetarian, asian style preparation",
    "curry": "food, curry dish, aromatic spices, rich sauce",
    "dumplings": "food, dumplings, steamed or fried, asian cuisine",
    "dessert": "food, asian dessert, sweet treat"
}

image_dir = "/mnt/c/Users/jcook/git/kohya_ss/train_data/image/1_food"

# Create caption files for each image
for filename in os.listdir(image_dir):
    if filename.endswith(('.jpg', '.png', '.jpeg')):
        base_name = os.path.splitext(filename)[0]
        caption_file = os.path.join(image_dir, base_name + '.txt')
        
        # Check if we have a specific caption for this image
        caption_found = False
        for key, caption in caption_map.items():
            if key in base_name:
                with open(caption_file, 'w') as f:
                    f.write(caption)
                caption_found = True
                break
        
        # If no specific caption, use default patterns
        if not caption_found:
            for pattern, default_caption in default_patterns.items():
                if pattern in base_name.lower():
                    with open(caption_file, 'w') as f:
                        f.write(default_caption)
                    caption_found = True
                    break
        
        # Fallback caption if nothing matches
        if not caption_found:
            caption = base_name.replace('_', ' ')
            caption = ' '.join(caption.split()[:-1]) if caption.split()[-1].isdigit() else caption
            caption = f"food, asian cuisine, {caption}"
            with open(caption_file, 'w') as f:
                f.write(caption)

print(f"Created detailed caption files for images in {image_dir}")