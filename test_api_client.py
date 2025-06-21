import requests
import json
import base64
from PIL import Image
import io

API_URL = "http://localhost:5000"

def test_api():
    """Test the Chinese Food API"""
    
    print("Testing Chinese Food Generation API")
    print("==================================\n")
    
    # 1. Health check
    print("1. Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"   Status: {response.json()}\n")
    
    # 2. List dishes
    print("2. Getting available dishes...")
    response = requests.get(f"{API_URL}/dishes")
    dishes = response.json()["dishes"]
    print(f"   Found {len(dishes)} dishes")
    for dish in dishes[:5]:  # Show first 5
        print(f"   - {dish['name']} ({dish['id']})")
    print()
    
    # 3. Generate single image
    print("3. Generating har gow image...")
    response = requests.post(
        f"{API_URL}/generate",
        json={"dish": "har_gow", "base64": True}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Generated! Prompt ID: {data['prompt_id']}")
        
        # Save image
        image_data = base64.b64decode(data['image'])
        with open("test_har_gow.png", "wb") as f:
            f.write(image_data)
        print("   Saved as test_har_gow.png\n")
    
    # 4. Custom prompt
    print("4. Testing custom prompt...")
    response = requests.post(
        f"{API_URL}/generate",
        json={
            "prompt": "chinese food, kung pao chicken, extra spicy, sichuan style, close up, white plate",
            "base64": False
        }
    )
    
    if response.status_code == 200:
        with open("test_custom.png", "wb") as f:
            f.write(response.content)
        print("   Saved as test_custom.png\n")
    
    # 5. Batch generation
    print("5. Testing batch generation...")
    response = requests.post(
        f"{API_URL}/generate_batch",
        json={"dishes": ["xiaolongbao", "spring_rolls", "wonton_soup"]}
    )
    print(f"   Batch queued: {response.json()}\n")
    
    print("API test complete!")

if __name__ == "__main__":
    test_api()