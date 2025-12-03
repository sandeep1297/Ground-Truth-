import os
import base64
import requests
import zipfile

# --- CONFIGURATION (Re-use LLM settings from Phase 2) ---

# OpenRouter API Key
LLM_API_KEY = "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" 
LLM_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"
LLM_MODEL = "google/gemini-2.5-flash" 

OUTPUT_DIR = "output_files"
FINAL_ZIP_FILE = "AI_Creative_Studio_Assets.zip"

# --- HELPER FUNCTIONS ---

def encode_image(image_path):
    """Encodes a local image file to a Base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return None

def generate_caption(image_path, creative_number):
    """Calls the LLM to generate caption/copy based on the visual creative."""
    
    image_b64 = encode_image(image_path)
    if not image_b64:
        return f"Caption generation failed for image {creative_number}."

    SYSTEM_PROMPT = (
        "You are an expert social media copywriter. Analyze the attached image, which is a professional ad creative. "
        "Your task is to write a high-converting, punchy ad copy (1-2 sentences) and generate three relevant, trending hashtags "
        "that motivate a purchase. Output the copy, followed by the hashtags on the next line."
    )

    payload = {
        "model": LLM_MODEL, 
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "text", "text": "Write the ad copy and hashtags for this creative."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_b64}"}},
            ]}
        ],
        "max_tokens": 150,
        "temperature": 0.5
    }

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(LLM_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        print(f"LLM Request Error during caption generation: {e}")
        return f"Caption generation failed due to API error: {e}"
    except KeyError:
        print("LLM Response parsing failed.")
        return "Caption generation failed due to response parsing."

def package_assets():
    """Generates captions, saves them, and zips all creatives."""
    
    print("\nStarting Phase 4: Caption Generation & Packaging...")
    
    files_to_zip = []

    # 1. Loop through all generated images
    for i in range(1, 4): # Assuming creative_1.png, creative_2.png, creative_3.png
        image_name = f"creative_{i}.png"
        image_path = os.path.join(OUTPUT_DIR, image_name)
        
        if os.path.exists(image_path):
            print(f"-> Generating caption for {image_name}...")
            
            # Generate the caption
            caption_text = generate_caption(image_path, i)
            
            # Save the caption to a file
            caption_name = f"caption_{i}.txt"
            caption_path = os.path.join(OUTPUT_DIR, caption_name)
            
            with open(caption_path, "w", encoding="utf-8") as f:
                f.write(caption_text)
            
            print(f"Saved caption to {caption_name}")
            
            # Add both files to the list for zipping
            files_to_zip.append(image_path)
            files_to_zip.append(caption_path)
        else:
            print(f"Warning: Image {image_name} not found. Skipping.")

    # 2. Create the final zip file
    print("\n-> Creating final downloadable ZIP file...")
    try:
        with zipfile.ZipFile(FINAL_ZIP_FILE, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in files_to_zip:
                # Use arcname to make the files appear directly inside the zip, not nested in output_files/
                arcname = os.path.basename(file_path)
                zf.write(file_path, arcname)
        
        print(f"SUCCESS! The final artifact is ready: {FINAL_ZIP_FILE}")
        print("You have completed the H-003 challenge!")

    except Exception as e:
        print(f"Failed to create zip file: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    package_assets()