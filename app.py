import streamlit as st
import requests
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Anytime Buddy", page_icon="💙", layout="centered")

st.title("💙 Anytime Buddy")
st.markdown("Welcome to your personal nursing companion. Click below to start chatting with Shawn.")

# --- YOUR RENDER BACKEND URL ---
# Replace this with your actual Render URL (keep the /api/start-conversation part)
BACKEND_URL = "https://anytime-buddy-backend.onrender.com/api/start-conversation"

# --- SESSION STATE ---
if "conversation_url" not in st.session_state:
    st.session_state.conversation_url = None

# --- UI CONTROLS ---
if st.session_state.conversation_url is None:
    if st.button("Start Conversation", type="primary", use_container_width=True):
        with st.spinner("Waking up Shawn... Please wait."):
            try:
                # 1. Ping the Node.js backend to get the Tavus URL
                response = requests.post(BACKEND_URL)
                
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.conversation_url = data.get("conversationUrl")
                    st.rerun()  # Refresh the page to show the video
                else:
                    st.error(f"Error connecting to backend: {response.text}")
            except Exception as e:
                st.error(f"Failed to reach the server. Make sure your Render backend is live! Error: {e}")

# --- VIDEO RENDERER ---
if st.session_state.conversation_url:
    st.success("Connected! Please allow camera and microphone permissions when prompted.")
    
    # We use an iframe to embed the Tavus video room. 
    # The 'allow' attribute is CRITICAL for the mic and camera to work!
    components.iframe(
        st.session_state.conversation_url,
        height=600,
        scrolling=False,
    )
    
    # End Call Button
    if st.button("End Session", type="secondary"):
        st.session_state.conversation_url = None
        st.rerun()