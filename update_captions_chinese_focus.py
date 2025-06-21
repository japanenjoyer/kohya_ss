import os

# Directory with images
image_dir = "/mnt/c/Users/jcook/git/kohya_ss/train_data/10_food"

# Define Chinese dishes and their enhanced captions
chinese_dishes = {
    "beef_and_broccoli": "chinese food, authentic chinese cuisine, beef and broccoli stir fry, wok hei, glossy brown sauce, tender beef slices, fresh green broccoli, chinese takeout classic",
    "char_siu_bao": "chinese food, cantonese dim sum, char siu bao, steamed bbq pork buns, fluffy white dough, sweet bbq pork filling, traditional chinese steamed bun",
    "chicken_chow_mein": "chinese food, cantonese cuisine, chicken chow mein, crispy fried noodles, stir fried vegetables, traditional chinese noodle dish",
    "chinese_cold_sesame_noodles": "chinese food, sichuan cuisine, cold sesame noodles, chinese street food, sesame sauce, julienned vegetables, refreshing chinese dish",
    "chinese_mushroom_chicken_soup": "chinese food, traditional chinese soup, mushroom chicken soup, clear broth, chinese healing soup, shiitake mushrooms",
    "dan_dan_noodles": "chinese food, sichuan cuisine, dan dan mian, spicy chinese noodles, ground pork, chili oil, sichuan peppercorns, authentic chinese street food",
    "dim_sum": "chinese food, cantonese cuisine, dim sum platter, bamboo steamer, traditional chinese brunch, yum cha, cantonese tea house",
    "dumplings": "chinese food, chinese dumplings, jiaozi, potstickers, traditional chinese cuisine, pleated dough, authentic chinese cooking",
    "general_tso": "chinese food, hunan cuisine, general tso chicken, chinese american classic, sweet spicy glaze, crispy fried chicken, chinese restaurant dish",
    "har_gow": "chinese food, cantonese dim sum, har gow, crystal shrimp dumplings, translucent wrapper, traditional chinese dumpling, cantonese technique",
    "kung_pao": "chinese food, sichuan cuisine, kung pao chicken, dried chilies, sichuan peppercorns, peanuts, authentic chinese spicy dish",
    "lo_mai_gai": "chinese food, cantonese dim sum, lo mai gai, lotus leaf sticky rice, traditional chinese wrapped dish, cantonese cuisine",
    "lo_mein": "chinese food, cantonese cuisine, lo mein noodles, soft wheat noodles, chinese stir fry, traditional chinese noodles",
    "mongolian_beef": "chinese food, chinese american cuisine, mongolian beef, tender beef strips, scallions, sweet savory sauce, chinese restaurant classic",
    "orange_chicken": "chinese food, chinese american cuisine, orange chicken, crispy battered chicken, tangy orange glaze, chinese takeout favorite",
    "pot_stickers": "chinese food, chinese dumplings, potstickers, guotie, pan fried dumplings, crispy bottom, traditional chinese appetizer",
    "siu_mai": "chinese food, cantonese dim sum, siu mai, pork shrimp dumplings, open top dumplings, traditional chinese dim sum",
    "spring_rolls": "chinese food, chinese appetizer, spring rolls, crispy fried wrapper, traditional chinese cuisine, golden brown chinese snack",
    "sweet_and_sour_pork": "chinese food, cantonese cuisine, sweet and sour pork, gu lao rou, battered pork, traditional chinese dish",
    "wonton": "chinese food, cantonese cuisine, wontons, chinese dumplings, wonton soup, traditional chinese comfort food",
    "xiaolongbao": "chinese food, shanghai cuisine, xiaolongbao, soup dumplings, traditional chinese delicacy, bamboo steamer, jiangnan cuisine",
    "yangzhou_fried_rice": "chinese food, jiangsu cuisine, yangzhou fried rice, chinese special fried rice, traditional chinese rice dish",
    "chinese_": "chinese food, authentic chinese cuisine, traditional chinese cooking, chinese culinary tradition",
    "sichuan": "chinese food, sichuan cuisine, spicy chinese food, mala flavor, sichuan peppercorns, authentic chinese regional cuisine",
    "cantonese": "chinese food, cantonese cuisine, southern chinese cooking, dim sum tradition, authentic chinese regional cuisine",
    "hunan": "chinese food, hunan cuisine, spicy chinese dishes, authentic chinese regional cooking",
    "shanghai": "chinese food, shanghai cuisine, jiangnan cooking, eastern chinese cuisine"
}

# Non-Chinese dishes to de-emphasize
non_chinese = ["pad_thai", "pho", "sushi", "ramen", "curry", "tikka", "biryani", "tempura", "teriyaki", "kimchi", "galbi", "vietnamese", "thai", "japanese", "korean", "indian"]

# Process each caption file
updated_count = 0
for filename in os.listdir(image_dir):
    if filename.endswith('.txt'):
        filepath = os.path.join(image_dir, filename)
        base_name = filename.replace('.txt', '')
        
        # Check if it's a Chinese dish
        is_chinese = False
        new_caption = None
        
        for chinese_key, chinese_caption in chinese_dishes.items():
            if chinese_key in base_name.lower():
                is_chinese = True
                new_caption = chinese_caption
                break
        
        # If not specifically Chinese but still Asian, add chinese influence
        if not is_chinese:
            is_non_chinese = any(non_chinese_term in base_name.lower() for non_chinese_term in non_chinese)
            
            if not is_non_chinese and "asian" in base_name.lower():
                # Generic Asian dish - emphasize Chinese influence
                with open(filepath, 'r') as f:
                    old_caption = f.read()
                new_caption = old_caption.replace("food,", "chinese food, chinese influenced,")
            elif not is_non_chinese:
                # Could be Chinese - check current caption
                with open(filepath, 'r') as f:
                    old_caption = f.read()
                if "chinese" not in old_caption.lower():
                    new_caption = old_caption.replace("food,", "chinese food, chinese style,")
        
        # Write updated caption if we have one
        if new_caption:
            with open(filepath, 'w') as f:
                f.write(new_caption)
            updated_count += 1
            print(f"Updated: {base_name}")

print(f"\nTotal captions updated: {updated_count}")
print("\nRecommendations:")
print("1. Use 'chinese food' as your trigger phrase instead of just 'food'")
print("2. Consider removing or reducing weight of non-Chinese dishes")
print("3. You may want to train for 4-5 epochs for stronger style learning")