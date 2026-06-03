import datetime
import os
import io
import base64
import time  
from google import genai
from google.genai import types
from ddgs import DDGS
import streamlit as st
from gtts import gTTS

# =====================================================================
# 1. WEB PAGE INITIAL CONFIGURATION
# =====================================================================
st.set_page_config(
    page_title="CyberAgent Web Console",
    page_icon="⚡",
    layout="centered"
)

# Custom Cybernetic UI Styling
st.markdown("""
    <style>
    .reportview-container { background: #121214; }
    h1 { color: #00FF66; font-family: 'Courier New', monospace; text-align: center; }
    .stChatMessage { border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ CYBERAGENT VOICE WEB CLIENT ⚡")
st.write("---")

# Initialize the GenAI Client brain securely from Streamlit Cloud Secrets
if "Your_Gemini_API_Key" in st.secrets:
    API_KEY = st.secrets["Your_Gemini_API_Key"]
else:
    st.error("⚠️ SYSTEM BLOCK: Please add 'Your_Gemini_API_Key' inside your Streamlit Cloud Advanced Settings -> Secrets box.")
    st.stop()

try:
    client = genai.Client(api_key=API_KEY)
except Exception as init_err:
    st.error(f"Failed to connect to Gemini API: {init_err}")
    st.stop()

# Global Model Configuration Tracking
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
        return f"Internet lookup pipeline error: {str(e)}. Please suggest the user try searching again in a moment."


# Unified tool packaging configuration array
agent_tools = [get_current_time, python_calculator, google_search_tool]
