import os
import base64
import requests
from PIL import Image

# --- 1. CONFIGURATION ---

# OpenRouter API Key
LLM_API_KEY = "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" 

# OpenRouter's standard Chat Completions endpoint 
LLM_ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

# --- 2. HELPER FUNCTION: ENCODE IMAGE TO BASE64 ---
def encode_image(image_path):
    """Encodes a local image file to a Base64 string for API payload."""
    try:
        if not os.path.exists(image_path):
             print(f"Error: Image file not found at {image_path}. Please check the path and file name.")
             return None
             
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"An error occurred while encoding {image_path}: {e}")
        return None

# --- 3. EXECUTION ---
if __name__ == "__main__":
    print("Starting Multimodal Analysis (Phase 2)...")

    # Define file paths
    PRODUCT_PATH = "input_files/product.jpg"
    LOGO_PATH = "input_files/logo.jpeg"

    # Encode images
    product_b64 = encode_image(PRODUCT_PATH)
    logo_b64 = encode_image(LOGO_PATH)

    if not product_b64 or not logo_b64:
        print("Exiting due to missing input files.")
        exit()

    # --- 4. CONSTRUCT THE MULTIMODAL PROMPT ---
    SYSTEM_PROMPT = (
        "You are an expert marketing prompt engineer. Your task is to analyze the product and brand logo in the two "
        "images provided. Then, generate three unique, creative, and professional image prompts suitable for a "
        "high-quality text-to-image model like Stable Diffusion XL. Incorporate the product, the brand colors, and "
        "a specific style (e.g., cinematic, minimalist, cyberpunk) into each prompt. "
        "The output MUST be ONLY the three image prompts, separated by a unique delimiter: '---'."
    )

    # Payload for the LLM API call
    payload = {
        "model": "google/gemini-2.5-flash", 
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": [
                # Text instruction
                {"type": "text", "text": "Image 1 is the product, Image 2 is the logo. Analyze and generate the 3 prompts."},
                # Image 1 (Product)
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{product_b64}"}},
                # Image 2 (Logo)
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{logo_b64}"}},
            ]}
        ],
        "max_tokens": 512,
        "temperature": 0.8
    }

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    # --- 5. MAKE THE API CALL ---
    try:
        print(f"Sending request to LLM endpoint: {LLM_ENDPOINT}...")
        response = requests.post(LLM_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        
        # OpenRouter/OpenAI API response structure:
        raw_prompts = data['choices'][0]['message']['content']

        # --- 6. PROCESS AND SAVE PROMPTS ---
        generated_prompts = [p.strip() for p in raw_prompts.split('---') if p.strip()]

        print("\nSuccessfully generated the following image prompts:")
        for i, prompt in enumerate(generated_prompts):
            print(f"  Prompt {i+1}: {prompt}")

        # Save prompts to a file for use in Phase 3
        with open("generated_image_prompts.txt", "w", encoding="utf-8") as f:
            f.write('\n---\n'.join(generated_prompts))
        
        print("\nSaved prompts to 'generated_image_prompts.txt'")

    except requests.exceptions.RequestException as e:
        print(f"\nAPI Request Error: {e}")
        print("Possible issues: API Key invalid, endpoint is wrong, or insufficient credits.")
    except KeyError:
        print("\nFailed to parse response from LLM host. Check the JSON structure.")
        print("Raw response:", response.text)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")