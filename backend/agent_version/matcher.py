import json
import re
import os

def load_track_data():
    """
    Load the JSON dataset correctly relative to the script location.
    """
    # Assuming matcher.py is in backend/agent_version/
    # Base dir will be 'SyncRights' folder
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # Adjusted path based on your exact screenshot
    file_path = os.path.join(base_dir, 'data', 'merged_without_suggest.json')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find file at {file_path}")
        return []

def match_version(track_id: str, user_query: str):
    """
    P2 Agent (Day 8 Core Logic): Matches user query to a track version using regex rules.
    NO AI ALLOWED YET.
    """
    dataset = load_track_data()
    
    if not dataset:
         return {"status": "error", "message": "Failed to load database."}

    # 1. Filter out all versions that belong to the given track_id
    track_versions = [item for item in dataset if item.get("track_id") == track_id]
    
    if not track_versions:
        return {"status": "error", "message": f"Track ID '{track_id}' not found in database."}

    query_lower = user_query.lower()

    # 2. Rule-Based Engine (Keyword Mapping)
    rules = {
        "live": "live",
        "concert": "live",
        "session": "live",
        "remix": "remix",
        "mix": "remix",
        "edit": "remix",
        "cover": "cover",
        "acoustic": "cover",
        "unplugged": "cover",
        "remaster": "remaster",
        "remastered": "remaster",
        "original": "original"
    }

    target_type = "original" # Default fallback
    
    # Keyword scanning
    for keyword, v_type in rules.items():
        if re.search(rf'\b{keyword}\b', query_lower):
            target_type = v_type
            break 

    # 3. Try to find the exact version type
    for version in track_versions:
        v_type_db = version.get("version_type", "").lower()
        if target_type == v_type_db:
            return {
                "status": "success",
                "track_id": track_id,
                "matched_version_id": version.get("version_id"),
                "title_label": version.get("title_label"),
                "version_type": version.get("version_type"),
                "confidence": "High (Rule Match)" if target_type != "original" else "Default"
            }

    # 4. Fallback if the requested version type doesn't exist for this track
    # Try to return original, or whatever is first in the list
    original_version = next((v for v in track_versions if v.get("version_type", "").lower() == "original"), track_versions[0])
    
    return {
        "status": "partial_match",
        "track_id": track_id,
        "matched_version_id": original_version.get("version_id"),
        "title_label": original_version.get("title_label"),
        "version_type": original_version.get("version_type"),
        "message": f"Requested type '{target_type}' not available. Defaulting to Original."
    }

# --- TESTING TERMINAL ---
if __name__ == "__main__":
    print("--- Testing P2 Version Matcher ---\n")
    
    # Taking trk_001 from your dataset (Nora Venn - Velvet Comet)
    test_id = "trk_001" 
    
    print("Query: I need the remix version")
    print(match_version(test_id, "I need the remix version"))
    print("-" * 50)
    
    # Taking trk_002 from your dataset (Callum Wren - Paper Lanterns)
    test_id_2 = "trk_002"
    
    print("Query: Can I get the acoustic unplugged one?")
    print(match_version(test_id_2, "Can I get the acoustic unplugged one?"))
    print("-" * 50)
    
    print("Query: Just give me the original")
    print(match_version(test_id, "Just give me the original"))