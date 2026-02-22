# Kitten TTS 0.8 - SillyTavern & Amica Bridge

A lightweight, local Python web server that wraps the Kitten TTS 0.8 Mini model into an OpenAI-compatible API endpoint. Designed specifically for seamless text-to-speech integration with AI roleplay frontends like **SillyTavern** and **Amica**. 

Includes a built-in browser UI for testing voices, adjusting playback speed, and downloading offline `.wav` files.

## ✨ Features
* **🪶 Ultra-Lightweight:** Runs entirely on your CPU. No dedicated GPU required.
* **🔌 Plug-and-Play:** Mimics the OpenAI API structure, meaning no custom extensions are needed for SillyTavern or Amica to connect.
* **🗣️ Expressive Personas:** Supports the 8 natively tuned Kitten TTS 0.8 voices (Bella, Jasper, Luna, Bruno, Rosie, Hugo, Kiki, Leo).
* **💻 Standalone Web UI:** Test prompts, adjust playback speed natively in the browser, and download generated audio directly to your machine.

---

## 🛠️ Prerequisites
* **Python 3.11** (Kitten TTS dependencies are currently incompatible with Python 3.12/3.13).
* A free **Hugging Face Access Token** (Required to download the model weights without hitting rate limits).

---

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/gtscoob/kitten-tts-st-bridge.git](https://github.com/gtscoob/kitten-tts-st-bridge.git)
   cd kitten-tts-st-bridge