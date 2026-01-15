import streamlit as st
import random
import time
from groq import Groq

# --- 1. SECRETS & CONFIGURATION ---
try:
    # This matches the key name in your Streamlit Cloud "Secrets" settings
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError):
    # Fallback for local testing if secrets.toml is missing
    # st.warning("Secrets not found, using placeholder key for testing...")
    GROQ_API_KEY = "gsk_..." # You can leave this blank if you only run on cloud
    st.stop() # Stop if no key found to prevent errors

client = Groq(api_key=GROQ_API_KEY)

# --- 2. PAGE SETUP ---
st.set_page_config(page_title="Book of Answers", page_icon="🌠", layout="wide")

# --- 3. ANIMATION ENGINE (Python Side) ---
# We generate the HTML for meteors here to keep the main markdown clean
meteor_html = ""
for i in range(20):  # Increased to 20 meteors for more visibility
    top_pos = random.randint(0, 100)  # Percentage for responsiveness
    left_pos = random.randint(0, 100) # Percentage
    delay = random.uniform(0, 15)     
    duration = random.uniform(2, 5)   
    
    # We use 'vh' and 'vw' in CSS, but generate random values here
    meteor_html += f"""
    <span class="meteor" style="top: {top_pos}vh; left: {left_pos}vw; animation-delay: {delay}s; animation-duration: {duration}s;"></span>
    """

# --- 4. CSS & VISUALS ---
st.markdown(f"""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Orbitron:wght@500;700&display=swap');

    /* FORCE DARK BACKGROUND (Crucial Fix) */
    .stApp {{
        background: radial-gradient(ellipse at bottom, #1b2735 0%, #090a0f 100%) !important;
        background-attachment: fixed !important;
        color: #fff !important;
    }}

    /* HIDE STREAMLIT HEADER/FOOTER FOR IMMERSION */
    header {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    footer {{visibility: hidden;}}

    /* STAR LAYER 1 (Small) */
    .stars {{
        position: fixed; top: 0; left: 0; width: 1px; height: 1px;
        background: transparent;
        box-shadow: {", ".join([f"{random.randint(0, 2000)}px {random.randint(0, 2000)}px #FFF" for _ in range(700)])};
        animation: animStar 50s linear infinite;
        z-index: 0; /* Behind text, in front of background */
    }}
    .stars:after {{
        content: " "; position: absolute; top: 2000px; width: 1px; height: 1px; 
        background: transparent;
        box-shadow: {", ".join([f"{random.randint(0, 2000)}px {random.randint(0, 2000)}px #FFF" for _ in range(700)])};
    }}

    /* STAR LAYER 2 (Medium) */
    .stars2 {{
        position: fixed; top: 0; left: 0; width: 2px; height: 2px;
        background: transparent;
        box-shadow: {", ".join([f"{random.randint(0, 2000)}px {random.randint(0, 2000)}px #FFF" for _ in range(200)])};
        animation: animStar 100s linear infinite;
        z-index: 0;
    }}
    
    /* STAR LAYER 3 (Large) */
    .stars3 {{
        position: fixed; top: 0; left: 0; width: 3px; height: 3px;
        background: transparent;
        box-shadow: {", ".join([f"{random.randint(0, 2000)}px {random.randint(0, 2000)}px #FFF" for _ in range(100)])};
        animation: animStar 150s linear infinite;
        z-index: 0;
    }}

    /* METEORS */
    .meteor {{
        position: fixed; /* Fixed to screen, not scroll */
        opacity: 0;
        width: 300px; height: 2px; /* Longer tail */
        background: linear-gradient(to right, rgba(255, 255, 255, 1) 0%, rgba(255, 255, 255, 0) 100%);
        transform: rotate(-45deg);
        z-index: 0;
        animation: meteor 5s linear infinite;
        pointer-events: none; /* Let clicks pass through */
    }}

    /* ANIMATIONS */
    @keyframes animStar {{
        from {{ transform: translateY(0px); }}
        to {{ transform: translateY(-2000px); }}
    }}

    @keyframes meteor {{
        0% {{ opacity: 1; margin-top: -300px; margin-right: -300px; }}
        12% {{ opacity: 0; }}
        100% {{ opacity: 0; }}
    }}

    /* NEON TEXT */
    .neon-title {{
        font-family: 'Orbitron', sans-serif;
        font-size: 60px;
        text-align: center;
        margin-top: 50px;
        color: #fff;
        text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 40px #0ff, 0 0 80px #0ff;
        animation: neon-pulse 1.5s infinite alternate;
        position: relative;
        z-index: 1; /* Above stars */
    }}

    @keyframes neon-pulse {{
        from {{ text-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 40px #0ff; }}
        to {{ text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #0ff; }}
    }}

    .instruction-text {{
        font-family: 'Great Vibes', cursive;
        font-size: 40px;
        color: rgba(255, 255, 255, 0.9);
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        z-index: 1;
    }}

    /* CHAT INPUT STYLING */
    .stChatInput textarea {{
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: white !important;
        border: 1px solid #0ff !important;
    }}
    
    /* BACKGROUND CONTAINER */
    .background-container {{
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        z-index: 0;
        pointer-events: none;
    }}
    
    /* Fix Chat Messages Visibility */
    .stChatMessage {{
        background-color: rgba(0,0,0,0.4);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
    }}
</style>

<div class="background-container">
    <div class="stars"></div>
    <div class="stars2"></div>
    <div class="stars3"></div>
    {meteor_html}
</div>

<div class="neon-title">The Book of Answers<br><span style="font-size:30px">答案之书</span></div>
<div class="instruction-text">Focus on your question... / 请在心中默念...</div>
""", unsafe_allow_html=True)

# --- 5. LOGIC & ANSWERS ---

answers = [
    # Positive / Affirmative
    "Yes / 是的", "Absolutely / 绝对是", "Count on it / 你可以指望它", "Do it / 去做吧",
    "It is certain / 这是肯定的", "The outcome will surprise you / 结果会让你惊讶",
    "It is worth the struggle / 值得去争取", "This is a sure thing / 这是一个确定的事情",
    "Go for it / 试一试", "You will succeed / 你会成功的", "Luck is on your side / 幸运女神站在你这边",
    "A definitive yes / 毫无疑问的“是”", "Signs point to yes / 迹象表明是肯定的",
    
    # Negative / Cautionary
    "No / 不", "Don't bet on it / 不要押注于此", "You will regret it / 你会后悔的",
    "Absolutely not / 绝不", "Stop / 停下", "Not yet / 还没到时候",
    "Don't ignore the obvious / 别忽视显而易见的事", "It's a trap / 这是一个陷阱",
    "Better not / 最好不要", "The answer is no / 答案是否定的",
    
    # Timing / Patience
    "Wait / 等待", "Not the right time / 现在不是时候", "Ask again later / 稍后再问",
    "Be patient / 保持耐心", "Don't wait / 不要等待", "It will pass / 它会过去的",
    "Time will tell / 时间会证明一切", "In a year / 一年之内",
    
    # Introspective / Spiritual
    "Follow your intuition / 跟随你的直觉", "Focus on your family / 专注于你的家庭",
    "Let it go / 放手", "Trust your first thought / 相信你最初的想法",
    "You need more information / 你需要更多信息", "Remove your own obstacles / 清除你自己的障碍",
    "Accept the change / 接受改变", "Reconsider / 重新考虑",
    "Keep it to yourself / 保守秘密", "Look within / 向内探索",
    "Listen to your heart / 倾听你的心声", "Respect the rules / 遵守规则",
    "Forgive / 原谅", "Let the past go / 让过去过去",
    
    # Action Oriented
    "Only if you do it now / 只有现在做才可以", "Take charge / 掌握主动权",
    "Work harder / 更努力一点", "Get advice from a friend / 像朋友寻求建议",
    "Make a list of why / 列出原因", "Save your energy / 节省你的精力",
    "Act as if it is already real / 假装它已经成真",
    
    # Cryptic / Mysterious
    "A year from now it won't matter / 一年后这都不重要了",
    "You already know the answer / 你其实已经知道答案了",
    "See it differently / 换个角度看", "Maybe / 也许"
]


# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle Input
if prompt := st.chat_input("Type your question here / 在此输入你的问题..."):
    
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. The Logic (Replicating n8n nodes)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Simulate "Focusing" (The Wait Node in n8n)
        with st.spinner("Consulting the spirits... / 正在连接命运..."):
            time.sleep(1.5) 
            
            # Step A: Get Random Answer (The Python Code Node)
            random_answer = random.choice(answers)
            
            # Step B: LLM Analysis (The AI Agent Node)
            # Replicating the exact system prompt from your n8n workflow
            system_prompt = f"""
            You are the "Oracle Interpreter" (命运解读者).
            Your task is to take the user's [Question] and the random [Book Answer] they received, and generate a spiritual analysis report.

            ### GUIDELINES (准则)
            1. **Language:** Every section must be bilingual (English first, then Chinese).
            2. **Tone:** Mystical but simple, gentle, and healing. Do not use complex words. (神秘但通俗易懂，温柔且治愈).
            3. **Analysis Logic:**
               - Connect the specific Question to the abstract Answer.
               - If the answer is negative, give advice on caution.
               - If the answer is positive, give encouragement.
               - If the answer is vague, advise them to listen to their heart.

            ### REPORT FORMAT (Strictly follow this Markdown structure)

            🔮 **ORACLE ANALYSIS REPORT / 命运启示录**

            ━━━━━━━━━━━━━━━━━━

            ❓ **The Question / 你的困惑:**
            {prompt}

            ✨ **The Answer / 指引:**
            # **{random_answer}**

            📜 **Deep Interpretation / 深度解析:**
            [Write 2-3 short sentences explaining what this answer means for their specific situation. Be supportive.]
            [用2-3句简短的话解释这个答案对他们的情况意味着什么。保持支持的态度。]

            ━━━━━━━━━━━━━━━━━━

            🍀 *Trust the process. / 相信命运的安排。*
            """

            try:
                # Call Groq API
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"User Question: {prompt}\nBook Answer: {random_answer}"}
                    ],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7,
                )
                
                full_response = chat_completion.choices[0].message.content
                
                # Display Result
                message_placeholder.markdown(full_response)
                
                # Save to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"The spirits are silent (Error): {e}")