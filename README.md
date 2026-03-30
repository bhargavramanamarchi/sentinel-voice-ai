# 🛡️ Sentinel Voice AI

## 🚨 Problem Statement
With the increasing rise of digital frauds such as OTP scams, phishing attacks, and account hacking, users often panic and fail to take the correct actions in time. Existing cybersecurity tools are complex, text-heavy, and not designed for real-time guidance or emotional support, especially for non-technical users.

---

## 💡 Solution
Sentinel Voice AI is an emotion-aware, voice-based cybersecurity assistant that helps users detect scams and respond instantly through voice guidance.

It listens to user input, analyzes the situation using AI, and gives back a clear safety response using voice.

---

## 🎯 Key Features
- 🎙️ Voice Input (Speech Recognition)
- 🧠 AI Scam Detection (Google Gemini)
- 🔊 Voice Output (Murf AI)
- 🌍 Multilingual Support (English, Hindi, Telugu, Tamil, Kannada, Malayalam)
- ⚡ Real-time response
- 📊 Scam Escape Score (0–100)
- 🎨 Simple UI using Gradio

---

## 🏗️ How It Works
1. User speaks or records audio  
2. Audio is converted to text  
3. AI analyzes the text for scam detection  
4. AI generates a safety tip + score  
5. Response is converted into voice  
6. User gets voice output + score  

---

## 🛠️ Tech Stack
- Python  
- Gradio  
- Google Gemini API  
- Murf AI  
- SpeechRecognition  
- Pydub  
- Requests  

---

## 🚀 How to Run

1. Clone the repo:
git clone https://github.com/bhargavramanamarchi/sentinel-voice-ai-murf-ai.git

2. Install dependencies:
pip install -r requirements.txt

3. Add API keys:
GOOGLE_API_KEY=your_key  
MURF_API_KEY=your_key  

4. Run:
python app.py

---

## 🌐 Live Demo
👉 https://huggingface.co/spaces/Bhargav-06/SentinelAi

---

## ⚠️ Limitations
- Free API has daily limits (Gemini)
- Some voices may fallback to English
- Requires internet

---

## 🔮 Future Scope
- Better regional voice support  
- Offline mode  
- Emotion detection improvement  
- Direct scam alert system  

---

## 👨‍💻 Team
- Bhargav Ramana Marchi  
- Jeevan  

---

## 📌 Conclusion
Sentinel Voice AI makes cybersecurity simple, fast, and accessible using voice and AI. It helps users stay safe from digital scams without technical knowledge.
