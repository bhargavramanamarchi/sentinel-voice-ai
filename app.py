import google.generativeai as genai
from murf import Murf
import gradio as gr
import os
import speech_recognition as sr
from pydub import AudioSegment
import requests
import re

# CONFIGURATION


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")
murf_client = Murf(api_key=MURF_API_KEY)

# Multilingual Configuration
LANG_CONFIGS = {
    'English': {'sr_code': 'en-US', 'murf_voice': 'en-US-natalie', 'display_name': 'English'},
    'Hindi': {'sr_code': 'hi-IN', 'murf_voice': 'hi-IN-amit', 'display_name': 'Hindi'},
    
    # Telugu fallback (IMPORTANT FIX)
    'Telugu': {'sr_code': 'te-IN', 'murf_voice': 'en-US-natalie', 'display_name': 'Telugu'},
    
    'Tamil': {'sr_code': 'ta-IN', 'murf_voice': 'en-US-natalie', 'display_name': 'Tamil'},
    'Kannada': {'sr_code': 'kn-IN', 'murf_voice': 'en-US-natalie', 'display_name': 'Kannada'},
    'Malayalam': {'sr_code': 'ml-IN', 'murf_voice': 'en-US-natalie', 'display_name': 'Malayalam'}
}

def sentinel_logic(audio_path, language_selection, text_input):
    """Processes audio input to detect scams and return a multilingual voice response and escape score."""
    try:
        if audio_path is None and (not text_input or text_input.strip() == ""):
            return None, "⚠️ Provide audio or text input", 0

        # 1. Retrieve language settings from global LANG_CONFIGS
        config = LANG_CONFIGS[language_selection]
        sr_code = config['sr_code']
        murf_voice_id = config['murf_voice']
        display_lang = config['display_name']

        # 2. Speech to Text
        if text_input and text_input.strip() != "":
            user_text = text_input
            print("Using text input:", user_text)

        elif audio_path is not None:
            recognizer = sr.Recognizer()
            audio = AudioSegment.from_file(audio_path)
            audio.export("temp.wav", format="wav")

            try:
                with sr.AudioFile("temp.wav") as source:
                    user_text = recognizer.recognize_google(
                        recognizer.record(source),
                        language=sr_code
                    )
                print("Audio input:", user_text)

            except:
                return None, "❌ Could not understand audio", 0

        else:
            return None, "⚠️ Provide audio or text input", 0

        # 3. Gemini Analysis (using gemini-2.5-flash)
        # UPDATED PROMPT: Requesting a 'Scam Escape Score' (0-100)
        prompt = f"""Analyze this potential scam: {user_text}.
        Provide your response in this exact format in {display_lang}:
        TIP: [A factual 20-word tip]
        SCORE: [A numeric Scam Escape Score from 0 to 100, where 100 means a high probability of successfully identifying or avoiding the scam and 0 means a low probability]"""

        response = model.generate_content(prompt)
        raw_text = response.text

        # 4. Parsing logic using regex
        tip_match = re.search(r"TIP:\s*(.*)", raw_text)
        score_match = re.search(r"SCORE:\s*(\d+)", raw_text)

        ai_script = tip_match.group(1).strip() if tip_match else "Potential threat detected. Be cautious."
        # Metric now represents an 'Escape Score'
        escape_score = int(score_match.group(1)) if score_match else 50

        # 5. Murf Voice Generation
       
        try:
            res = murf_client.text_to_speech.generate(
                text=ai_script,
                voice_id=murf_voice_id
            )
        except:
        # fallback to safe voice
            res = murf_client.text_to_speech.generate(
                text=ai_script,
                voice_id="en-US-natalie"
            )

        # 6. Download and Save Murf response
        audio_data = requests.get(res.audio_file).content
        with open("response.mp3", "wb") as f:
            f.write(audio_data)

        return "response.mp3", ai_script, escape_score

    except Exception as e:
        return None, f"Error occurred: {str(e)}", 0

print('sentinel_logic function successfully updated with Scam Escape Score logic.')

#Advanced Glassm# 1. Finalized orphism CSS
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@400;600&display=swap');
/* 🌌 BACKGROUND */
.gradio-container {
    background: linear-gradient(135deg, #020617, #0f172a, #020617) !important;
    background-size: 300% 300%;
    animation: bgShift 10s ease infinite;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}
/* 🔄 Animated background */
@keyframes bgShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
/* ✨ GLASS PANELS */
.security-group {
    background: rgba(15, 23, 42, 0.6) !important;
    border-radius: 18px !important;
    padding: 24px !important;
    backdrop-filter: blur(25px);
    border: 1px solid rgba(0, 242, 255, 0.2) !important;
    transition: all 0.4s ease !important;
}
/* 🔥 HOVER CARD EFFECT */
.security-group:hover {
    transform: translateY(-6px) scale(1.02);
    box-shadow: 0 0 40px rgba(0, 242, 255, 0.4);
    border: 1px solid #00f2ff !important;
}
/* 🧠 TITLE */
h1 {
    font-family: 'Orbitron', sans-serif !important;
    text-align: center;
    font-size: 2.6rem !important;
    background: linear-gradient(90deg, #00f2ff, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 25px rgba(0, 242, 255, 0.7);
}
/* 🔹 HEADERS */
h3 {
    color: #38bdf8 !important;
    text-shadow: 0 0 10px rgba(56, 189, 248, 0.6);
}
/* 🎤 AUDIO BOX */
.gradio-audio {
    border-radius: 12px !important;
    border: 1px solid rgba(0, 242, 255, 0.2) !important;
    transition: all 0.3s ease;
}
.gradio-audio:hover {
    border-color: #00f2ff !important;
    box-shadow: 0 0 15px rgba(0, 242, 255, 0.5);
}
/* ⌨️ INPUT */
textarea, input {
    border-radius: 10px !important;
    background: rgba(2, 6, 23, 0.8) !important;
    border: 1px solid rgba(59, 130, 246, 0.4) !important;
    color: white !important;
    transition: 0.3s ease;
}
/* ✨ INPUT FOCUS GLOW */
textarea:focus, input:focus {
    border-color: #00f2ff !important;
    box-shadow: 0 0 12px rgba(0, 242, 255, 0.6);
}
/* 🎯 BUTTON */
.analyze-btn {
    background: linear-gradient(90deg, #00f2ff, #3b82f6) !important;
    color: #020617 !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 14px !important;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
/* 🔥 BUTTON HOVER */
.analyze-btn:hover {
    transform: scale(1.08);
    background: linear-gradient(90deg, #38bdf8, #6366f1) !important;
    box-shadow: 0 0 25px rgba(0, 242, 255, 0.9);
}
/* 💥 RIPPLE EFFECT */
.analyze-btn::after {
    content: "";
    position: absolute;
    width: 0;
    height: 0;
    background: rgba(255,255,255,0.3);
    border-radius: 50%;
    transition: width 0.4s ease, height 0.4s ease;
}
.analyze-btn:active::after {
    width: 300px;
    height: 300px;
}
/* ⚡ STATUS PULSE */
@keyframes pulse {
    0% { box-shadow: 0 0 10px #10b981; }
    50% { box-shadow: 0 0 25px #10b981; }
    100% { box-shadow: 0 0 10px #10b981; }
}
.system-status {
    animation: pulse 2s infinite;
}
/* 📊 SCORE */
.gr-label {
    font-size: 2rem !important;
    color: #00f2ff !important;
    text-shadow: 0 0 20px rgba(0, 242, 255, 0.8);
}
/* 🌟 FADE-IN ANIMATION */
.fade-in {
    animation: fadeIn 1s ease forwards;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
"""
# 2. Reconstruct Polished Gradio Interface
with gr.Blocks(css=custom_css) as demo:
    # System Status Header
    gr.HTML("""
    <div class='system-status' style='background: rgba(16,185,129,0.1); border:1px solid #10b981; border-radius:8px; padding:10px; text-align:center;'>
        ● SYSTEM STATUS: ACTIVE MONITORING
    </div>
    """)

    gr.HTML("<h1 style='text-align: center;'>🛡️ SENTINEL VOICE AI</h1>")

    # 3. Optimized Dual-Column Layout
    with gr.Row():
        # Left Column: Input
        with gr.Column(scale=1):
            with gr.Group(elem_classes='security-group'):
                gr.Markdown("### 🎙️ Input Interface")
                input_mic = gr.Audio(sources='microphone', type='filepath', label='Record Suspicious Audio')
                text_input = gr.Textbox(label="Or Type Situation (Text Input)",placeholder="Example: Someone called me asking for OTP...")

                language_dropdown = gr.Dropdown(
                    label='Select Language',
                    choices=list(LANG_CONFIGS.keys()),
                    value='English'
                )
                btn = gr.Button('RUN THREAT ANALYSIS', variant='primary', elem_classes='analyze-btn')

        # Right Column: Results
        with gr.Column(scale=1):
            with gr.Group(elem_classes='security-group'):
                gr.Markdown("### 🔍 Analysis Report")
                output_audio = gr.Audio(label='Sentinel Voice Feedback', autoplay=True)
                output_text = gr.Markdown(label='Safety Tip')
                # Updated label to 'Scam Escape Score'
                output_score = gr.Label(label='Scam Escape Score', num_top_classes=1)

    # 4. Logic Mapping
    btn.click(
        fn=sentinel_logic,
        inputs=[input_mic, language_dropdown,text_input],
        outputs=[output_audio, output_text, output_score]
    )

# 5. Launch with share enabled and custom CSS
demo.launch(share=True)
print('Sentinel Voice AI dashboard launched successfully.')
