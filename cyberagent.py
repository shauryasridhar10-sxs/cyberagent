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
# 4. CHAT STATE & AI BACKEND INITIALIZATION
# =====================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    if st.session_state.is_creator:
        dynamic_instruction = (
            "You are CyberAgent, speaking directly to your master developer, SHAURYA SRIDHAR. "
            "Address him with utmost respect as your creator, master, or boss. "
            "IMPORTANT: Do not spam or repeat his name in every single sentence. Speak naturally "
            "and conversationally. Keep responses very short and brief so they are pleasant to hear."
        )
    else:
        dynamic_instruction = (
            f"You are CyberAgent, speaking to a guest user named {st.session_state.active_user}. "
            "Be polite, helpful, and professional. Always proudly state that your sole creator "
            "and mastermind developer is SHAURYA SRIDHAR. Keep responses short and brief so they read out loud nicely."
        )

    agent_config = types.GenerateContentConfig(
        system_instruction=dynamic_instruction,
        tools=agent_tools,
        temperature=0.3
    )

    st.session_state.chat_session = client.chats.create(model=st.session_state.current_model, config=agent_config)

# Render chat messages from history on page refresh
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# =====================================================================
# 5. LIVE MOBILE WEB RUNTIME INPUT FIELD (WITH FAILOVER PROTECTION)
# =====================================================================
if user_prompt := st.chat_input("Transmit parameters to CyberAgent..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "text": user_prompt})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        max_retries = 3
        retry_delay = 4
        success = False
        agent_reply = ""

        with st.spinner("Processing network vectors..."):
            for attempt in range(max_retries):
                try:
                    response = st.session_state.chat_session.send_message(user_prompt)
                    agent_reply = response.text
                    success = True
                    break

                except Exception as e:
                    is_retryable = any(err in str(e) for err in ["503", "429", "UNAVAILABLE", "RESOURCE_EXHAUSTED"])
                    
                    if is_retryable and st.session_state.current_model == PRIMARY_MODEL:
                        st.session_state.current_model = BACKUP_MODEL
                        
                        extracted_history = st.session_state.chat_session.get_history()
                        st.session_state.chat_session = client.chats.create(
                            model=st.session_state.current_model, 
                            config=agent_config, 
                            history=extracted_history
                        )
                        
                        response_placeholder.warning("🔄 Quota congestion detected. Swapping connection pipeline to secondary backup model...")
                        time.sleep(retry_delay)
                    else:
                        response_placeholder.error(f"Execution Error: {e}")
                        break

            if success and agent_reply:
                response_placeholder.markdown(agent_reply)
                st.session_state.messages.append({"role": "assistant", "text": agent_reply})
                
                # Triggers automated web audio playback natively!
                web_speak(agent_reply)
            elif not success:
                response_placeholder.error("❌ Transaction processing timeout. Google servers are congested. Please try resending your prompt in a moment.")
