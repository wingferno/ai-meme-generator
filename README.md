# 🤖 AI Meme Generator 😂

> An AI-powered meme generator that creates 3 fitting memes (jpg images) for a given prompt using the Gemini 2.5 Flash model 

## 📋 Table of Contents

- [Installation](#-installation)
- [Setup](#-setup)
- [Usage](#-usage)
- [Features](#-features)
- [Requirements](#-requirements)
- [Contributing](#-contributing)

## 🚀 Installation

Install all required dependencies with a single command:

```bash
pip install google-generativeai python-dotenv pillow
```

### 📦 What gets installed:

| Package | Purpose |
|---------|---------|
| `google-generativeai` | Google's Generative AI library for AI text/image generation |
| `python-dotenv` | Load environment variables from .env files |
| `pillow` | Python Imaging Library for image processing and manipulation |


## ⚙️ Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/wingferno/ai-meme-generator.git
   cd ai-meme-generator
   ```

2. **Install dependencies**
   ```bash
   pip install google-generativeai python-dotenv pillow
   ```
3. **Add your API key**
   
   Open `.env` and add your Google api key:
   ```env
   MY_API_KEY=your_api_key_here
   ```

3. **Run the meme generator**
   ```bash
   python meme_generator.py
   ```

## 🎮 Usage

```bash
python meme_generator.py
```

## 📋 Requirements

- ![Python](https://img.shields.io/badge/Python-3.6+-blue) or higher
- 🔑 Google AI API key ([Get yours here](https://ai.google.dev/))
- 🌐 Internet connection for AI generation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

