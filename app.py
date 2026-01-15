import streamlit as st
import random
import time
from groq import Groq

# --- CONFIGURATION ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except FileNotFoundError:
    st.error("API Key not found. Please set it in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# --- EXPANDED ANSWER DATABASE ---
answers = [
    # Positive / Affirmative
    "Yes / 是的", "Absolutely / 绝对是", "Count on it / 你可以指望它", "Do it / 去做吧",
    "It is certain / 这是肯定的", "The outcome will surprise you / 结果会让你惊讶",
    "It is worth the struggle / 值得去争取", "This is a sure thing / 这是一个确定的事情",
    "Go for it / 试一试", "You will succeed / 你会成功的", "Luck is on your side / 幸运女神站在你这边",
    "A definitive yes / 毫无疑问的"是"", "Signs point to yes / 迹象表明是肯定的",
    
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

# --- STREAMLIT UI SETUP ---
st.set_page_config(page_title="Book of Answers", page_icon="📖")

# Custom CSS for magical starry night theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Great+Vibes&family=Cinzel:wght@400;600&display=swap');
    
    /* Background and Stars */
    .stApp {
        background: linear-gradient(to bottom, #000000 0%, #0a0e27 50%, #1a1a2e 100%);
        color: #FAFAFA;
        overflow: hidden;
        position: relative;
    }
    
    /* Starfield Container */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Twinkling Stars */
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2); }
    }
    
    @keyframes twinkle-slow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    @keyframes twinkle-fast {
        0%, 100% { opacity: 0.2; }
        50% { opacity: 0.9; }
    }
    
    /* Shooting Stars */
    @keyframes shooting-star {
        0% {
            transform: translateX(0) translateY(0);
            opacity: 1;
        }
        100% {
            transform: translateX(-300px) translateY(300px);
            opacity: 0;
        }
    }
    
    .shooting-star {
        position: fixed;
        width: 2px;
        height: 2px;
        background: white;
        border-radius: 50%;
        box-shadow: 0 0 10px 2px rgba(255, 255, 255, 0.8);
        z-index: 1;
        animation: shooting-star 1.5s linear;
    }
    
    .shooting-star::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 80px;
        height: 2px;
        background: linear-gradient(to right, rgba(255, 255, 255, 0.8), transparent);
        transform: translateX(-80px);
    }
    
    /* Neon Title Animation */
    @keyframes neon-glow {
        0%, 100% { 
            color: #ff00ff;
            text-shadow: 0 0 10px #ff00ff, 0 0 20px #ff00ff, 0 0 30px #ff00ff, 0 0 40px #ff1493;
        }
        25% { 
            color: #00ffff;
            text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff, 0 0 30px #00ffff, 0 0 40px #00bfff;
        }
        50% { 
            color: #ffff00;
            text-shadow: 0 0 10px #ffff00, 0 0 20px #ffff00, 0 0 30px #ffff00, 0 0 40px #ffd700;
        }
        75% { 
            color: #00ff00;
            text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00, 0 0 30px #00ff00, 0 0 40px #32cd32;
        }
    }
    
    h1 {
        font-family: 'Great Vibes', cursive !important;
        font-size: 3.5rem !important;
        text-align: center !important;
        animation: neon-glow 8s infinite !important;
        margin-bottom: 1rem !important;
        position: relative;
        z-index: 10;
    }
    
    /* Subtitle styling */
    .subtitle {
        font-family: 'Cinzel', serif;
        font-size: 1.2rem;
        text-align: center;
        color: #d4af37;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
        margin-bottom: 2rem;
        position: relative;
        z-index: 10;
    }
    
    /* Chat Input */
    .stChatInput > div {
        background-color: rgba(38, 39, 48, 0.8) !important;
        border: 2px solid #d4af37 !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 10;
    }
    
    .stChatInput input {
        font-family: 'Great Vibes', cursive !important;
        font-size: 1.3rem !important;
        color: #d4af37 !important;
    }
    
    .stChatInput input::placeholder {
        font-family: 'Great Vibes', cursive !important;
        color: rgba(212, 175, 55, 0.5) !important;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background-color: rgba(38, 39, 48, 0.7) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 15px !important;
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 10;
    }
    
    /* Answer Card */
    .answer-card {
        padding: 25px;
        border-radius: 15px;
        background: linear-gradient(135deg, rgba(38, 39, 48, 0.9) 0%, rgba(26, 26, 46, 0.9) 100%);
        border: 2px solid #d4af37;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.3);
        position: relative;
        z-index: 10;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #d4af37 !important;
    }
    
    /* All text elements */
    div[data-testid="stChatMessageContent"] {
        position: relative;
        z-index: 10;
    }
</style>

<script>
// Create starfield
function createStars() {
    const container = document.querySelector('.stApp');
    if (!container) return;
    
    // Create stars
    for (let i = 0; i < 200; i++) {
        const star = document.createElement('div');
        const size = Math.random() * 3 + 1;
        const x = Math.random() * 100;
        const y = Math.random() * 100;
        const duration = Math.random() * 3 + 2;
        const delay = Math.random() * 5;
        const animations = ['twinkle', 'twinkle-slow', 'twinkle-fast'];
        const animation = animations[Math.floor(Math.random() * animations.length)];
        
        star.style.cssText = `
            position: fixed;
            width: ${size}px;
            height: ${size}px;
            background: white;
            border-radius: 50%;
            left: ${x}%;
            top: ${y}%;
            box-shadow: 0 0 ${size * 2}px ${size / 2}px rgba(255, 255, 255, 0.8);
            animation: ${animation} ${duration}s infinite;
            animation-delay: ${delay}s;
            z-index: 1;
            pointer-events: none;
        `;
        container.appendChild(star);
    }
}

// Create shooting stars
function createShootingStar() {
    const container = document.querySelector('.stApp');
    if (!container) return;
    
    const star = document.createElement('div');
    star.className = 'shooting-star';
    star.style.left = Math.random() * 100 + '%';
    star.style.top = Math.random() * 50 + '%';
    container.appendChild(star);
    
    setTimeout(() => star.remove(), 1500);
}

// Initialize
setTimeout(() => {
    createStars();
    
    // Random shooting stars (1-5 every few seconds)
    setInterval(() => {
        const count = Math.floor(Math.random() * 5) + 1;
        for (let i = 0; i < count; i++) {
            setTimeout(() => createShootingStar(), Math.random() * 2000);
        }
    }, 3000);
}, 100);
</script>
""", unsafe_allow_html=True)

st.title("📖 𝓣𝓱𝓮 𝓑𝓸𝓸𝓴 𝓸𝓯 𝓐𝓷𝓼𝔀𝓮𝓻𝓼 / 答案之书")
st.markdown("<div class='subtitle'>𝓕𝓸𝓬𝓾𝓼 𝓸𝓷 𝔂𝓸𝓾𝓻 𝓺𝓾𝓮𝓼𝓽𝓲𝓸𝓷... 请在心中默念你的问题... ✨</div>", unsafe_allow_html=True)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- MAIN LOGIC ---
if prompt := st.chat_input("𝓣𝔂𝓹𝓮 𝓼𝓸𝓶𝓮𝓽𝓱𝓲𝓷𝓰 𝓽𝓸 𝓼𝓽𝓪𝓻𝓽 / 在此输入你的问题..."):
    
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. The Logic
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Simulate "Focusing"
        with st.spinner("✨ 𝓒𝓸𝓷𝓼𝓾𝓵𝓽𝓲𝓷𝓰 𝓽𝓱𝓮 𝓼𝓽𝓪𝓻𝓼... / 正在连接宇宙能量..."):
            time.sleep(1.5) 
            
            # Get Random Answer
            random_answer = random.choice(answers)
            
            # LLM Analysis
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