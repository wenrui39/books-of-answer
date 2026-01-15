import streamlit as st
import random
import time
from groq import Groq

# --- 1. CONFIGURATION ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError):
    # Fallback for local testing
    GROQ_API_KEY = "gsk_..." # Put your key here for local testing
    # st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="Book of Answers", page_icon="🌠", layout="wide")

# --- 3. INJECT THE NEW BACKGROUND (HTML + CONVERTED CSS) ---
# Note: We put the CSS and HTML in one block to ensure no indentation bugs.
st.markdown("""
<style>
    /* --- 1. RESET & FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@10..48,200;10..48,300;10..48,400;10..48,500;10..48,600;10..48,700;10..48,800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Great+Vibes&display=swap');

    :root {
        --animation-options: 24s infinite linear alternate;
        --star-dimensions: 1.77; /* Aspect ratio roughly */
    }

    /* --- 2. STREAMLIT OVERRIDES (Force Transparent) --- */
    .stApp {
        background: transparent !important;
    }
    header, footer, .stDeployButton {
        display: none !important;
    }

    /* --- 3. BACKGROUND CONTAINER --- */
    #starry-section {
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        z-index: -1; /* Puts it behind the chat */
        background: linear-gradient(150deg, #0f172a, #1c1917);
        overflow: hidden;
        display: grid;
        grid-template-areas: "Stack";
    }

    /* --- 4. STARS (Converted from SCSS Loop) --- */
    .starry-section--background--stars {
        grid-area: Stack;
        position: absolute;
        animation: moveStars var(--animation-options);
        /* Use CSS variables for offset logic */
        width: auto; height: auto;
    }

    /* Specific offsets for the 3 layers */
    #stars1 { 
        --star-offset: 120vh; 
        height: calc(100vh + 120vh); 
        transform: translate(0, -50%); 
        /* Simplified positioning for CSS */
        top: -60vh; left: -50vw;
    }
    #stars2 { 
        --star-offset: 180vh; 
        height: calc(100vh + 180vh); 
        top: -90vh; left: -50vw;
    }
    #stars3 { 
        --star-offset: 240vh; 
        height: calc(100vh + 240vh); 
        top: -120vh; left: -50vw;
    }

    /* --- 5. ICONS (UFO, PLANET, METEORS) --- */
    .icon {
        position: absolute;
        z-index: 2;
        color: white; /* Fallback */
    }

    .icon.ufo {
        animation: moveUfo var(--animation-options);
        height: 9vh;
        top: 5vh; left: 0;
    }

    .icon.planet {
        animation: movePlanet var(--animation-options);
        height: 24vh;
        bottom: 5vh; left: 0;
    }
    
    .icon.meteor {
        animation: moveMeteor var(--animation-options);
        height: 6vh;
    }
    
    /* Meteor Positioning */
    .icon.meteor1 { right: 0; top: 10vh; animation-delay: 0s; }
    .icon.meteor2 { right: 10vw; top: 40vh; animation-delay: 5s; }
    .icon.meteor3 { right: 20vw; top: 20vh; animation-delay: 10s; }

    /* --- 6. KEYFRAME ANIMATIONS --- */
    @keyframes moveStars {
        0% { transform: translateX(-10vw); }
        100% { transform: translateX(10vw); }
    }

    @keyframes moveUfo {
        0% { transform: translateX(110vw); }
        100% { transform: translateX(-20vw); }
    }

    @keyframes movePlanet {
        0% { transform: translateX(-20vw); }
        100% { transform: translateX(90vw); }
    }

    @keyframes moveMeteor {
        0%, 60% { transform: translateX(20vw) translateY(-20vh); opacity: 1; }
        80%, 100% { transform: translateX(-50vw) translateY(50vh); opacity: 0; }
    }

    /* --- 7. YOUR ORIGINAL NEON TITLE --- */
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 60px;
        text-align: center;
        text-transform: uppercase;
        margin-top: 10vh;
        color: #fff;
        text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 40px #0ff, 0 0 80px #0ff;
        animation: neon-color-cycle 5s infinite alternate;
        position: relative; z-index: 10;
    }

    @keyframes neon-color-cycle {
        0% { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 40px #f09, 0 0 80px #f09; }
        33% { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 40px #0ff, 0 0 80px #0ff; }
        66% { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 40px #0f0, 0 0 80px #0f0; }
        100% { text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 40px #ff0, 0 0 80px #ff0; }
    }

    .instruction-text {
        font-family: 'Great Vibes', cursive;
        font-size: 35px;
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
        margin-top: -10px;
        margin-bottom: 30px;
        position: relative; z-index: 10;
    }

    /* Chat Styling */
    .stChatInput textarea {
        background-color: rgba(0, 0, 0, 0.7) !important;
        color: white !important;
        border: 1px solid #0ff !important;
    }
    .stChatMessage {
        background-color: rgba(0,0,0,0.5);
        border-radius: 10px;
        position: relative; z-index: 5;
    }
</style>

<div id="starry-section">
<img class="starry-section--background--stars" id="stars1" src="https://cdn.jsdelivr.net/gh/KyleSchullerDEV/CodePenStorage/images/starry.svg">
<img class="starry-section--background--stars" id="stars2" src="https://cdn.jsdelivr.net/gh/KyleSchullerDEV/CodePenStorage/images/starry.svg">
<img class="starry-section--background--stars" id="stars3" src="https://cdn.jsdelivr.net/gh/KyleSchullerDEV/CodePenStorage/images/starry.svg">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 512" class="icon ufo"><path fill="currentColor" d="M320 288c124.2 0 176-50.9 176-50.9c0-8.3-.6-16.5-1.7-24.5C582 235.5 640 275 640 320c0 70.7-143.3 128-320 128S0 390.7 0 320c0-45 58-84.5 145.7-107.4c-1.2 8-1.7 16.2-1.7 24.5c0 0 51.8 50.9 176 50.9zm24 88a24 24 0 1 0 -48 0 24 24 0 1 0 48 0zM128 352a24 24 0 1 0 0-48 24 24 0 1 0 0 48zm408-24a24 24 0 1 0 -48 0 24 24 0 1 0 48 0z"/><path fill="#7dd3fc" opacity="0.4" d="M496 237.1s-51.8 50.9-176 50.9s-176-50.9-176-50.9C144 141.5 222.8 64 320 64s176 77.5 176 173.1z"/></svg>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="icon planet"><path fill="#c2410c" d="M408.3 114.3C370.3 73.5 316.1 48 256 48C141.1 48 48 141.1 48 256c0 60.1 25.5 114.3 66.3 152.3c58.5-37.6 111.3-85 160.1-133.8s96.3-101.7 133.8-160.1zm38 57.5c-32.6 46-75.8 97.1-126.6 147.9s-101.8 94-147.9 126.6C197.6 457.7 226 464 256 464c114.9 0 208-93.1 208-208c0-30-6.3-58.4-17.7-84.2z"/><path fill="#fb923c" d="M503.9 8.1c35.2 35.2-47.3 174.7-184.2 311.6S43.3 539.1 8.1 503.9c-22.1-22.1 2.3-85.6 57.6-163.7c9.1 20.7 21.8 40.2 38 57.5c-5.7 8.8-11.1 17.8-16.3 26.9c69.3-39.6 130.8-94 187-150.1s110.6-117.7 150.1-187c-9.1 5.2-18 10.6-26.9 16.3c-17.4-16.2-36.9-28.9-57.5-38C418.3 10.4 481.7-14 503.9 8.1z"/></svg>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="icon meteor meteor1"><path fill="#ef4444" d="M64 320a128 128 0 1 1 256 0A128 128 0 1 1 64 320zm128-32a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zm16 96a16 16 0 1 0 0-32 16 16 0 1 0 0 32z"/><path fill="#fde047" d="M493.7 .9L299.4 75.6l2.3-29.3c1-12.8-12.8-21.5-24-15.1L101.3 133.4C38.6 169.7 0 236.6 0 309C0 421.1 90.9 512 203 512c72.4 0 139.4-38.6 175.7-101.3L480.8 234.3c6.5-11.1-2.2-25-15.1-24l-29.3 2.3L511.1 18.3c.6-1.5 .9-3.2 .9-4.8C512 6 506 0 498.5 0c-1.7 0-3.3 .3-4.8 .9zM192 192a128 128 0 1 1 0 256 128 128 0 1 1 0-256z"/></svg>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="icon meteor meteor2"><path fill="#ef4444" d="M64 320a128 128 0 1 1 256 0A128 128 0 1 1 64 320zm128-32a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zm16 96a16 16 0 1 0 0-32 16 16 0 1 0 0 32z"/><path fill="#fde047" d="M493.7 .9L299.4 75.6l2.3-29.3c1-12.8-12.8-21.5-24-15.1L101.3 133.4C38.6 169.7 0 236.6 0 309C0 421.1 90.9 512 203 512c72.4 0 139.4-38.6 175.7-101.3L480.8 234.3c6.5-11.1-2.2-25-15.1-24l-29.3 2.3L511.1 18.3c.6-1.5 .9-3.2 .9-4.8C512 6 506 0 498.5 0c-1.7 0-3.3 .3-4.8 .9zM192 192a128 128 0 1 1 0 256 128 128 0 1 1 0-256z"/></svg>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" class="icon meteor meteor3"><path fill="#ef4444" d="M64 320a128 128 0 1 1 256 0A128 128 0 1 1 64 320zm128-32a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zm16 96a16 16 0 1 0 0-32 16 16 0 1 0 0 32z"/><path fill="#fde047" d="M493.7 .9L299.4 75.6l2.3-29.3c1-12.8-12.8-21.5-24-15.1L101.3 133.4C38.6 169.7 0 236.6 0 309C0 421.1 90.9 512 203 512c72.4 0 139.4-38.6 175.7-101.3L480.8 234.3c6.5-11.1-2.2-25-15.1-24l-29.3 2.3L511.1 18.3c.6-1.5 .9-3.2 .9-4.8C512 6 506 0 498.5 0c-1.7 0-3.3 .3-4.8 .9zM192 192a128 128 0 1 1 0 256 128 128 0 1 1 0-256z"/></svg>
</div>
""", unsafe_allow_html=True)

# --- 4. TITLE & INSTRUCTION ---
st.markdown('<div class="neon-title">The Book of Answers<br><span style="font-size:24px">答案之书</span></div>', unsafe_allow_html=True)
st.markdown('<div class="instruction-text">Type something to start... / 请输入文字开启...</div>', unsafe_allow_html=True)

# --- 5. CHAT LOGIC ---
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