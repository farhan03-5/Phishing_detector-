import os
import streamlit as st
import base64
from database import add_user, login_user

# ✅ Safe image loader
def get_base64(img_path):
    try:
        with open(img_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        st.error(f"❌ Image not found: {img_path}")
        return ""

def auth_page():
    if "login" not in st.session_state:
        st.session_state.login = False

    if not st.session_state.login:

        # ✅ Image path
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(BASE_DIR, "image", "background2.jpg")
        img = get_base64(img_path)

        # 🔥 FUTURISTIC UI
        st.markdown(f"""
        <style>

        .stApp {{
            background: url("data:image/jpg;base64,{img}");
            background-size: cover;
            background-position: center;
            font-family: 'Segoe UI', sans-serif;
            color: white;
        }}

        .login-box {{
            position: relative;
            background: #020617;   /* 🔥 DARK BLACK/BLUE */
            border-radius: 20px;
            padding: 35px;
            width: 360px;
            margin: auto;
            margin-top: 100px;
            text-align: center;
            box-shadow: 0 0 40px rgba(56, 189, 248, 0.3);
            border: 1px solid rgba(255,255,255,0.1);

        }}

        .login-box::before {{
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 20px;
            padding: 2px;
            background: linear-gradient(270deg, #38bdf8, #0ea5e9, #6366f1, #38bdf8);
            background-size: 600% 600%;
            animation: borderGlow 6s linear infinite;
            -webkit-mask: 
                linear-gradient(#fff 0 0) content-box, 
                linear-gradient(#fff 0 0);
            -webkit-mask-composite: xor;
            mask-composite: exclude;
        }}

        @keyframes borderGlow {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        .login-box h2 {{
            color: #38bdf8;
            text-shadow: 0 0 10px #38bdf8;
        }}

        label {{
            color: #e2e8f0 !important;
        }}

        .stTextInput > div > div > input {{
            background: rgba(255,255,255,0.1) !important;
            color: black !important;
            border-radius: 10px;
            padding: 12px;
            border: 1px solid rgba(255,255,255,0.2);
        }}

        .stTextInput > div > div > input:focus {{
            border: 1px solid #38bdf8;
            box-shadow: 0 0 10px #38bdf8;
        }}

        .stButton > button {{
            background: linear-gradient(90deg, #38bdf8, #0ea5e9);
            color: black;
            border-radius: 12px;
            font-weight: bold;
            width: 100%;
        }}

        .stButton > button:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 20px #38bdf8;
        }}

        header, footer {{
            visibility: hidden;
        }}

        </style>
        """, unsafe_allow_html=True)

        # 🔐 LOGIN UI
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("## 🔐 AI Cyber Login")

        option = st.radio("", ["Login", "Sign Up"])

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # 🔐 SIGN UP
        if option == "Sign Up":
            if st.button("Create Account"):
                if username.strip() == "" or password.strip() == "":
                    st.warning("⚠️ Please fill all fields")
                else:
                    if add_user(username, password):
                        st.success("✅ Account created! Please login")
                    else:
                        st.error("⚠️ Username already exists")

        # 🔐 LOGIN
        else:
            if st.button("Login"):
                if username.strip() == "" or password.strip() == "":
                    st.warning("⚠️ Please fill all fields")
                else:
                    user = login_user(username, password)
                    if user:
                        st.session_state.login = True
                        st.session_state.username = username   # ✅ IMPORTANT (for dashboard/history)
                        st.success("✅ Login successful")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")

        st.markdown("</div>", unsafe_allow_html=True)

        return False

    return True