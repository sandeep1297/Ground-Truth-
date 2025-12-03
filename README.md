# 🚀 H-003 | AI Creative Studio: Auto-Creative Engine  
### Hackathon Challenge – Generative AI & Marketing Tech

The **AI Creative Studio** is an automated Python-based pipeline that transforms a single product image and brand logo into multiple high-quality, branded marketing creatives.  
It eliminates manual design effort using multimodal analysis, intelligent prompt engineering, SDXL image generation, and AI-powered captioning.

---

## ✨ Key Features

### 🔍 Multimodal Product & Logo Analysis  
- Uses an advanced LLM (Gemini 2.5 Flash / Mixtral 8x7B)  
- Detects brand colors, product style, key visual elements  
- Extracts brand identity for prompt-generation  

### 🎨 Intelligent Prompt Engineering  
Automatically generates **three high-quality creative prompts** in unique themes:
- Cinematic  
- Cyberpunk  
- Minimalist  
(or other dynamically generated themes)

### 🖼️ High-Resolution Image Generation  
- Uses **Stable Diffusion XL (SDXL)**  
- Creates **3 image creatives (1024×1024)**  
- Generates clean, commercial-ready marketing visuals  

### ✍️ AI Copywriting  
- Generates catchy captions for each creative  
- Provides trending hashtags  
- Tailored to the image theme + product context  

### 📦 Automated Packaging  
Produces a single downloadable artifact:  
```
AI_Creative_Studio_Assets.zip
```
Which includes:
- All 3 generated creatives  
- Captions for each image  
- Original input + generated prompts  

---

## 🛠️ Technical Stack

| Role | Technology | Model / Service | Access |
|------|------------|------------------|---------|
| Project Language | Python 3 | — | — |
| LLM (multimodal analysis & captions) | Mixtral 8x7B / Gemini 2.5 Flash | OpenRouter | OpenAI-compatible endpoint |
| Image Generation | Stable Diffusion XL | Stability AI (DreamStudio) | REST API |
| Libraries | requests, Pillow, zipfile | — | Local |

---

## 📂 Directory Structure

```
project_root/
│
├── analyze_and_prompt.py
├── generate_images.py
├── finalize_creatives.py
│
├── input_files/
│   ├── product.jpg
│   └── logo.jpeg
│
├── output_files/
│   ├── creative_1.png
│   ├── creative_2.png
│   └── creative_3.png
│
├── generated_image_prompts.txt
└── AI_Creative_Studio_Assets.zip
```

---

## ⚙️ Setup & Installation

### **1. Clone the Repository**
```bash
git clone [YOUR_GITHUB_REPO_URL]
cd [YOUR_REPO_NAME]
```

### **2. Create & Activate Virtual Environment (Windows)**
```bash
python -m venv H003
.H003\Scriptsctivate
```

### **3. Install Dependencies**
```bash
pip install requests pillow
```

### **4. Add Input Files**

Create a folder:
```
input_files/
```

Place your files:
```
input_files/product.jpg
input_files/logo.jpeg
```

### **5. Configure API Keys**

Replace placeholders inside the scripts:
```
OPENROUTER_API_KEY = "YOUR_KEY"
STABILITY_API_KEY = "YOUR_KEY"
```
Or set environment variables in the terminal.

---

## ▶️ Execution Pipeline

### **Phase 1: Multimodal Analysis**
```bash
python analyze_and_prompt.py
```
- Generates brand analysis  
- Writes 3 creative prompts to:
```
generated_image_prompts.txt
```

---

### **Phase 2: Image Generation**
```bash
python generate_images.py
```
Creates:
- `creative_1.png`
- `creative_2.png`
- `creative_3.png`

Stored in:
```
output_files/
```

---

### **Phase 3: Captioning & Packaging**
```bash
python finalize_creatives.py
```

Outputs:
```
AI_Creative_Studio_Assets.zip
```

---

## 🔮 Future Enhancements

- **Web UI (Flask/React)**  
  Drag-drop interface for uploads instead of file paths  
- **Brand Consistency Engine**  
  Automatic detection of brand hex codes + font family  
- **ControlNet / Image-to-Image**  
  Guarantee logo placement inside generated creatives  
- **Batch-Mode Support**  
  Generate creatives for multiple products at once  

---

## 🏁 Conclusion

The **AI Creative Studio** delivers a fully-automated, production-ready creative generation pipeline for marketing teams, brands, and e-commerce applications.

Start generating stunning AI creatives from a single product image instantly!
