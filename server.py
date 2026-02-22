import io, soundfile as sf, uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from kittentts import KittenTTS

app = FastAPI()
tts = KittenTTS("KittenML/kitten-tts-mini-0.8")

AVAILABLE_VOICES = ["Bella", "Jasper", "Luna", "Bruno", "Rosie", "Hugo", "Kiki", "Leo"]

class Req(BaseModel):
    input: str
    voice: str = "Jasper"

@app.post("/v1/audio/speech")
@app.post("/audio/speech")
@app.post("/")
async def speech(r: Req):
    target_voice = r.voice if r.voice in AVAILABLE_VOICES else "Jasper"
    audio = tts.generate(r.input, voice=target_voice)
    buf = io.BytesIO()
    sf.write(buf, audio, 22050, format='WAV')
    buf.seek(0)
    return Response(content=buf.read(), media_type="audio/wav")

@app.get("/", response_class=HTMLResponse)
async def ui():
    voice_options = "".join([f'<option value="{v}">{v}</option>' for v in AVAILABLE_VOICES])
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kitten TTS Control Panel</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 650px; margin: 40px auto; padding: 25px; background: #121212; color: #eee; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
            h2 {{ color: #fff; text-align: center; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 15px; }}
            label {{ display: block; margin-top: 15px; font-weight: 600; color: #bbb; }}
            textarea, select, button, input[type="range"] {{ width: 100%; margin-top: 8px; padding: 12px; box-sizing: border-box; background: #222; color: #fff; border: 1px solid #444; border-radius: 6px; font-size: 15px; transition: border 0.3s; }}
            textarea:focus, select:focus {{ outline: none; border-color: #007bff; }}
            textarea {{ resize: vertical; }}
            
            /* Guide Panel Styles */
            details.guide-panel {{ background: #1a1a1a; padding: 12px 15px; border-radius: 6px; margin-top: 10px; border: 1px solid #333; font-size: 14px; }}
            details.guide-panel summary {{ font-weight: bold; cursor: pointer; color: #007bff; outline: none; }}
            details.guide-panel summary:hover {{ color: #3399ff; }}
            details.guide-panel ul {{ margin-top: 10px; margin-bottom: 0; padding-left: 20px; color: #bbb; line-height: 1.6; }}
            details.guide-panel li strong {{ color: #fff; }}

            .btn-group {{ display: flex; gap: 10px; margin-top: 20px; }}
            button {{ flex: 1; background: #007bff; cursor: pointer; border: none; font-weight: bold; transition: background 0.2s; }}
            button:hover {{ background: #0056b3; }}
            button:disabled {{ background: #444; color: #888; cursor: not-allowed; }}
            #downloadBtn {{ background: #28a745; display: none; }}
            #downloadBtn:hover {{ background: #218838; }}
            
            .settings-panel {{ background: #1a1a1a; padding: 15px; border-radius: 6px; margin-top: 20px; border: 1px solid #333; }}
            .setting-row {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
            .setting-row:last-child {{ margin-bottom: 0; }}
            input[type="checkbox"] {{ transform: scale(1.2); margin-right: 10px; accent-color: #007bff; }}
            audio {{ width: 100%; margin-top: 25px; outline: none; border-radius: 6px; }}
            .status {{ text-align: center; margin-top: 15px; font-size: 14px; color: #888; min-height: 20px; }}
        </style>
    </head>
    <body>
        <h2>Kitten TTS 0.8 Engine</h2>
        
        <label for="text">Text to Speech:</label>
        <textarea id="text" rows="5">I... I didn't mean to do that! Wait, are you sure it's broken?</textarea>
        
        <details class="guide-panel">
            <summary>Punctuation & Pacing Guide</summary>
            <ul>
                <li><strong>. (Period):</strong> Creates a full stop and drops the pitch at the end of a thought.</li>
                <li><strong>, (Comma):</strong> Adds a short breath or slight pitch rise to break up long sentences.</li>
                <li><strong>? (Question Mark):</strong> Forces a natural upward vocal inflection at the end of the sentence.</li>
                <li><strong>! (Exclamation):</strong> Increases the energy, speed, and emphasis of the delivery.</li>
                <li><strong>... (Ellipsis):</strong> Creates a noticeable hesitation or trailing thought. Great for nervous or thoughtful dialogue.</li>
                <li><strong>— (Em-dash):</strong> Causes an abrupt stop or a sharp interruption in the flow of speech.</li>
                <li><strong>ALL CAPS:</strong> Many models will slightly increase volume or stress on fully capitalized words.</li>
            </ul>
        </details>
        
        <label for="voice">Select Voice:</label>
        <select id="voice">
            {voice_options}
        </select>
        
        <div class="settings-panel">
            <div class="setting-row">
                <label style="margin: 0; display: flex; align-items: center;">
                    <input type="checkbox" id="autoPlay" checked> Auto-play generated audio
                </label>
            </div>
            <div class="setting-row" style="flex-direction: column; align-items: flex-start;">
                <label style="margin: 10px 0 5px 0;">Playback Speed: <span id="speedValue">1.0x</span></label>
                <input type="range" id="playbackSpeed" min="0.5" max="2.0" step="0.1" value="1.0" 
                    oninput="document.getElementById('speedValue').innerText = Number(this.value).toFixed(1) + 'x'; document.getElementById('player').playbackRate = this.value;">
            </div>
        </div>
        
        <div class="btn-group">
            <button id="generateBtn" onclick="generateAudio()">Generate Audio</button>
            <button id="downloadBtn">Download .WAV</button>
        </div>
        
        <div class="status" id="statusText">Ready</div>
        
        <audio id="player" controls></audio>

        <script>
            let currentBlobUrl = null;

            async function generateAudio() {{
                const text = document.getElementById('text').value;
                const voice = document.getElementById('voice').value;
                const btn = document.getElementById('generateBtn');
                const dlBtn = document.getElementById('downloadBtn');
                const status = document.getElementById('statusText');
                const player = document.getElementById('player');
                
                if (!text.trim()) return;

                btn.disabled = true;
                btn.innerText = "Generating...";
                dlBtn.style.display = "none";
                status.innerText = "Processing audio with Kitten TTS...";
                
                try {{
                    const response = await fetch('/v1/audio/speech', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ input: text, voice: voice }})
                    }});
                    
                    if (!response.ok) throw new Error("Server returned an error");
                    
                    const blob = await response.blob();
                    
                    if (currentBlobUrl) URL.revokeObjectURL(currentBlobUrl);
                    currentBlobUrl = URL.createObjectURL(blob);
                    
                    player.src = currentBlobUrl;
                    player.playbackRate = document.getElementById('playbackSpeed').value;
                    
                    if (document.getElementById('autoPlay').checked) {{
                        player.play();
                    }}
                    
                    dlBtn.style.display = "block";
                    dlBtn.onclick = () => {{
                        const a = document.createElement('a');
                        a.href = currentBlobUrl;
                        a.download = `KittenTTS_${{voice}}_${{Date.now()}}.wav`;
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                    }};
                    
                    status.innerText = "Audio generated successfully!";
                }} catch (e) {{
                    status.innerText = "Error: " + e.message;
                }} finally {{
                    btn.disabled = false;
                    btn.innerText = "Generate Audio";
                }}
            }}
        </script>
    </body>
    </html>
    """
    return html_content

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)