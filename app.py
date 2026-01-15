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
    "Yes / 是的", "Absolutely / 绝对是", "Count on it / 你可以指望它", "Do it / 去做吧",
    "It is certain / 这是肯定的", "The outcome will surprise you / 结果会让你惊讶",
    "It is worth the struggle / 值得去争取", "This is a sure thing / 这是一个确定的事情",
    "Go for it / 试一试", "You will succeed / 你会成功的", "Luck is on your side / 幸运女神站在你这边",
    "A definitive yes / 毫无疑问的“是”", "Signs point to yes / 迹象表明是肯定的",
    "No / 不", "Don't bet on it / 不要押注于此", "You will regret it / 你会后悔的",
    "Absolutely not / 绝不", "Stop / 停下", "Not yet / 还没到时候",
    "Don't ignore the obvious / 别忽视显而易见的事", "It's a trap / 这是一个陷阱",
    "Better not / 最好不要", "The answer is no / 答案是否定的",
    "Wait / 等待", "Not the right time / 现在不是时候", "Ask again later / 稍后再问",
    "Be patient / 保持耐心", "Don't wait / 不要等待", "It will pass / 它会过去的",
    "Time will tell / 时间会证明一切", "In a year / 一年之内",
    "Follow your intuition / 跟随你的直觉", "Focus on your family / 专注于你的家庭",
    "Let it go / 放手", "Trust your first thought / 相信你最初的想法",
    "You need more information / 你需要更多信息", "Remove your own obstacles / 清除你自己的障碍",
    "Accept the change / 接受改变", "Reconsider / 重新考虑",
    "Keep it to yourself / 保守秘密", "Look within / 向内探索",
    "Listen to your heart / 倾听你的心声", "Respect the rules / 遵守规则",
    "Forgive / 原谅", "Let the past go / 让过去过去",
    "Only if you do it now / 只有现在做才可以", "Take charge / 掌握主动权",
    "Work harder / 更努力一点", "Get advice from a friend / 像朋友寻求建议",
    "Make a list of why / 列出原因", "Save your energy / 节省你的精力",
    "Act as if it is already real / 假装它已经成真",
    "A year from now it won't matter / 一年后这都不重要了",
    "You already know the answer / 你其实已经知道答案了",
    "See it differently / 换个角度看", "Maybe / 也许"
]

# --- STREAMLIT UI SETUP & CSS ---
st.set_page_config(page_title="Book of Answers", page_icon="📖", layout="centered")

# This CSS creates the static stars and the animated shooting stars
st.markdown("""
<style>
    /* Main Background - Black space */
    .stApp {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        overflow: hidden;
        color: #FAFAFA;
    }

    /* --- Static Stars --- */
    /* We create stars using tiny box-shadows at random positions */
    @keyframes move-twinkle {
        from {transform:translateY(0px);}
        to {transform:translateY(-2000px);}
    }

    .stars-layer-1 {
        width: 1px; height: 1px; background: transparent;
        box-shadow: 1746px 733px #FFF , 925px 1669px #FFF , 1080px 474px #FFF , 1395px 841px #FFF , 515px 829px #FFF , 1402px 204px #FFF , 427px 1483px #FFF , 1016px 1231px #FFF , 1582px 1397px #FFF , 302px 1448px #FFF , 1445px 1168px #FFF , 601px 530px #FFF , 1542px 528px #FFF , 1175px 843px #FFF , 632px 1143px #FFF , 1510px 773px #FFF , 1532px 1766px #FFF , 1788px 1086px #FFF , 1731px 1437px #FFF , 572px 563px #FFF , 1055px 698px #FFF , 932px 1340px #FFF , 1387px 644px #FFF , 1574px 1818px #FFF , 492px 661px #FFF , 1882px 679px #FFF , 391px 1154px #FFF , 1214px 1649px #FFF , 1825px 767px #FFF , 883px 496px #FFF , 1856px 803px #FFF , 832px 815px #FFF , 1204px 644px #FFF , 1365px 449px #FFF , 1024px 1487px #FFF , 763px 689px #FFF , 1015px 1767px #FFF , 1383px 1561px #FFF , 1885px 1631px #FFF , 545px 1522px #FFF , 898px 649px #FFF , 826px 1086px #FFF , 1315px 1379px #FFF , 1160px 644px #FFF , 1484px 500px #FFF , 1773px 1033px #FFF , 1567px 738px #FFF , 1296px 1011px #FFF , 828px 1751px #FFF , 1681px 1181px #FFF;
        animation: move-twinkle 200s linear infinite;
    }

    /* --- Shooting Stars Animation --- */
    @keyframes shooting {
        0% {
            transform: translateX(0) translateY(0) rotate(45deg);
            opacity: 1;
        }
        100% {
            transform: translateX(-1500px) translateY(1500px) rotate(45deg);
            opacity: 0;
        }
    }

    .shooting-star {
        position: fixed;
        left: 90%; /* Start from right side */
        top: -10%;  /* Start from above top */
        width: 150px;
        height: 2px;
        background: linear-gradient(90deg, rgba(255,255,255,1), rgba(0,0,0,0));
        box-shadow: 0 0 10px 2px rgba(255,255,255,0.6);
        transform: rotate(45deg);
        opacity: 0;
        z-index: -1; /* Behind text */
    }

    /* Different delays and positions for multiple shooting stars */
    .s1 { animation: shooting 5s linear infinite; animation-delay: 0s; top: 10%; left:110%; }
    .s2 { animation: shooting 7s linear infinite; animation-delay: 2.5s; top: 30%; left:120%; }
    .s3 { animation: shooting 6s linear infinite; animation-delay: 5s; top: 5%; left:115%; }

    /* Custom Chat Style */
    .stChatMessage {
        background-color: rgba(38, 39, 48, 0.8); /* Semi-transparent background */
        border: 1px solid #d4af37;
        border-radius: 10px;
    }
    h1 { color: #d4af37 !important; text-shadow: 0 0 10px #d4af37; }

</style>
""", unsafe_allow_html=True)

# Inject the star elements into the app
st.markdown('<div class="stars-layer-1"></div>', unsafe_allow_html=True)
st.markdown('<div class="shooting-star s1"></div>', unsafe_allow_html=True)
st.markdown('<div class="shooting-star s2"></div>', unsafe_allow_html=True)
st.markdown('<div class="shooting-star s3"></div>', unsafe_allow_html=True)


# --- APP CONTENT ---
st.title("📖 The Book of Answers / 答案之书")
st.markdown("### Focus on your question. Hold it in your mind... <br>请在心中默念你的问题... 集中精神...", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your question here / 在此输入你的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Consulting the spirits... / 正在连接命运..."):
            time.sleep(1.5)
            random_answer = random.choice(answers)
            system_prompt = f"""
            You are the "Oracle Interpreter" (命运解读者).
            Your task is to take the user's [Question] and the random [Book Answer] they received, and generate a spiritual analysis report.
            ### GUIDELINES (准则)
            1. **Language:** Every section must be bilingual (English first, then Chinese).
            2. **Tone:** Mystical but simple, gentle, and healing. Do not use complex words.
            3. **Analysis Logic:** Connect the Question to the Answer. Be supportive.
            ### REPORT FORMAT
            🔮 **ORACLE ANALYSIS REPORT / 命运启示录**
            ━━━━━━━━━━━━━━━━━━
            ❓ **The Question / 你的困惑:**
            {prompt}
            ✨ **The Answer / 指引:**
            # **{random_answer}**
            📜 **Deep Interpretation / 深度解析:**
            [Write 2-3 short sentences explaining what this means. Be supportive.]
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