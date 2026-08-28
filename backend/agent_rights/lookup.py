import json
import os

def get_rights_data(version_id: str):
    """
    Day 8 P3 Agent: Rights lookup function.
    Takes a version_id and returns the specific rights record.
    """
    # Navigating up to the 'data' folder
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(base_dir, 'data', 'merged_without_suggest.json')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
    except FileNotFoundError:
        return {"status": "error", "message": "Dataset not found."}

    # Find the exact version and its rights
    for item in dataset:
        if item.get("version_id") == version_id:
            return {
                "status": "success",
                "version_id": version_id,
                "title": item.get("title"),
                "master_rights": item.get("master_rights"),
                "publishing_rights": item.get("publishing_rights"),
                "usage_types_allowed": item.get("usage_types_allowed"),
                "commercial_use": item.get("commercial_use")
            }
            
    return {"status": "error", "message": f"Rights for version '{version_id}' not found."}

# --- DAY 10 STRESS TEST FOR P3 ---
if __name__ == "__main__":
    print("--- Day 10: Running 10-Query Stress Test (Rights Lookup) ---")
    
    # 10 Diverse Version IDs from the dataset (including one fake one to test error handling)
    test_version_ids = [
        "ver_001_c",  # Remix
        "ver_002_a",  # Original
        "ver_015_b",  # Remastered
        "ver_021_c",  # Cyber Remix
        "ver_040_a",  # Original Studio
        "ver_050_c",  # Acoustic Cover
        "ver_066_b",  # Saffron Echoes Remaster
        "ver_077_a",  # Cybernetic Tabla
        "ver_080_c",  # Live Festival Edition
        "ver_999_invalid" # FAKE ID to test error handling
    ]
    
    for i, v_id in enumerate(test_version_ids, 1):
        print(f"\n[{i}/10] Fetching rights for version_id: '{v_id}'")
        result = get_rights_data(v_id)
        
        if result.get("status") == "success":
            print(f"-> SUCCESS: Found rights for '{result.get('title')}'")
            print(f"   Master: {result.get('master_rights')} | Publishing: {result.get('publishing_rights')}")
            print(f"   Allowed Usage: {', '.join(result.get('usage_types_allowed', []))}")
        else:
            print(f"-> ERROR: {result.get('message')}")