import streamlit as st
import random
import time
from groq import Groq

# --- 1. SETUP & CONFIGURATION ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except (FileNotFoundError, KeyError):
    GROQ_API_KEY = "gsk_..." 
    # st.warning("Using placeholder key for local testing.") 

client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="The Book of Answers", page_icon="🌠", layout="wide")

# --- 2. INJECT CSS (From Part 1) ---
if 'css_code' not in locals():
    css_code = """<style>
    /* --- 1. GLOBAL RESETS & FONTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@10..48,200;10..48,800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Great+Vibes&display=swap');

    :root {
        --animation-speed: 24s;
    }

    /* 强制覆盖 Streamlit 默认样式，消除白边和滚动条 */
    .stApp {
        background: transparent !important;
    }
    header, footer, .stDeployButton {
        display: none !important;
    }
    
    /* 修复 Streamlit 的容器内边距干扰 */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* --- 2. THE STARRY STAGE (背景容器) --- */
    #starry-section {
        position: fixed;
        inset: 0; /* Top/Left/Right/Bottom = 0 */
        width: 100vw;
        height: 100vh;
        background: linear-gradient(150deg, #0f172a, #1c1917); /* 原版深色渐变 */
        overflow: hidden;
        z-index: -1; /* 确保在最底层 */
        perspective: 1000px; /* 增加 3D 深度感 */
    }

    /* --- 3. STARS PARALLAX (星星视差系统) --- */
    /* 这里的计算还原了 SCSS 中的 offset 逻辑 */
    
    .star-layer {
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        width: 150vmax; /* 确保足够大以覆盖旋转和移动 */
        height: 150vmax;
        opacity: 0.8;
        pointer-events: none;
    }

    /* 第1层星星：最远，移动最慢 */
    #stars1 {
        z-index: 1;
        width: 120vw; 
        height: 120vh;
        /* SCSS Logic: offset base 120vh */
        animation: moveStars var(--animation-speed) linear infinite alternate;
    }

    /* 第2层星星：中间，稍快 */
    #stars2 {
        z-index: 2;
        width: 140vw; 
        height: 140vh;
        opacity: 0.6;
        animation: moveStars calc(var(--animation-speed) * 0.8) linear infinite alternate-reverse;
    }

    /* 第3层星星：最近，最快，产生深度 */
    #stars3 {
        z-index: 3;
        width: 160vw; 
        height: 160vh;
        opacity: 0.4;
        animation: moveStars calc(var(--animation-speed) * 0.6) linear infinite alternate;
    }

    @keyframes moveStars {
        0% { transform: translate(-50%, -50%) translateX(-5vw) translateY(-2vh); }
        100% { transform: translate(-50%, -50%) translateX(5vw) translateY(2vh); }
    }

    /* --- 4. ICONS & OBJECTS (UFO, PLANET, METEORS) --- */
    .icon-svg {
        position: absolute;
        z-index: 5;
    }

    /* UFO: 左右漂浮 */
    .ufo {
        width: 120px;
        top: 10%;
        left: -150px; /* Start off screen */
        filter: drop-shadow(0 0 10px rgba(125, 211, 252, 0.5));
        animation: moveUfo 20s linear infinite alternate;
    }

    /* Planet: 底部缓慢旋转/移动 */
    .planet {
        width: 300px;
        bottom: -50px;
        left: -100px;
        filter: drop-shadow(0 0 20px rgba(194, 65, 12, 0.4));
        animation: movePlanet 40s linear infinite alternate;
        z-index: 4;
    }

    /* Meteors: 修复卡顿问题，使用固定视口单位 */
    .meteor {
        width: 80px;
        filter: drop-shadow(0 0 15px rgba(253, 224, 71, 0.8));
        opacity: 0; /* 默认隐藏 */
    }

    /* 不同的流星轨道 */
    .meteor1 {
        top: 0;
        right: 0;
        animation: shootMeteor 6s linear infinite;
        animation-delay: 0s;
    }
    .meteor2 {
        top: 20%;
        right: -10%;
        width: 60px;
        animation: shootMeteor 8s linear infinite;
        animation-delay: 3s;
    }
    .meteor3 {
        top: 40%;
        right: -20%;
        width: 100px;
        animation: shootMeteor 7s linear infinite;
        animation-delay: 5s;
    }

    @keyframes moveUfo {
        0% { transform: translateX(0) rotate(-5deg); }
        100% { transform: translateX(110vw) rotate(5deg); }
    }

    @keyframes movePlanet {
        0% { transform: translateX(0) rotate(0deg); }
        100% { transform: translateX(50vw) rotate(20deg); }
    }

    @keyframes shootMeteor {
        0% {
            opacity: 1;
            transform: translate(20vw, -20vh) rotate(0deg); /* Start: Top Right (off screen) */
        }
        20% {
            opacity: 1;
        }
        60%, 100% {
            opacity: 0;
            transform: translate(-120vw, 120vh) rotate(0deg); /* End: Bottom Left */
        }
    }

    /* --- 5. NEON TITLE (完美还原多色循环) --- */
    .neon-container {
        position: relative;
        z-index: 10;
        text-align: center;
        margin-top: 15vh; /* 垂直定位 */
        pointer-events: none; /* 让鼠标穿透，不影响下方输入框 */
    }

    .neon-title {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: clamp(3rem, 5vw, 5rem); /* 响应式字体 */
        color: #fff;
        text-transform: uppercase;
        letter-spacing: 5px;
        /* 初始阴影 */
        text-shadow: 
            0 0 5px #fff,
            0 0 10px #fff,
            0 0 20px #fff,
            0 0 40px #f09,
            0 0 80px #f09;
        animation: neon-color-cycle 8s infinite alternate;
    }

    .sub-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.8);
        margin-top: 10px;
        letter-spacing: 2px;
        text-shadow: 0 0 5px rgba(255,255,255,0.5);
    }

    .cursive-instruction {
        font-family: 'Great Vibes', cursive;
        font-size: 2.5rem;
        color: rgba(255, 255, 255, 0.9);
        margin-top: 30px;
        text-shadow: 0 0 8px rgba(255,255,255,0.6);
        animation: breathe 3s infinite ease-in-out;
    }

    /* 还原 CodePen 的 RGB 循环变色 */
    @keyframes neon-color-cycle {
        0% {
            text-shadow: 
                0 0 5px #fff, 0 0 10px #fff, 0 0 20px #fff, 
                0 0 40px #ff00de, 0 0 80px #ff00de; /* Pink */
        }
        25% {
            text-shadow: 
                0 0 5px #fff, 0 0 10px #fff, 0 0 20px #fff, 
                0 0 40px #00ffff, 0 0 80px #00ffff; /* Cyan */
        }
        50% {
            text-shadow: 
                0 0 5px #fff, 0 0 10px #fff, 0 0 20px #fff, 
                0 0 40px #00ff00, 0 0 80px #00ff00; /* Green */
        }
        75% {
            text-shadow: 
                0 0 5px #fff, 0 0 10px #fff, 0 0 20px #fff, 
                0 0 40px #ffff00, 0 0 80px #ffff00; /* Yellow */
        }
        100% {
            text-shadow: 
                0 0 5px #fff, 0 0 10px #fff, 0 0 20px #fff, 
                0 0 40px #ff0000, 0 0 80px #ff0000; /* Red */
        }
    }

    @keyframes breathe {
        0%, 100% { opacity: 0.8; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.05); }
    }

    /* --- 6. CHAT INTERFACE (OCD APPROVED: CLEAN, CENTERED, STABLE) --- */

    /* [1] 根除所有背景干扰 (The Nuclear Option) */
    /* 强制底部所有容器透明，去掉那个廉价的方形黑底 */
    div[data-testid="stBottom"],
    div[data-testid="stBottom"] > div,
    div[data-testid="stChatInput"],
    div[data-testid="stChatInput"] > div,
    div[data-testid="stChatInput"] > div > div {
        background-color: transparent !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* [2] 输入框容器布局 (Centering) */
    /* 让输入框不再占满全屏，而是居中 */
    div[data-testid="stChatInput"] {
        display: flex !important;
        justify-content: center !important; /* 水平居中 */
        padding-bottom: 50px !important; /* 距离底部抬高 */
    }

    div[data-testid="stChatInput"] > div {
        width: 100% !important;
        max-width: 650px !important; /* 【变短】：限制最大宽度 */
        flex-grow: 0 !important;
    }

    /* [3] 胶囊本体设计 (The Capsule) */
    .stChatInput textarea {
        /* 【变粗】：增加高度和内边距 */
        min-height: 60px !important; 
        padding-top: 18px !important; /* 调整文字垂直居中 */
        padding-bottom: 18px !important;
        
        /* 形状与材质 */
        border-radius: 40px !important; /* 完美的圆润度 */
        background-color: rgba(20, 20, 20, 0.9) !important; /* 深邃的高级黑，不透光以免看到后面的星星 */
        border: 1px solid rgba(255, 255, 255, 0.15) !important; /* 极细的高光边 */
        color: #FFFFFF !important;
        font-family: 'Bricolage Grotesque', sans-serif !important;
        font-size: 18px !important; /* 字体加大一点，更易读 */
        letter-spacing: 0.5px;
        
        /* 阴影：增加悬浮感 */
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        
        /* 【禁止颤动】：移除所有可能导致布局变化的 transition */
        transition: border-color 0.2s, box-shadow 0.2s !important; 
        
        /* 隐藏滚动条 */
        overflow: hidden !important;
    }

    /* [4] 交互状态 (Focus) */
    .stChatInput textarea:focus {
        background-color: rgba(10, 10, 10, 1) !important; /* 聚焦时更黑更实 */
        border-color: rgba(100, 200, 255, 0.6) !important; /* 青蓝色微光 */
        box-shadow: 0 0 20px rgba(100, 200, 255, 0.15), 0 10px 30px rgba(0,0,0,0.6) !important;
    }

    /* [5] 清理多余元素 */
    /* 隐藏发送按钮 (保持极简) */
    button[data-testid="stChatInputSubmitButton"] {
        display: none !important;
    }
    /* 隐藏右下角字符数 */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    /* 隐藏输入框右上角的奇怪图标容器（如果有） */
    div[data-testid="stChatInput"] svg {
        display: none !important;
    }
</style>
"""


if 'css_code' in locals():
    st.markdown(css_code, unsafe_allow_html=True)

# --- 3. INJECT HTML BACKGROUND (SVG ASSETS) ---
# 这是专业设计的背景层：视差星星 + 动态 SVG 图标 (UFO/行星/流星)
# --- 找到 html_structure = """ ... """ 这一段，完全替换为下面这个 ---
html_structure = """
<div id="starry-section">
<img class="star-layer" id="stars1" src="https://cdn.jsdelivr.net/gh/KyleSchullerDEV/CodePenStorage/images/starry.svg">
<img class="star-layer" id="stars2" src="https://cdn.jsdelivr.net/gh/KyleSchullerDEV/CodePenStorage/images/starry.svg">
<img class="star-layer" id="stars3" src="https://cdn.jsdelivr.net/gh/KyleSchullerDEV/CodePenStorage/images/starry.svg">
<svg viewBox="0 0 640 512" class="icon-svg ufo"><path fill="currentColor" d="M320 288c124.2 0 176-50.9 176-50.9c0-8.3-.6-16.5-1.7-24.5C582 235.5 640 275 640 320c0 70.7-143.3 128-320 128S0 390.7 0 320c0-45 58-84.5 145.7-107.4c-1.2 8-1.7 16.2-1.7 24.5c0 0 51.8 50.9 176 50.9zm24 88a24 24 0 1 0 -48 0 24 24 0 1 0 48 0zM128 352a24 24 0 1 0 0-48 24 24 0 1 0 0 48zm408-24a24 24 0 1 0 -48 0 24 24 0 1 0 48 0z"/><path fill="#7dd3fc" opacity="0.4" d="M496 237.1s-51.8 50.9-176 50.9s-176-50.9-176-50.9C144 141.5 222.8 64 320 64s176 77.5 176 173.1z"/></svg>
<svg viewBox="0 0 512 512" class="icon-svg planet"><path fill="#c2410c" d="M408.3 114.3C370.3 73.5 316.1 48 256 48C141.1 48 48 141.1 48 256c0 60.1 25.5 114.3 66.3 152.3c58.5-37.6 111.3-85 160.1-133.8s96.3-101.7 133.8-160.1zm38 57.5c-32.6 46-75.8 97.1-126.6 147.9s-101.8 94-147.9 126.6C197.6 457.7 226 464 256 464c114.9 0 208-93.1 208-208c0-30-6.3-58.4-17.7-84.2z"/><path fill="#fb923c" d="M503.9 8.1c35.2 35.2-47.3 174.7-184.2 311.6S43.3 539.1 8.1 503.9c-22.1-22.1 2.3-85.6 57.6-163.7c9.1 20.7 21.8 40.2 38 57.5c-5.7 8.8-11.1 17.8-16.3 26.9c69.3-39.6 130.8-94 187-150.1s110.6-117.7 150.1-187c-9.1 5.2-18 10.6-26.9 16.3c-17.4-16.2-36.9-28.9-57.5-38C418.3 10.4 481.7-14 503.9 8.1z"/></svg>
<svg viewBox="0 0 512 512" class="icon-svg meteor meteor1"><path fill="#ef4444" d="M64 320a128 128 0 1 1 256 0A128 128 0 1 1 64 320zm128-32a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zm16 96a16 16 0 1 0 0-32 16 16 0 1 0 0 32z"/><path fill="#fde047" d="M493.7 .9L299.4 75.6l2.3-29.3c1-12.8-12.8-21.5-24-15.1L101.3 133.4C38.6 169.7 0 236.6 0 309C0 421.1 90.9 512 203 512c72.4 0 139.4-38.6 175.7-101.3L480.8 234.3c6.5-11.1-2.2-25-15.1-24l-29.3 2.3L511.1 18.3c.6-1.5 .9-3.2 .9-4.8C512 6 506 0 498.5 0c-1.7 0-3.3 .3-4.8 .9zM192 192a128 128 0 1 1 0 256 128 128 0 1 1 0-256z"/></svg>
<svg viewBox="0 0 512 512" class="icon-svg meteor meteor2"><path fill="#ef4444" d="M64 320a128 128 0 1 1 256 0A128 128 0 1 1 64 320zm128-32a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zm16 96a16 16 0 1 0 0-32 16 16 0 1 0 0 32z"/><path fill="#fde047" d="M493.7 .9L299.4 75.6l2.3-29.3c1-12.8-12.8-21.5-24-15.1L101.3 133.4C38.6 169.7 0 236.6 0 309C0 421.1 90.9 512 203 512c72.4 0 139.4-38.6 175.7-101.3L480.8 234.3c6.5-11.1-2.2-25-15.1-24l-29.3 2.3L511.1 18.3c.6-1.5 .9-3.2 .9-4.8C512 6 506 0 498.5 0c-1.7 0-3.3 .3-4.8 .9zM192 192a128 128 0 1 1 0 256 128 128 0 1 1 0-256z"/></svg>
<svg viewBox="0 0 512 512" class="icon-svg meteor meteor3"><path fill="#ef4444" d="M64 320a128 128 0 1 1 256 0A128 128 0 1 1 64 320zm128-32a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zm16 96a16 16 0 1 0 0-32 16 16 0 1 0 0 32z"/><path fill="#fde047" d="M493.7 .9L299.4 75.6l2.3-29.3c1-12.8-12.8-21.5-24-15.1L101.3 133.4C38.6 169.7 0 236.6 0 309C0 421.1 90.9 512 203 512c72.4 0 139.4-38.6 175.7-101.3L480.8 234.3c6.5-11.1-2.2-25-15.1-24l-29.3 2.3L511.1 18.3c.6-1.5 .9-3.2 .9-4.8C512 6 506 0 498.5 0c-1.7 0-3.3 .3-4.8 .9zM192 192a128 128 0 1 1 0 256 128 128 0 1 1 0-256z"/></svg>
</div>

<div class="neon-container">
<div class="neon-title">THE BOOK OF ANSWERS</div>
<div class="sub-title">答案之书</div>
<div class="cursive-instruction">Focus on your question... / 请在心中默念你的问题... 集中精神...</div>
</div>
"""
st.markdown(html_structure, unsafe_allow_html=True)

# --- 4. EXPANDED ANSWER DATABASE (从你的最新请求中整合的完整列表) ---
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

# --- 5. CHAT LOGIC & PROMPT ENGINEERING ---

if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 处理用户输入
if prompt := st.chat_input("Type your question here / 在此输入你的问题..."):
    
    # 1. 记录用户输入
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. 生成回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # 模拟连接命运的等待时间
        with st.spinner("Consulting the spirits... / 正在连接命运..."):
            time.sleep(1.5)
            
        random_answer = random.choice(answers)
        
        # 使用你指定的 Prompt 结构
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
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User Question: {prompt}\nBook Answer: {random_answer}"}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
            )
            full_response = chat_completion.choices[0].message.content
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"The spirits are silent (Error): {e}")