import streamlit as st
import random
import time
from groq import Groq

# --- 1. SECRETS & CONFIGURATION ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError):
    # Placeholder for local testing
    GROQ_API_KEY = "gsk_..." 
    # st.stop() # Uncomment this in production

client = Groq(api_key=GROQ_API_KEY)

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="Book of Answers", page_icon="🌠", layout="wide")

# --- 3. ANIMATION ENGINE (FIXED) ---
# 🛠️ BUG FIX: We generate the HTML as a single line to prevent Streamlit 
# from mistakenly treating it as a "Code Block" (the text you saw on screen).
meteor_html = ""
for i in range(25):  # Increased to 25 meteors
    top_pos = random.randint(0, 100) 
    left_pos = random.randint(0, 100) 
    delay = random.uniform(0, 10)     # Faster cycle
    duration = random.uniform(2, 4)   # Faster speed
    
    # CSS Inline string - No newlines, No indentation
    meteor_html += f'<span class="meteor" style="top: {top_pos}vh; left: {left_pos}vw; animation-delay: {delay}s; animation-duration: {duration}s;"></span>'

# --- 4. VISUALS (CSS) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Orbitron:wght@500;700&display=swap');

    /* FORCE DARK BACKGROUND */
    .stApp {{
        background: black !important; /* Pure black for contrast */
        color: #fff !important;
    }}
    
    /* Hide default elements */
    header, .stDeployButton, footer {{visibility: hidden;}}

    /* STAR ANIMATIONS */
    /* Layer 1: Small & Slow */
    .stars {{
        position: fixed; top: 0; left: 0; width: 2px; height: 2px;
        background: white;
        box-shadow: {", ".join([f"{random.randint(0, 2000)}px {random.randint(0, 2000)}px #FFF" for _ in range(400)])};
        animation: animStar 50s linear infinite;
        z-index: 0;
    }}
    
    /* Layer 2: Medium & Faster */
    .stars2 {{
        position: fixed; top: 0; left: 0; width: 3px; height: 3px;
        background: white;
        box-shadow: {", ".join([f"{random.randint(0, 2000)}px {random.randint(0, 2000)}px #FFF" for _ in range(150)])};
        animation: animStar 30s linear infinite;
        z-index: 0;
    }}

    @keyframes animStar {{
        from {{ transform: translateY(0px); opacity: 0.9; }}
        to {{ transform: translateY(-2000px); opacity: 1; }}
    }}

    /* METEORS (Shooting Stars) - BRIGHTER & THICKER */
    .meteor {{
        position: fixed;
        opacity: 0;
        width: 300px; height: 3px; /* Thicker */
        background: linear-gradient(to right, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0) 100%);
        transform: rotate(-45deg);
        z-index: 0;
        animation: meteor-fall linear infinite;
        pointer-events: none;
        box-shadow: 0 0 20px 2px #fff; /* Glow effect */
    }}

    @keyframes meteor-fall {{
        0% {{ opacity: 1; margin-top: -300px; margin-right: -300px; }}
        10% {{ opacity: 0; }}
        100% {{ opacity: 0; }}
    }}

    /* NEON TITLE */
    .neon-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 50px; /* Adjusted size for mobile/web balance */
        text-align: center;
        margin-top: 60px;
        color: #fff;
        text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #0ff, 0 0 40px #0ff;
        animation: neon-pulse 2s infinite alternate;
        position: relative;
        z-index: 2;
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
        position: relative;
        z-index: 2;
    }}
    
    /* INPUT BOX STYLING */
    .stChatInput textarea {{
        background-color: rgba(20, 20, 20, 0.8) !important;
        color: white !important;
        border: 1px solid #0ff !important;
        border-radius: 20px;
    }}

    .background-container {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: 0;
        pointer-events: none;
    }}
</style>

<div class="background-container">
    <div class="stars"></div>
    <div class="stars2"></div>
    {meteor_html}
</div>

<div class="neon-title">The Book of Answers<br><span style="font-size:24px">答案之书</span></div>
<div class="instruction-text">Type something to start... / 请输入文字开启...</div>
""", unsafe_allow_html=True)

# --- 5. LOGIC & ANSWERS ---
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