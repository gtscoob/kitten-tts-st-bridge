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

2. Create and activate a Python 3.11 virtual environment:
   ```bash
   py -3.11 -m venv venv
   .\venv\Scripts\Activate.ps1

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

---

##🎮 Usage

1. Start the Server:
Run the following command in your activated virtual environment:
   ```bash
   python server.py
   
(Note: The server will download the model weights on the very first run. Please be patient!)

2. Web UI Control Panel
   ```bash
   Open your browser and navigate to: http://localhost:5050 to access the testing dashboard.

3. SillyTavern / Amica Integration
   
   To route your character dialogue through the Kitten TTS engine, use the following settings in your frontend:

   Provider: OpenAI Compatible

   API URL: http://127.0.0.1:5050/v1

   API Key: kitten (or any random string)

   Ensure you update your Available Voices list in SillyTavern to exactly: Bella,Jasper,Luna,Bruno,Rosie,Hugo,Kiki,Leo

---


##📝 Punctuation & Pacing Guide
Because Kitten TTS is a lightweight model without manual emotion sliders, it relies entirely on your text formatting to determine pacing and delivery.

   . (Period): Drops the pitch at the end of a thought.

   , (Comma): Adds a short breath or slight pitch rise.

   ? (Question Mark): Forces a natural upward vocal inflection.

   ! (Exclamation): Increases energy, speed, and emphasis.

   ... (Ellipsis): Creates a noticeable hesitation or trailing thought.

   — (Em-dash): Causes an abrupt stop or a sharp interruption.

   ---

  ##📄 License
   Distributed under the MIT License. See LICENSE for more information.



   


