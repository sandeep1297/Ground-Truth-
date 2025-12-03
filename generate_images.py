import os
import requests
import base64
from io import BytesIO

# --- 1. CONFIGURATION ---

# Stability AI Key
IMAGE_API_KEY = "sk-NKAhYXRTz3g9HtSbbMj2O2BElW3WPxRmVeplRP592gM832Ag" 

# Stability AI Endpoint for Stable Diffusion XL
IMAGE_ENDPOINT = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
OUTPUT_DIR = "output_files"

def generate_images_from_prompts(prompts):
    """Generates images using the Stability AI API based on a list of prompts."""
    
    # 1. Setup Request Headers
    headers = {
        "Authorization": f"Bearer {IMAGE_API_KEY}",
        "Accept": "application/json"
    }

    print("\nStarting Phase 3: Generating Image Creatives...")
    
    # 2. Loop through the generated prompts
    for i, prompt in enumerate(prompts):
        print(f"\n-> Generating Image {i+1} with prompt: {prompt[:70]}...")

        # 3. Construct the Payload
        data = {
            "text_prompts": [
                {"text": prompt, "weight": 1.0},
                # Add a general negative prompt for quality improvement
                {"text": "blurry, duplicate, ugly, low quality, bad hands, bad anatomy, deformed, signature, watermark", "weight": -1.0}
            ],
            # Standard settings for high-quality SDXL generation:
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30
        }

        # 4. Make the API Call
        try:
            response = requests.post(
                IMAGE_ENDPOINT,
                headers=headers,
                json=data
            )
            response.raise_for_status() # Check for errors

            response_data = response.json()

            # 5. Process and Save the Image
            # The API returns a list of artifacts (images)
            for j, artifact in enumerate(response_data.get("artifacts", [])):
                if artifact["finishReason"] == "SUCCESS":
                    # Decode the Base64 image data
                    image_bytes = base64.b64decode(artifact["base64"])
                    
                    # Create image file name (using the loop index for naming)
                    file_path = os.path.join(OUTPUT_DIR, f"creative_{i+1}.png")
                    
                    # Write the binary data to a file
                    with open(file_path, "wb") as f:
                        f.write(image_bytes)
                    
                    print(f"Saved creative to {file_path}")
                else:
                    print(f"Generation failed for Image {i+1}. Reason: {artifact.get('finishReason', 'Unknown')}")

        except requests.exceptions.RequestException as e:
            print(f"\nImage API Request Error: {e}")
            print("Possible issues: API Key invalid or expired, or insufficient credits.")
            # Break the loop if a critical API error occurs
            return 
        except Exception as e:
            print(f"\nAn unexpected error occurred during image processing: {e}")
            # Break the loop on other critical errors
            return

# --- INTEGRATE WITH PREVIOUS PHASE ---

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    prompts_file = "generated_image_prompts.txt"
    try:
        # 1. Load Prompts from the file generated in Phase 2
        with open(prompts_file, "r", encoding="utf-8") as f:
            # Read and split by the delimiter '---'
            all_prompts = [p.strip() for p in f.read().split('---') if p.strip()]
        
        if not all_prompts:
            print(f"Error: {prompts_file} is empty. Ensure Phase 2 ran correctly.")
            exit()
            
        # 2. Start Image Generation
        generate_images_from_prompts(all_prompts)
        
    except FileNotFoundError:
        print(f"Error: {prompts_file} not found. Please run Phase 2 first to create this file.")
        exit()
    
    # Next step after image generation is Phase 4
    print("\n---")
    print("Phase 3 Complete.")
    print(f"Check the '{OUTPUT_DIR}' folder for your three image creatives.")
    print("Next: Phase 4 (Caption Generation & Packaging).")