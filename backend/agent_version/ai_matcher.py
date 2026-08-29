import json
import os
from google import genai
from dotenv import load_dotenv

# 1. API Key Load Kar
load_dotenv()

# Naya SDK automatically .env se GEMINI_API_KEY utha leta hai
client = genai.Client()

def load_track_versions(track_id: str):
    """Loads versions for a specific track from your JSON data."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(base_dir, 'data', 'merged_without_suggest.json')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
            return [item for item in dataset if item.get("track_id") == track_id]
    except FileNotFoundError:
        print(f"Error: Could not find file at {file_path}")
        return []

def match_version_with_ai(track_id: str, user_query: str):
    """
    Day 9 P2 Agent: Uses Gemini to disambiguate version references.
    """
    versions = load_track_versions(track_id)
    
    if not versions:
        return {"status": "error", "message": f"Track ID '{track_id}' not found."}

    # Clean list of available versions to send to Gemini
    available_options = [
        {
            "version_id": v.get("version_id"), 
            "title_label": v.get("title_label"), 
            "version_type": v.get("version_type"),
            "artist_label": v.get("artist_label")
        } 
        for v in versions
    ]

    # 2. Smart Prompt Engineering
    prompt = f"""
    You are an intelligent music rights version-matching agent.
    A user is looking for a specific version of a track based on their natural language query.
    
    User Query: "{user_query}"
    
    Available Versions for this track:
    {json.dumps(available_options, indent=2)}
    
    Task: 
    1. Analyze the user's query and match it to the best available version. 
    2. For example, if they say "the new remaster", find the version_type 'remaster'.
    3. CRITICAL VIBE MAPPING RULES:
       - If the user asks for "fast", "upbeat", "energetic", "dance", or "club" -> Strictly prioritize versions labeled as 'remix'.
       - If the user asks for "slow", "quiet", "raw", "unplugged", or "chill" -> Strictly prioritize versions labeled as 'acoustic'.
       - If the user asks for "better quality", "crisp", or "modern" -> Strictly prioritize 'remaster'.
       - Do not default to the original version if a vibe keyword strongly suggests an alternative.
    4. If the query is completely ambiguous and lacks any vibe keywords, only then default to the 'original' version_type.
    
    Respond ONLY with a valid JSON object in exactly this format (do not include markdown tags like ```json):
    {{
        "matched_version_id": "the exact version_id string",
        "confidence": "High/Medium/Low",
        "reasoning": "A 1-sentence explanation of why you chose this version"
    }}
    """

    try:
        # 3. Call Gemini using the NEW SDK
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Parse the JSON response
        clean_text = response.text.strip()
        if clean_text.startswith('```json'):
            clean_text = clean_text[7:-3].strip()
        elif clean_text.startswith('```'):
            clean_text = clean_text[3:-3].strip()
            
        ai_decision = json.loads(clean_text)
        
        # 4. Fetch the full version data based on AI's choice
        matched_ver = next((v for v in versions if v["version_id"] == ai_decision.get("matched_version_id")), versions[0])
        
        return {
            "status": "success",
            "track_id": track_id,
            "matched_version_id": matched_ver["version_id"],
            "title_label": matched_ver["title_label"],
            "version_type": matched_ver["version_type"],
            "ai_confidence": ai_decision.get("confidence"),
            "ai_reasoning": ai_decision.get("reasoning")
        }
        
    except Exception as e:
        return {"status": "error", "message": f"Gemini failed: {str(e)}"}

# --- DAY 10 STRESS TEST ---
if __name__ == "__main__":
    print("--- Day 10: Running 10-Query Stress Test ---")
    
    test_id = "trk_001" # Velvet Comet by Nora Venn
    
    # 10 Tricky and Diverse Queries
    test_queries = [
        "give me the remix", # Direct
        "i need the 2022 version", # Date inference (should find Remaster)
        "do you have the dj solace track?", # Artist label inference (should find Remix)
        "just the normal original song", # Exact Original
        "the night drive one", # Title inference
        "i want the acoustic cover", # Doesn't exist (should fallback to original)
        "remastered pls", # Keyword match
        "the newest one", # Logical inference
        "can i use the club mix?", # Synonym for remix
        "Velvet Comet original studio" # Exact title match
    ]
    
    import time
    for i, q in enumerate(test_queries, 1):
        print(f"\n[{i}/10] Query: '{q}'")
        result = match_version_with_ai(test_id, q)
        print(f"-> Selected: {result.get('title_label', 'ERROR')} (Confidence: {result.get('ai_confidence', 'N/A')})")
        print(f"-> Reasoning: {result.get('ai_reasoning', result.get('message', 'N/A'))}")
        time.sleep(15) # Adding a 15-sec delay to avoid hitting Gemini API rate limits