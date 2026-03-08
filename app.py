import streamlit as st
from google import genai

# --- 1. 頁面基本設定 ---
st.set_page_config(page_title="Inner Bar 心之鎖向", layout="centered")

# --- 2. 安全載入 API Key ---
if "GEMINI_API_KEY" in st.secrets:
    # 使用最新的 Client 寫法
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("請在 Secrets 中設定 GEMINI_API_KEY")
    st.stop()

# --- 3. 注入原本的 CSS 樣式 --- (與之前相同，略過不改)
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;700&family=Noto+Serif+TC:wght@600&display=swap');
        :root { --paper-color: #f4e4bc; }
        .main { background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://i.postimg.cc/0yc2ysf9/04f91558-7b1d-4662-af46-4a023992c21a.png') no-repeat center center fixed; background-size: cover; }
        .chat-container { background: var(--paper-color); padding: 35px; box-shadow: 15px 15px 35px rgba(0,0,0,0.7); transform: rotate(-0.5deg); border-radius: 2px; margin-top: 50px; }
        .dialog-text { color: #2c1e11; font-family: "Noto Serif TC", serif; font-size: 1.1rem; line-height: 1.8; min-height: 150px; }
        .status-text { font-size: 0.9rem; color: #8b5e3c; font-style: italic; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. 初始化對話狀態 ---
if "messages" not in st.session_state:
    # 最新版 SDK 改用 messages 列表來管理歷史
    st.session_state.messages = [
        {"role": "user", "content": "妳是神祕酒保。優雅、感性，在 10 題內探測依戀類型。第 10 題邀請至 6/4 松菸展覽。請用繁體中文。"}
    ]
    st.session_state.turn_count = 0
    st.session_state.last_response = "「歡迎推開這扇門。在調製第一杯酒前，我想知道，你通常在什麼樣的瞬間，會覺得自己需要一個安靜的角落？」"

# --- 5. 介面渲染 ---
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
st.markdown(f'<div class="dialog-text">{st.session_state.last_response}</div>', unsafe_allow_html=True)

if st.session_state.turn_count < 10:
    user_input = st.chat_input("寫下妳的心情...")
    
    if user_input:
        st.session_state.turn_count += 1
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("酒保正在思考..."):
            # 使用最新的 generate_content 語法
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=st.session_state.messages
            )
            st.session_state.last_response = response.text
            st.session_state.messages.append({"role": "model", "content": response.text})
            st.rerun()
else:
    st.markdown('<div class="status-text">酒保已為妳調好最後一杯酒，期待 6/4 與妳在松菸相見。</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)