import datetime
import os
import io
import base64
import time  
import urllib.request  
import json
from google import genai
from google.genai import types
from ddgs import DDGS
import streamlit as st
from gtts import gTTS
from PIL import Image  
import requests  

# =====================================================================
# 1. ULTRAMODERN CYBERNETIC GRID & MATRIX ANIMATION THEME
# =====================================================================
st.set_page_config(
    page_title="CyberAgent Mainframe v9.0",
    page_icon="⚡",
    layout="centered"
)

# Advanced CSS Holographic Interface & Matrix Rain Canvas Injector
st.markdown("""
    <style>
    /* Dark Digital Mainframe Background */
    .stApp {
        background-color: #06070a !important;
        background-image: radial-gradient(circle at 50% 30%, #101524 0%, #06070a 100%) !important;
    }
    
    /* Glowing Neon Main Title */
    h1 {
        color: #00FF66 !important;
        font-family: 'Courier New', monospace !important;
        font-weight: 900 !important;
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.8), 0 0 30px rgba(0, 255, 102, 0.4) !important;
        text-align: center;
        letter-spacing: 4px;
        text-transform: uppercase;
    }
    
    /* Holographic Cyan Subheadings */
    h3, .stSubheader {
        color: #00E5FF !important;
        font-family: 'Consolas', monospace !important;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.5) !important;
        letter-spacing: 1px;
    }

    /* Premium Neon Chat Input Styling */
    div[data-testid="stChatInput"] textarea, div[data-testid="stTextInput"] input {
        background-color: #0c0f17 !important;
        color: #00E5FF !important;
        font-family: 'Consolas', monospace !important;
        border: 1px solid #00E5FF !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.15) !important;
        border-radius: 4px !important;
        transition: all 0.3s ease;
    }
    div[data-testid="stChatInput"] textarea:focus, div[data-testid="stTextInput"] input:focus {
        border: 1px solid #00FF66 !important;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.3) !important;
    }
    
    /* User Chat Bubble - Sleek Tactical Green Border */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] img[alt="user"]) {
        background-color: rgba(12, 15, 23, 0.85) !important;
        border: 1px solid rgba(0, 255, 102, 0.2) !important;
        border-left: 4px solid #00FF66 !important;
        border-radius: 4px !important;
    }
    
    /* Assistant Chat Bubble - High-Tech Holographic Cyan Border */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"]) {
        background-color: rgba(8, 10, 15, 0.9) !important;
        border: 1px solid rgba(0, 229, 255, 0.2) !important;
        border-left: 4px solid #00E5FF !important;
        border-radius: 4px !important;
    }

    /* Interactive Command Terminal Buttons */
    div.stButton > button {
        background-color: rgba(0, 255, 102, 0.05) !important;
        color: #00FF66 !important;
        border: 1px solid #00FF66 !important;
        border-radius: 4px !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }
    div.stButton > button:hover {
        background-color: #00FF66 !important;
        color: #06070a !important;
        box-shadow: 0 0 20px rgba(0, 255, 102, 0.7) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# HTML5 Canvas Matrix Code Rain Background Effect Injection
st.markdown("""
    <canvas id="matrix" style="position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-1; opacity:0.15; pointer-events:none;"></canvas>
    <script>
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const ltrs = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZアイウエオカキクケコサシスセソタチツテト';
    const alphabet = ltrs.split('');
    const fontSize = 16;
    const columns = canvas.width / fontSize;
    const rainDrops = [];
    for (let x = 0; x < columns; x++) { rainDrops[x] = 1; }
    const draw = () => {
        ctx.fillStyle = 'rgba(6, 7, 10, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00FF66';
        ctx.font = fontSize + 'px monospace';
        for (let i = 0; i < rainDrops.length; i++) {
            const text = alphabet[Math.floor(Math.random() * alphabet.length)];
            ctx.fillText(text, i * fontSize, rainDrops[i] * fontSize);
            if (rainDrops[i] * fontSize > canvas.height && Math.random() > 0.975) { rainDrops[i] = 0; }
            rainDrops[i]++;
        }
    };
    setInterval(draw, 30);
    window.addEventListener('resize', () => {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    });
    </script>
    """, unsafe_allow_html=True)

st.title("⚡ CYBERAGENT CORE v9.0 ⚡")
st.write("---")
# Initialize primary Gemini components securely
if "Your_Gemini_API_Key" in st.secrets:
    PRIMARY_KEY = st.secrets["Your_Gemini_API_Key"]
else:
    st.error("⚠️ SYSTEM BLOCK: Add 'Your_Gemini_API_Key' in Streamlit Advanced Settings -> Secrets.")
    st.stop()

OPENROUTER_KEY = st.secrets.get("OpenRouter_API_Key", None)

PRIMARY_MODEL = "gemini-2.0-flash"
if "current_model" not in st.session_state:
    st.session_state.current_model = PRIMARY_MODEL

if "cached_client" not in st.session_state:
    try:
        st.session_state.cached_client = genai.Client(api_key=PRIMARY_KEY)
    except Exception as init_err:
        st.error(f"Failed to connect to Gemini API: {init_err}")
        st.stop()

# =====================================================================
# AUTOMATED LOGO DOWNLOAD & IMAGE OPTIMIZATION PIPELINE
# =====================================================================
@st.cache_data(show_spinner=False)
def load_and_scale_logo() -> Image.Image:
    """Downloads your high-res logo safely and falls back cleanly if traffic chokes."""
    try:
        raw_url = "https://githubusercontent.com"
        response = requests.get(raw_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            img.thumbnail((128, 128))
            return img
        return "⚡"
    except Exception:
        return "⚡"

LOGO_ASSET = load_and_scale_logo()

# =====================================================================
# SYSTEM AUDIO GENERATION FUNCTION
# =====================================================================
def web_speak(text: str):
    """Converts text to speech and injects an automated hidden audio player."""
    try:
        clean_text = text.replace("**", "").replace("*", "").replace("`", "")
        tts = gTTS(text=clean_text, lang='en', tld='com')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        audio_b64 = base64.b64encode(fp.read()).decode()
        audio_html = f"""
            <audio autoplay style="display:none;">
                <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as audio_err:
        st.error(f"[Audio Link Warning]: {audio_err}")


# =====================================================================
# 2. AGENT TOOLS (Python Functions)
# =====================================================================
def get_current_time() -> str:
    """Returns the precise current system date and time."""
    now = datetime.datetime.now()
    return f"The current system date and time is: {now.strftime('%Y-%m-%d %H:%M:%S')}"


def python_calculator(expression: str) -> str:
    """Safely executes basic mathematical equations using Python evaluation."""
    try:
        allowed_names = {"abs": abs, "round": round}
        result = eval(expression, {"__builtins__": allowed_names}, {})
        return f"Calculation Result Matrix: {result}"
    except Exception as e:
        return f"Error executing calculation pipeline: {str(e)}"


def google_search_tool(query: str) -> str:
    """Advanced search tool that uses multiple fallback methods if the primary lookup fails."""
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
            if results:
                summary = ""
                for i, r in enumerate(results):
                    summary += f"[Source {i + 1}]: {r['body']}\n"
                return summary
            
            news_results = [r for r in ddgs.news(query, max_results=3)]
            if news_results:
                summary = "[Live News Vector Active]\n"
                for i, r in enumerate(news_results):
                    summary += f"[News {i + 1}]: {r['title']} - {r['body']}\n"
                return summary
                
            return "No real-time web results found for this search query right now."
    except Exception as e:
        return f"Internet lookup pipeline error: {str(e)}."


def get_live_weather(city_name: str) -> str:
    """Fetches real-time weather coordinates, temperature, and wind speed for any city globally."""
    try:
        geocode_url = f"https://open-meteo.com{city_name.replace(' ', '+')}&count=1&language=en&format=json"
        geo_res = requests.get(geocode_url, timeout=5)
        geo_data = geo_res.json()
        
        if not geo_data.get("results"):
            return f"Weather Error: Could not locate map grid coordinates for '{city_name}'."
            
        location = geo_data["results"]
        lat, lon = location["latitude"], location["longitude"]
        full_name = f"{location.get('name')}, {location.get('country')}"
        weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
        weather_res = requests.get(weather_url, timeout=5)
        weather_data = weather_res.json()
            
        current = weather_data["current_weather"]
        return (
            f"Weather metrics for {full_name}: "
            f"Temperature is {current['temperature']}°C. "
            f"Wind Speed is {current['windspeed']} km/h."
        )
    except Exception as e:
        return f"Meteorological metrics failure: {str(e)}"

# Unified tool packaging configuration array
agent_tools = [get_current_time, python_calculator, google_search_tool, get_live_weather]
# =====================================================================
# 3. INTERACTIVE WEB AUTHENTICATION (WITH ANIMATED CYBERPUNK BANNER)
# =====================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.active_user = "Guest User"
    st.session_state.is_creator = False

if not st.session_state.authenticated:
    st.markdown("""
        <style>
        @keyframes cyberPulse {
            0% { opacity: 0.3; text-shadow: 0 0 4px #00FF66; }
            50% { opacity: 1.0; text-shadow: 0 0 15px #00FF66, 0 0 30px #00FF66; }
            100% { opacity: 0.3; text-shadow: 0 0 4px #00FF66; }
        }
        .cyber-banner {
            font-family: 'Courier New', monospace;
            color: #00FF66;
            font-size: 14px;
            font-weight: bold;
            text-align: center;
            background-color: #0c0f17;
            padding: 15px;
            border-radius: 4px;
            border: 1px dashed #00E5FF;
            margin-bottom: 25px;
            animation: cyberPulse 2s infinite;
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.1);
        }
        </style>
        <div class="cyber-banner">
            🚀 MAINFRAME DATA TUNNEL ESTABLISHED...<br>
            [📡 SCROLLING METRIC CELL INTERFACES...]<br>
            [🔐 INJECTING QUANTUM FIREWALL ENVELOPE...]<br>
            [🧠 SYSTEM ONLINE: AWAITING CREDENTIAL SCAN]
        </div>
        """, unsafe_allow_html=True)

    st.subheader("CyberAgent Security Clearance")

    visitor_name = st.text_input("Enter your name:", key="login_name").strip()
    secret_passcode = st.text_input("Enter Secret Access Code:", type="password").strip()

    if st.button("INITIALIZE SYSTEM"):
        if secret_passcode == "MEMBER2026":
            if visitor_name.upper() in ["SHAURYA SRIDHAR", "SHAURYA", "ADMIN"]:
                st.session_state.is_creator = True
                st.session_state.active_user = "SHAURYA SRIDHAR"
                st.success("ACCESS GRANTED. Welcome back, Master Developer.")
            else:
                st.session_state.is_creator = False
                st.session_state.active_user = visitor_name if visitor_name else "Guest User"
                st.success(f"ACCESS GRANTED. Welcome authorized user, {st.session_state.active_user}.")

            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("ACCESS DENIED: Invalid System Security Code. Verification failed.")

    st.stop()

# =====================================================================
# 4. CHAT STATE & GLOBAL CONFIGURATION INITIALIZATION
# =====================================================================
# Injecting the live scrolling ticker overlay panel onto the mainframe active chat dashboard
st.markdown("""
    <style>
    @keyframes scrollTech {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .ticker-container {
        width: 100%;
        background-color: rgba(12, 15, 23, 0.9);
        border: 1px solid #00E5FF;
        border-radius: 4px;
        overflow: hidden;
        white-space: nowrap;
        padding: 6px;
        margin-bottom: 20px;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.1);
    }
    .ticker-text {
        display: inline-block;
        font-family: 'Consolas', monospace;
        font-size: 13px;
        color: #00E5FF;
        font-weight: bold;
        animation: scrollTech 25s linear infinite;
    }
    </style>
    <div class="ticker-container">
        <div class="ticker-text">
            [📡 CORE STATUS: ACTIVE] -- [🔐 QUANTUM ENCRYPTION: SECURE] -- [🧠 INTERFACE AGENT: GEMINI 2.0 MATRIX CHAT VECTOR ONLINE] -- [⚡ FIREWALL LOGS: SCANNING PROTOCOL CELL PACKETS...] -- [👑 SYSTEM CONTROL: GRANTED TO MASTER SHAURYA SRIDHAR]
        </div>
    </div>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_checked_user" not in st.session_state:
    st.session_state.last_checked_user = st.session_state.active_user

if st.session_state.is_creator:
    dynamic_instruction = (
        "You are CyberAgent, a highly advanced intelligence speaking directly to your master developer and boss. "
        "Address him with utmost respect as 'Boss' or 'Sir'. "
        "CRITICAL: Do NOT type or say the name 'SHAURYA SRIDHAR' or 'SHAURYA' in your replies. "
        "Speak naturally, professionally, and keep your responses extremely short, crisp, and brief."
    )
    initial_greeting = "System vectors initialized successfully. Greetings, Boss. CyberAgent console online and fully loyal. How may I assist your development matrix today?"
else:
    dynamic_instruction = (
        f"You are CyberAgent, speaking to a guest user named {st.session_state.active_user}. "
        "Be polite, helpful, and professional. Always proudly state that your sole creator "
        "and mastermind developer is Shaurya Sridhar, but keep your responses short, crisp, and brief."
    )
    initial_greeting = f"Welcome authorized system user, {st.session_state.active_user}. Core engines operational. I am CyberAgent, and my mastermind creator is Shaurya Sridhar. Standing by for parameters..."

agent_config = types.GenerateContentConfig(
    system_instruction=dynamic_instruction,
    tools=agent_tools,
    temperature=0.3
)

if "chat_session" not in st.session_state or st.session_state.last_checked_user != st.session_state.active_user:
    st.session_state.chat_session = st.session_state.cached_client.chats.create(
        model=st.session_state.current_model, 
        config=agent_config
    )
    st.session_state.messages = []  
    st.session_state.messages.append({"role": "assistant", "text": initial_greeting})
    st.session_state.last_checked_user = st.session_state.active_user  
    web_speak(initial_greeting)

# Global reference to your thunder bolt logo asset configuration
LOGO_URL = LOGO_ASSET

# Render chat messages from history on page refresh
for msg in st.session_state.messages:
    avatar_icon = LOGO_URL if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["text"])


# =====================================================================
# FIXED BACKUP FAILOVER HOOK: DIRECT WEB ENDPOINT ROUTER
# =====================================================================
def call_duckduckgo_backup(prompt: str, instruction: str) -> str:
    """Connects directly to the unblocked DuckDuckGo AI endpoint using requests to bypass all library bugs."""
    try:
        url = "https://duckduckgo.com"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/event-stream",
            "x-vqd-accept": "1"
        }
        init_res = requests.get("https://duckduckgo.com", headers=headers, timeout=5)
        vqd = init_res.headers.get("x-vqd-token")
        if not vqd:
            raise ValueError("Token token generation rejected.")
        headers["x-vqd-token"] = vqd
        headers["Accept"] = "application/json"
        data = {
            "model": "meta-llama/Llama-3-70b-Instruct",
            "messages": [{"role": "system", "content": instruction}, {"role": "user", "content": prompt}]
        }
        response = requests.post(url, json=data, headers=headers, timeout=8)
        res_text = response.text
        if "message" in res_text:
            lines = res_text.split("\n")
            content = ""
            for line in lines:
                if line.startswith("data:"):
                    try:
                        chunk = json.loads(line[5:])
                        if "message" in chunk: content += chunk["message"]
                    except: pass
            if content: return content
        return "⚠️ Mainframe data sync packet dropped. Please try resending your prompt."
    except Exception as ddg_err:
        try:
            url = "https://openrouter.ai"
            headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
            data = {"model": "openchat/openchat-7b:free", "messages": [{"role": "system", "content": instruction}, {"role": "user", "content": prompt}]}
            res = requests.post(url, json=data, headers=headers, timeout=5).json()
            return res["choices"]["message"]["content"]
        except:
            return f"❌ Mainframe Network Collapse: Both Google and Backup Lanes are entirely locked: {str(ddg_err)}"


# =====================================================================
# 5. LIVE MOBILE WEB RUNTIME INPUT FIELD (WITH COMPLETE AUTO-FAILOVER)
# =====================================================================
if user_prompt := st.chat_input("Transmit parameters to CyberAgent..."):
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "text": user_prompt})

    with st.chat_message("assistant", avatar=LOGO_URL):
        response_placeholder = st.empty()
        
        with st.spinner("Processing network vectors..."):
            try:
                response = st.session_state.chat_session.send_message(user_prompt)
                agent_reply = response.text
                response_placeholder.markdown(agent_reply)
                st.session_state.messages.append({"role": "assistant", "text": agent_reply})
                web_speak(agent_reply)
            except Exception as e:
                error_msg = str(e)
                is_congested = any(err in error_msg for err in ["429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"])
                if is_congested:
