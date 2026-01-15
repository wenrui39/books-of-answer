import streamlit as st
import random
import time
from groq import Groq

# --- 1. CONFIGURATION ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError):
    # Placeholder for local testing
    GROQ_API_KEY = "gsk_..." 
    # st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="Book of Answers", page_icon="🌠", layout="wide")

# --- 3. INJECT CUSTOM HTML BACKGROUND ---
# This is the content from your 'html.html' file, optimized for Streamlit
# We use standard <img> tags for the stars and inline SVGs for the icons.
background_html = """
<div id="starry-section--background" aria-hidden="true">
    <img class="starry-section--background--stars" id="stars1" src="https://cdn.jsdelivr.net/gh/KyleSchullerDEV/CodePenStorage/images/starry.svg">
    <img class="starry-section--background--stars" id="stars2" src="https://cdn.jsdelivr.net/gh/KyleSchullerDEV/CodePenStorage/images/starry.svg">
    <img class="starry-section--background--stars" id="stars3" src="https://cdn.jsdelivr.net/gh/KyleSchullerDEV/CodePenStorage/images/starry.svg">
    
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512" class="icon ufo">
        <path fill="currentColor" d="M320 288c124.2 0 176-50.9 176-50.9c0-8.3-.6-16.5-1.7-24.5C582 235.5 640 275 640 320c0 70.7-143.3 128-320 128S0 390.7 0 320c0-45 58-84.5 145.7-107.4c-1.2 8-1.7 16.2-1.7 24.5c0 0 51.8 50.9 176 50.9zm24 88a24 24 0 1 0 -48 0 24 24 0 1 0 48 0zM128 352a24 24 0 1 0 0-48 24 24 0 1 0 0 48zm408-24a24 24 0 1 0 -48 0 24 24 0 1 0 48 0z"/><path fill="#7dd3fc" opacity="0.4" d="M496 237.1s-51.8 50.9-176 50.9s-176-50.9-176-50.9C144 141.5 222.8 64 320 64s176 77.5 176 173.1z"/>
    </svg>
    
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="icon planet">
        <path fill="#c2410c" d="M408.3 114.3C370.3 73.5 316.1 48 256 48C141.1 48 48 141.1 48 256c0 60.1 25.5 114.3 66.3 152.3c58.5-37.6 111.3-85 160.1-133.8s96.3-101.7 133.8-160.1zm38 57.5c-32.6 46-75.8 97.1-126.6 147.9s-101.8 94-147.9 126.6C197.6 457.7 226 464 256 464c114.9 0 208-93.1 208-208c0-30-6.3-58.4-17.7-84.2z"/><path fill="#fb923c" d="M503.9 8.1c35.2 35.2-47.3 174.7-184.2 311.6S43.3 539.1 8.1 503.9c-22.1-22.1 2.3-85.6 57.6-163.7c9.1 20.7 21.8 40.2 38 57.5c-5.7 8.8-11.1 17.8-16.3 26.9c69.3-39.6 130.8-94 187-150.1s110.6-117.7 150.1-187c-9.1 5.2-18 10.6-26.9 16.3c-17.4-16.2-36.9-28.9-57.5-38C418.3 10.4 481.7-14 503.9 8.1z"/>
    </svg>
</div>
"""

# --- 4. INJECT CSS STYLES ---
# This is your 'cssdesign.css' CONVERTED from SCSS to standard CSS
# I also adjusted 'z-index' and 'position' so it stays behind your chat app.
st.markdown(f"""
<style>
    /* 1. IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Orbitron:wght@500;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@10..48,200..800&display=swap');

    /* 2. RESET STREAMLIT DEFAULTS */
    .stApp {{
        background: transparent !important;
    }}
    header, .stDeployButton, footer {{visibility: hidden;}}

    /* 3. BACKGROUND CONTAINER STYLE */
    #starry-section--background {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: linear-gradient(150deg, #0f172a, #1c1917);
        overflow: hidden;
        z-index: -1; /* Puts it BEHIND the chat */
        display: grid;
        place-items: center;
        grid-template-areas: "StarStack";
    }}
    
    #starry-section--background > * {{
        grid-area: StarStack;
    }}

    /* 4. STARS ANIMATION */
    .starry-section--background--stars {{
        /* Calculated from your SCSS variables */
        --stars-dimensions: 1.77; 
        width: 100vw; 
        height: auto;
        min-height: 100vh;
        object-fit: cover;
        opacity: 0.7;
    }}

    /* Individual Star Layers with offsets */
    #stars1 {{
        --star-offset: 120vh;
        animation: moveStars 40s infinite linear alternate;
    }}
    #stars2 {{
        --star-offset: 180vh;
        animation: moveStars 45s infinite linear alternate;
        opacity: 0.5;
    }}
    #stars3 {{
        --star-offset: 240vh;
        animation: moveStars 50s infinite linear alternate;
        opacity: 0.3;
    }}

    @keyframes moveStars {{
        0% {{ transform: translateX(-10%); }}
        100% {{ transform: translateX(10%); }}
    }}

    /* 5. ICONS ANIMATION (UFO & PLANET) */
    .icon {{
        color: white;
        z-index: 2;
        position: absolute;
    }}

    /* UFO Style */
    .icon.ufo {{
        width: 80px;
        top: 10vh;
        animation: moveUfo 24s infinite linear alternate;
    }}

    /* Planet Style */
    .icon.planet {{
        width: 150px;
        bottom: 5vh;
        animation: movePlanet 30s infinite linear alternate;
    }}

    @keyframes moveUfo {{
        0% {{ transform: translateX(120vw); }}
        100% {{ transform: translateX(-120vw); }}
    }}

    @keyframes movePlanet {{
        0% {{ transform: translateX(-80vw) rotate(0deg); }}
        100% {{ transform: translateX(80vw) rotate(20deg); }}
    }}

    /* 6. NEON TEXT STYLES (Kept from your original request) */
    .neon-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 50px;
        text-align: center;
        margin-top: 60px;
        color: #fff;
        text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #0ff, 0 0 40px #0ff;
        animation: neon-pulse 2s infinite alternate;
    }}
    
    @keyframes neon-pulse {{
        from {{ text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #0ff; opacity: 1; }}
        to {{ text-shadow: 0 0 2px #fff, 0 0 5px #fff, 0 0 10px #0ff; opacity: 0.8; }}
    }}

    .instruction-text {{
        font-family: 'Great Vibes', cursive;
        font-size: 30px;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin-bottom: 20px;
    }}
    
    /* Input Box Styling */
    .stChatInput textarea {{
        background-color: rgba(20, 20, 20, 0.8) !important;
        color: white !important;
        border: 1px solid #0ff !important;
        border-radius: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# --- 5. RENDER BACKGROUND ---
st.markdown(background_html, unsafe_allow_html=True)

# --- 6. TITLE & LOGIC ---
st.markdown('<div class="neon-title">The Book of Answers<br><span style="font-size:24px">答案之书</span></div>', unsafe_allow_html=True)
st.markdown('<div class="instruction-text">Type something to start... / 请输入文字开启...</div>', unsafe_allow_html=True)

# --- ANSWERS LOGIC ---
answers = [
    "Yes / 是的", "Absolutely / 绝对是", "Count on it / 你可以指望它", 
    "It is certain / 这是肯定的", "The outcome will surprise you / 结果会让你惊讶",
    "Go for it / 试一试", "You will succeed / 你会成功的", 
    "No / 不", "Don't bet on it / 不要押注于此", "You will regret it / 你会后悔的",
    "Stop / 停下", "Wait / 等待", "Not the right time / 现在不是时候",
    "Follow your intuition / 跟随你的直觉", "Let it go / 放手", 
    "Listen to your heart / 倾听你的心声"
]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask the stars / 向星空提问..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Connecting..."):
            time.sleep(1.5)
        
        random_answer = random.choice(answers)
        
        system_prompt = f"""
        You are the "Star Oracle". 
        User Question: {prompt}
        Oracle Answer: {random_answer}
        
        Output format:
        🔮 **ORACLE ANALYSIS / 星际启示**
        ━━━━━━━━━━━━━━━━━━
        ✨ **The Answer:** # **{random_answer}**
        📜 **Interpretation:** [Bilingual interpretation, mystical but clear]
        ━━━━━━━━━━━━━━━━━━
        🍀 *Trust the stars.*
        """

        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "system", "content": system_prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
            )
            full_response = chat_completion.choices[0].message.content
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Error: {e}")