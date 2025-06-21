import os
import json

# Enhanced appetizing descriptions for Chinese dishes
appetizing_descriptions = {
    # Dumplings & Dim Sum
    "har_gow": {
        "name": "Crystal Shrimp Dumplings",
        "description": "chinese food, har gow, translucent crystal skin dumplings, plump pink shrimp visible through delicate wrapper, perfect pleated edges, glistening with steam, bamboo steamer, 4 pristine pieces, dim sum perfection, juicy succulent filling, restaurant quality, white tablecloth background",
        "tags": ["steamed", "delicate", "translucent", "juicy", "pristine"]
    },
    "xiaolongbao": {
        "name": "Soup Dumplings", 
        "description": "chinese food, xiaolongbao, delicate soup dumplings, thin translucent skin holding rich broth, 18 precise pleats on top, bamboo steamer lined with cabbage, steam rising, golden chicken broth visible, tender pork filling, shanghai delicacy, white marble table",
        "tags": ["soup-filled", "delicate", "steaming", "juicy", "perfect pleats"]
    },
    "siu_mai": {
        "name": "Pork & Shrimp Shumai",
        "description": "chinese food, siu mai, golden topped dumplings, juicy pork and shrimp filling, orange crab roe garnish, open-faced beauty, bamboo steamer, glistening with savory juices, perfect yellow wrapper, dim sum classic, restaurant presentation",
        "tags": ["open-topped", "juicy", "golden", "savory", "garnished"]
    },
    "char_siu_bao": {
        "name": "BBQ Pork Buns",
        "description": "chinese food, char siu bao, fluffy white steamed buns, split open revealing glossy red bbq pork, honey-glazed char siu filling, pillowy soft dough, steam wisps, bamboo steamer, 3 perfect buns, sweet and savory, white background",
        "tags": ["fluffy", "glazed", "sweet-savory", "pillowy", "steamed"]
    },
    
    # Noodle Dishes
    "dan_dan_noodles": {
        "name": "Sichuan Dan Dan Noodles",
        "description": "chinese food, dan dan noodles, silky wheat noodles, rich red chili oil pooling, savory minced pork, crushed peanuts, vibrant green scallions, sesame paste coating, aromatic sichuan peppercorns, white ceramic bowl, appetizing presentation",
        "tags": ["spicy", "silky", "aromatic", "rich", "vibrant"]
    },
    "lo_mein": {
        "name": "Cantonese Lo Mein",
        "description": "chinese food, lo mein, glossy egg noodles, wok-charred edges, colorful crisp vegetables, tender chicken slices, rich brown sauce coating, bean sprouts, scallions, steam rising, white plate, restaurant style",
        "tags": ["glossy", "wok-charred", "colorful", "tender", "savory"]
    },
    
    # Chicken Dishes
    "kung_pao": {
        "name": "Kung Pao Chicken",
        "description": "chinese food, kung pao chicken, glistening cubed chicken, vibrant dried red chilies, roasted peanuts, glossy soy glaze, fresh scallions, sichuan peppercorns visible, rich mahogany sauce, white porcelain plate, steam rising, restaurant quality",
        "tags": ["spicy", "glistening", "nutty", "aromatic", "glossy"]
    },
    "general_tso": {
        "name": "General Tso's Chicken",
        "description": "chinese food, general tso chicken, crispy golden battered chicken, thick glossy sweet-spicy glaze, sesame seed garnish, bright broccoli florets, caramelized edges, steam rising, white rice side, elegant plating, restaurant presentation",
        "tags": ["crispy", "glazed", "caramelized", "sweet-spicy", "golden"]
    },
    "orange_chicken": {
        "name": "Orange Chicken",
        "description": "chinese food, orange chicken, crispy battered chicken pieces, bright orange citrus glaze, fresh orange zest, caramelized coating, green onion garnish, glistening sauce, white serving plate, vibrant colors, appetizing presentation",
        "tags": ["citrusy", "crispy", "bright", "caramelized", "zesty"]
    },
    "lemon_chicken": {
        "name": "Cantonese Lemon Chicken",
        "description": "chinese food, lemon chicken, golden crispy chicken breast, bright yellow lemon sauce, fresh lemon slices, light cornstarch coating, glossy citrus glaze, garnished with parsley, white plate, elegant presentation, cantonese style",
        "tags": ["crispy", "citrus", "golden", "light", "bright"]
    },
    
    # Beef Dishes
    "mongolian_beef": {
        "name": "Mongolian Beef",
        "description": "chinese food, mongolian beef, tender beef strips, rich dark sauce, caramelized onions, fresh green scallions, glossy soy glaze, slight char, aromatic steam, white plate, restaurant quality, appetizing colors",
        "tags": ["tender", "caramelized", "rich", "glossy", "aromatic"]
    },
    "beef_and_broccoli": {
        "name": "Beef & Broccoli",
        "description": "chinese food, beef and broccoli, tender marinated beef slices, bright green broccoli florets, rich brown oyster sauce, glossy coating, sesame oil sheen, steam rising, white rice accompaniment, classic presentation",
        "tags": ["tender", "fresh", "glossy", "classic", "vibrant"]
    },
    
    # Rice & Fried Dishes
    "yangzhou_fried_rice": {
        "name": "Yangzhou Fried Rice",
        "description": "chinese food, yangzhou fried rice, golden egg-coated rice, colorful diced char siu, plump shrimp, bright green peas, fluffy separated grains, wok hei aroma, garnished with scallions, white plate, restaurant style",
        "tags": ["fluffy", "colorful", "wok-fried", "golden", "aromatic"]
    },
    "spring_rolls": {
        "name": "Crispy Spring Rolls",
        "description": "chinese food, spring rolls, golden crispy wrapper, shatteringly crunchy, diagonal cut showing colorful vegetable filling, sweet chili sauce, fresh lettuce garnish, grease-free, perfectly fried, white plate presentation",
        "tags": ["crispy", "golden", "crunchy", "fresh", "perfect"]
    },
    
    # Seafood
    "honey_walnut_shrimp": {
        "name": "Honey Walnut Shrimp",
        "description": "chinese food, honey walnut shrimp, plump crispy shrimp, creamy white sauce, candied walnuts, golden tempura coating, sweet mayo glaze, garnished with sesame seeds, elegant plating, restaurant quality",
        "tags": ["crispy", "creamy", "sweet", "plump", "candied"]
    },
    
    # Soups
    "wonton_soup": {
        "name": "Wonton Soup",
        "description": "chinese food, wonton soup, clear golden broth, plump pork wontons, fresh bok choy, sliced scallions, sesame oil drops, steam rising, white ceramic bowl, comforting warmth, traditional presentation",
        "tags": ["clear", "comforting", "fresh", "aromatic", "traditional"]
    },
    
    # Desserts & Drinks
    "egg_tart": {
        "name": "Chinese Egg Tarts",
        "description": "chinese food, egg tarts, golden flaky pastry, silky smooth custard, perfectly caramelized top, delicate layers visible, 4 tarts on white plate, bakery fresh, portuguese-chinese fusion, appetizing golden color",
        "tags": ["flaky", "silky", "golden", "delicate", "caramelized"]
    },
    "bubble_tea": {
        "name": "Brown Sugar Bubble Tea",
        "description": "chinese food, bubble tea, creamy milk tea, dark brown sugar syrup swirls, black tapioca pearls, condensation on glass, wide straw, marble pattern, fresh and cold, taiwanese style, white background",
        "tags": ["creamy", "sweet", "fresh", "cold", "marbled"]
    }
}

def enhance_all_captions():
    """Enhance all caption files in the training directory"""
    image_dir = "/mnt/c/Users/jcook/git/kohya_ss/train_data/10_food"
    enhanced_count = 0
    
    # Create backup directory
    backup_dir = "/mnt/c/Users/jcook/git/kohya_ss/train_data/10_food_backup"
    os.makedirs(backup_dir, exist_ok=True)
    
    for filename in os.listdir(image_dir):
        if filename.endswith('.txt'):
            filepath = os.path.join(image_dir, filename)
            base_name = filename.replace('.txt', '').replace('.jpg', '')
            
            # Find matching description
            enhanced_caption = None
            for key, data in appetizing_descriptions.items():
                if key in base_name.lower():
                    enhanced_caption = data["description"]
                    break
            
            # If no specific match, try generic enhancement
            if not enhanced_caption:
                # Read current caption
                with open(filepath, 'r') as f:
                    current = f.read()
                
                # Generic enhancements
                if "chinese" in base_name.lower():
                    additions = ", glistening, appetizing, fresh ingredients, restaurant quality, professional food photography, steam rising, perfect plating, white background"
                    enhanced_caption = current.rstrip() + additions
            
            if enhanced_caption:
                # Backup original
                backup_path = os.path.join(backup_dir, filename)
                with open(filepath, 'r') as f:
                    original = f.read()
                with open(backup_path, 'w') as f:
                    f.write(original)
                
                # Write enhanced caption
                with open(filepath, 'w') as f:
                    f.write(enhanced_caption)
                enhanced_count += 1
                print(f"Enhanced: {base_name}")
    
    print(f"\nTotal enhanced: {enhanced_count} captions")
    print(f"Backups saved to: {backup_dir}")
    return enhanced_count

# Create a JSON file with all enhanced descriptions for reference
def save_descriptions_json():
    with open('appetizing_descriptions.json', 'w') as f:
        json.dump(appetizing_descriptions, f, indent=2)
    print("Saved appetizing descriptions to appetizing_descriptions.json")

if __name__ == "__main__":
    print("Enhancing Chinese Food Captions")
    print("===============================")
    print("Making all dishes sound delicious and appetizing...")
    print()
    
    save_descriptions_json()
    enhance_all_captions()
    
    print("\nEnhancement complete!")
    print("Your captions now include:")
    print("- Appetizing visual descriptions")
    print("- Texture and appearance details")
    print("- Professional photography terms")
    print("- Consistent white/restaurant backgrounds")
    print("\nReady for retraining with enhanced dataset!")