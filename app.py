import streamlit as st
import requests
import streamlit.components.v1 as components
import base64
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Anytime Buddy", page_icon="✨", layout="wide", initial_sidebar_state="collapsed")

# --- FLOATING LOGO FUNCTION ---
def add_floating_logo(image_path):
    """Reads a local image and pins it to the top left corner using CSS."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        logo_html = f"""
        <style>
            .floating-logo {{
                position: fixed;
                top: 20px;
                left: 30px;
                z-index: 999999; /* Ensures it stays on top of the video */
                width: 140px; /* Adjust this to make your logo bigger/smaller */
            }}
        </style>
        <img src="data:image/png;base64,{encoded_string}" class="floating-logo">
        """
        st.markdown(logo_html, unsafe_allow_html=True)

# Inject the logo immediately
add_floating_logo("asb_logo_dark.png")


# --- GLOBAL CSS & FONTS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Inter:wght@400;600&family=EB+Garamond:wght@400;500&display=swap');

    /* Hide default Streamlit elements */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Elegant Serif Heading - Centered */
    h1 {
        font-family: 'Playfair Display', serif !important;
        font-size: 5rem !important;
        font-weight: 400 !important;
        color: #FAFAFA !important;
        line-height: 1.1 !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -1px;
        text-align: center;
    }
    
    /* Classic Serif Body Text - Centered */
    .subtitle {
        font-family: 'EB Garamond', serif;
        font-size: 1.6rem;
        color: #D1D5DB;
        line-height: 1.4;
        margin-bottom: 3rem;
        text-align: center;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Sharp Retro-Modern Button - Primary */
    div.stButton > button[kind="primary"] {
        font-family: 'Inter', sans-serif;
        background-color: #31E171; 
        color: #0E1117;
        border: 2px solid #1A202C;
        border-radius: 0px; 
        padding: 0.8rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 4px 4px 0px #1A202C; 
        transition: all 0.1s ease;
    }
    
    div.stButton > button[kind="primary"]:hover {
        transform: translate(2px, 2px);
        box-shadow: 2px 2px 0px #1A202C;
    }

    /* End Call Button - Secondary */
    div.stButton > button[kind="secondary"] {
        font-family: 'Inter', sans-serif;
        background-color: #F56565; /* Soft Red for ending call */
        color: #FAFAFA;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 2rem;
        text-transform: uppercase;
        font-weight: 600;
        margin-top: 1rem;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

# --- YOUR RENDER BACKEND URL ---
BACKEND_URL = "https://anytime-buddy-backend.onrender.com/api/start-conversation"

# --- SESSION STATE ---
if "conversation_url" not in st.session_state:
    st.session_state.conversation_url = None

# ==========================================
# STATE 1: THE FOCUSED LANDING PAGE
# ==========================================
if st.session_state.conversation_url is None:
    
    # Inject CSS to push the text down so it sits perfectly in the middle of the screen
    st.markdown("""
    <style>
        .block-container {
            padding-top: 10rem !important;
            max-width: 1000px !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1>You've never met<br>Shawn like this.</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>A companion that looks and feels human. Because he can finally see, hear, and emotionally understand you, all in real-time.</p>", unsafe_allow_html=True)
    
    # Use columns to perfectly center the Start button beneath the text
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("Start Conversation", type="primary", use_container_width=True):
            with st.spinner("Connecting..."):
                try:
                    response = requests.post(BACKEND_URL)
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.conversation_url = data.get("conversationUrl")
                        st.rerun() 
                    else:
                        st.error(f"Error connecting to backend: {response.text}")
                except Exception as e:
                    st.error(f"Failed to reach the server. Error: {e}")

# ==========================================
# STATE 2: THE IMMERSIVE PURE BLACK VIDEO
# ==========================================
else:
    # Inject CSS to strip away padding and force the entire app background to pure black
    st.markdown("""
    <style>
        /* Force the entire Streamlit canvas to black */
        [data-testid="stAppViewContainer"] {
            background-color: #000000 !important;
        }
        
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
            margin-top: -2rem !important;
        }
        
        /* Ensure the iframe itself is black */
        iframe {
            border: none !important;
            background-color: #000000 !important;
        }
        
        /* Make the info tip text slightly darker so it doesn't distract */
        div[data-testid="stNotification"] {
            background-color: rgba(25, 25, 25, 0.8) !important;
            color: #A0AEC0 !important;
            border: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    st.info("💡 **Tip:** Ensure your camera and microphone are allowed.")
    
    # Render the video massive 
    components.iframe(
        st.session_state.conversation_url,
        height=800,
        scrolling=False,
    )
    
    # End Call Button underneath
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("End Session", type="secondary", use_container_width=True):
            st.session_state.conversation_url = None
            st.rerun()