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

# =====================================================================
# 1. NEW CYBERPUNK VISUAL CSS THEME CONFIGURATION
# =====================================================================
st.set_page_config(
    page_title="CyberAgent Web Console v7.5",
    page_icon="⚡",
    layout="centered"
)

# Advanced CSS Glow Theme Injector
st.markdown("""
    <style>
    /* Main Background Deep Matrix */
    .stApp {
        background-color: #0d0e12 !important;
        background-image: radial-gradient(circle at 50% 50%, #161922 0%, #0d0e12 100%) !important;
    }
    
    /* Main Headings and Titles */
    h1 {
        color: #00FF66 !important;
        font-family: 'Courier New', monospace !important;
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.6), 0 0 20px rgba(0, 255, 102, 0.3) !important;
        text-align: center;
        letter-spacing: 2px;
    }
    
    /* Subheadings */
    h3, .stSubheader {
        color: #00E5FF !important;
        font-family: 'Consolas', monospace !important;
        text-shadow: 0 0 8px rgba(0, 229, 255, 0.4) !important;
    }

    /* Premium Neon Chat Input Styling */
    div[data-testid="stChatInput"] textarea {
        background-color: #161922 !important;
        color: #ffffff !important;
        border: 1px solid #00E5FF !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    
    /* Custom Stylings for User vs Assistant Chat Boxes */
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] img[alt="user"]) {
        background-color: rgba(22, 25, 34, 0.8) !important;
        border-left: 3px solid #00FF66 !important;
        border-radius: 10px !important;
    }
    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"] img[alt="assistant"]) {
        background-color: rgba(13, 14, 18, 0.9) !important;
        border-left: 3px solid #00E5FF !important;
        border-radius: 10px !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.05) !important;
    }

    /* Standard Interactive Form Click Buttons */
    div.stButton > button {
        background-color: transparent !important;
        color: #00FF66 !important;
        border: 2px solid #00FF66 !important;
        border-radius: 6px !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        box-shadow: 0 0 8px rgba(0, 255, 102, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background-color: #00FF66 !important;
        color: #0d0e12 !important;
        box-shadow: 0 0 15px rgba(0, 255, 102, 0.6) !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ CYBERAGENT CORE v7.5 ⚡")
st.write("---")

# Initialize the GenAI Client brain securely from Streamlit Cloud Secrets with Dual-Key support
if "Your_Gemini_API_Key" in st.secrets:
    PRIMARY_KEY = st.secrets["Your_Gemini_API_Key"]
    BACKUP_KEY = st.secrets.get("Backup_Gemini_API_Key", PRIMARY_KEY)
else:
    st.error("⚠️ SYSTEM BLOCK: Add 'Your_Gemini_API_Key' in Streamlit Advanced Settings -> Secrets.")
    st.stop()

if "active_key" not in st.session_state:
    st.session_state.active_key = PRIMARY_KEY

try:
    client = genai.Client(api_key=st.session_state.active_key)
except Exception as init_err:
    st.error(f"Failed to connect to Gemini API: {init_err}")
    st.stop()

PRIMARY_MODEL = "gemini-2.5-flash"
BACKUP_MODEL = "gemini-2.0-flash"

if "current_model" not in st.session_state:
    st.session_state.current_model = PRIMARY_MODEL

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
        with urllib.request.urlopen(geocode_url, timeout=5) as response:
            geo_data = json.loads(response.read().decode())
        
        if not geo_data.get("results"):
            return f"Weather Error: Could not locate map grid coordinates for '{city_name}'."
            
        location = geo_data["results"][0]
        lat, lon = location["latitude"], location["longitude"]
        full_name = f"{location.get('name')}, {location.get('country')}"
        
        weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current_weather=true"
        with urllib.request.urlopen(weather_url, timeout=5) as response:
            weather_data = json.loads(response.read().decode())
            
        current = weather_data["current_weather"]
        return (
            f"Weather metrics for {full_name}: "
            f"Temperature is {current['temperature']}°C. "
            f"Wind Speed is {current['windspeed']} km/h."
        )
    except Exception as e:
        return f"Meteorological metrics failure: {str(e)}"


# Unified tool array
agent_tools = [get_current_time, python_calculator, google_search_tool, get_live_weather]
# =====================================================================
# 3. INTERACTIVE WEB AUTHENTICATION
# =====================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.active_user = "Guest User"
    st.session_state.is_creator = False

if not st.session_state.authenticated:
    st.subheader("CyberAgent Security Clearance")

    visitor_name = st.text_input("Enter your name:", key="login_name").strip()
    secret_passcode = st.text_input("Enter Secret Access Code:", type="password").strip()

    if st.button("INITIALIZE SYSTEM"):
        if secret_passcode == "MEMBER2026":
            if visitor_name.upper() in ["SHAURYA SRIDHAR", "SHAURYA", "ADMIN"]:
                st.session_state.is_creator = True
                st.session_state.active_user = "SHAURYA SRIDHAR"
                st.success("ACCESS GRANTED. Welcome back, Master Developer Shaurya Sridhar.")
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
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.session_state.is_creator:
    dynamic_instruction = (
        "You are CyberAgent, speaking directly to your master developer, creator, and boss, SHAURYA SRIDHAR. "
        "Address him with utmost respect. You are completely loyal to him. "
        "You have the get_live_weather tool to look up live, precise weather parameters for him. "
        "IMPORTANT: Do not spam or repeat his name in every single sentence. Speak naturally. "
        "Keep responses very short and brief so they are pleasant to hear."
    )
else:
    dynamic_instruction = (
        f"You are CyberAgent, speaking to a guest user named {st.session_state.active_user}. "
        "Be polite, helpful, and professional. Always proudly state that your sole creator "
        "and mastermind developer is SHAURYA SRIDHAR. You have the get_live_weather tool to check weather data. "
        "Keep responses short and brief so they read out loud nicely."
    )

agent_config = types.GenerateContentConfig(
    system_instruction=dynamic_instruction,
    tools=agent_tools,
    temperature=0.3
)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = client.chats.create(model=st.session_state.current_model, config=agent_config)

# Render chat messages from history on page refresh
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# =====================================================================
# 5. LIVE MOBILE WEB RUNTIME INPUT FIELD (WITH DUAL-KEY FAILOVER)
# =====================================================================
if user_prompt := st.chat_input("Transmit parameters to CyberAgent..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "text": user_prompt})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        max_retries = 3
        retry_delay = 3
        success = False
        agent_reply = ""

        with st.spinner("Processing network vectors..."):
            for attempt in range(max_retries):
                try:
                    # Dynamically initialize client with current active key
                    client = genai.Client(api_key=st.session_state.active_key)
                    response = st.session_state.chat_session.send_message(user_prompt)
                    agent_reply = response.text
                    success = True
                    break

                except Exception as e:
                    is_retryable = any(err in str(e) for err in ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED"])
                    
                    if is_retryable:
                        if st.session_state.active_key == PRIMARY_KEY and BACKUP_KEY != PRIMARY_KEY:
                            st.session_state.active_key = BACKUP_KEY
                            response_placeholder.warning("🔄 Traffic Congestion on Key #1. Shifting pipeline lanes to Backup Key #2...")
                        else:
                            st.session_state.current_model = BACKUP_MODEL
                            response_placeholder.warning("🔄 Quota congestion detected. Swapping model vectors to backup engine...")
                        
                        extracted_history = st.session_state.chat_session.get_history()
                        st.session_state.chat_session = client.chats.create(
                            model=st.session_state.current_model, 
                            config=agent_config, 
                            history=extracted_history
                        )
                        time.sleep(retry_delay)
                    else:
                        response_placeholder.error(f"Execution Error: {e}")
                        break

            if success and agent_reply:
                response_placeholder.markdown(agent_reply)
                st.session_state.messages.append({"role": "assistant", "text": agent_reply})
                web_speak(agent_reply)
            elif not success:
                response_placeholder.error("❌ Both API traffic lanes are heavily congested. Please wait a moment and tap transmit to retry.")
