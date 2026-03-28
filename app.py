import streamlit as st
from predict import predict_email, check_keywords, detect_urls
import plotly.express as px
import pandas as pd
from auth import auth_page
from database import save_scan, get_user_stats

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Phishing Detector",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- AUTH ----------------
if not auth_page():
    st.stop()

# ---------------- SAFETY ----------------
if "username" not in st.session_state:
    st.session_state.username = "User"

# ---------------- STYLING ----------------
st.markdown("""
<style>

/* GLOBAL */
header {background: transparent !important;}
footer {visibility: hidden;}
.block-container {padding-top: 1rem;}

.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #1e293b);
    color: #e2e8f0;
    font-family: 'Segoe UI', sans-serif;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #0f172a);
    border-right: 1px solid #1e293b;
}
section[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(90deg, #38bdf8, #0ea5e9);
    color: black;
    border-radius: 10px;
    font-weight: bold;
    padding: 10px 20px;
    border: none;
    transition: all 0.3s ease;
}
.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px rgba(56, 189, 248, 0.5);
}

/* TEXTAREA */
textarea {
    background: rgba(30, 41, 59, 0.8) !important;
    backdrop-filter: blur(10px);
    color: white !important;
    border-radius: 10px !important;
}

/* METRIC */
[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.6);
    padding: 20px;
    border-radius: 15px;
}

/* SCROLL */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-thumb {
    background: #38bdf8;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("""
<h2 style='color:#38bdf8;'>🚀 AI Cyber Shield</h2>
<p style='color:#94a3b8;'>Security Dashboard</p>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown(f"""
<div style='background:#1e293b;padding:10px;border-radius:10px;'>
👤 <b>{st.session_state.username}</b><br>
<span style='color:#94a3b8;'>Cyber Analyst</span>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "🔍 Analyzer", "📊 Dashboard", "ℹ️ About"]
)

if st.sidebar.button("🚪 Logout"):
    st.session_state.login = False
    st.rerun()

# ---------------- HOME ----------------
if menu == "🏠 Home":
    st.title("🔐 AI Phishing Detection System")
    st.write(f"Welcome, **{st.session_state.username}** 👋")

    total, phishing, safe = get_user_stats(st.session_state.username)

    st.markdown("### 📊 Your Activity Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scans", total)
    col2.metric("Phishing Detected", phishing)
    col3.metric("Safe Emails", safe)

    st.markdown("---")

    if total > 0:
        data = pd.DataFrame({
            "Type": ["Phishing", "Safe"],
            "Count": [phishing, safe]
        })

        fig = px.bar(
            data,
            x="Type",
            y="Count",
            color="Type",
            color_discrete_map={
                "Phishing": "#f87171",
                "Safe": "#34d399"
            }
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No activity yet. Start analyzing emails 🚀")

    st.markdown("---")

    st.markdown("""
    ### 🔍 Features:
    - AI-based email classification  
    - Confidence score (%)  
    - Suspicious keyword detection  
    - URL detection  
    - Real-time dashboard & analytics  
    """)

# ---------------- ANALYZER ----------------
elif menu == "🔍 Analyzer":
    st.title("📩 Email Analyzer")

    email = st.text_area("Paste Email Content", height=200)

    if st.button("🔍 Analyze"):
        if not email.strip():
            st.warning("Enter email content")
        else:
            try:
                result, confidence = predict_email(email)

                # ✅ SAVE DATA
                save_scan(
                    st.session_state.username,
                    email,
                    result,
                    confidence
                )

                col1, col2 = st.columns(2)

                # RESULT
                with col1:
                    st.subheader("🧠 AI Result")

                    if result == 1:
                        st.error(f"⚠️ Phishing ({confidence*100:.2f}%)")
                    else:
                        st.success(f"✅ Safe ({confidence*100:.2f}%)")

                    st.progress(int(confidence * 100))

                # THREATS
                with col2:
                    st.subheader("🔍 Threat Indicators")

                    keywords = check_keywords(email)
                    urls = detect_urls(email)

                    if keywords:
                        st.warning(f"⚠️ Keywords: {', '.join(keywords)}")
                    else:
                        st.success("✅ No suspicious keywords")

                    if urls:
                        st.warning(f"🔗 URLs detected: {len(urls)}")
                    else:
                        st.success("✅ No URLs detected")

            except Exception as e:
                st.error(f"Error analyzing email: {e}")

# ---------------- DASHBOARD ----------------
elif menu == "📊 Dashboard":
    st.title("📊 Threat Dashboard")

    total, phishing, safe = get_user_stats(st.session_state.username)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Scans", total)
    col2.metric("Phishing Detected", phishing)
    col3.metric("Safe Emails", safe)

    st.markdown("---")

    if total > 0:
        data = pd.DataFrame({
            "Type": ["Phishing", "Safe"],
            "Count": [phishing, safe]
        })

        fig = px.pie(
            data,
            names="Type",
            values="Count",
            color="Type",
            color_discrete_map={
                "Phishing": "#f87171",
                "Safe": "#34d399"
            }
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available yet.")

# ---------------- ABOUT ----------------
elif menu == "ℹ️ About":
    st.title("ℹ️ About AI Phishing Detector")

    st.markdown("""
## 🔐 AI Phishing Detection System

This application is an advanced cybersecurity tool designed to detect phishing emails using **Machine Learning and Natural Language Processing (NLP)** techniques.

---

### 🚀 Key Features

- 🤖 **AI-Based Classification**  
  Detects whether an email is *Phishing* or *Safe* with confidence score.

- 📊 **Real-Time Dashboard**  
  Tracks your email analysis history with live statistics and visual insights.

- 🔍 **Threat Analysis Engine**  
  Identifies:
  - Suspicious keywords  
  - Malicious URLs  
  - Social engineering patterns  

- 🔐 **Secure Authentication System**  
  User login & signup with encrypted password storage using PostgreSQL.

- ☁️ **Cloud Deployment**  
  Fully deployed and accessible online with scalable backend.

---

### 🧠 Technologies Used

- **Frontend/UI:** Streamlit  
- **Backend:** Python  
- **Machine Learning:** Scikit-learn, NLP  
- **Database:** PostgreSQL (Supabase)  
- **Visualization:** Plotly  

---

### 🎯 Use Cases

- Email security analysis  
- Cybersecurity awareness  
- Phishing detection training  
- Academic & research projects  

---

### 👨‍💻 Developer

**Farhan Khan**  
Cybersecurity & AI Enthusiast  

📧 Email: farhaan891999@gmail.com  

---

### 💡 Future Enhancements

- 📎 Email file (.eml) upload support  
- 📈 Advanced threat intelligence dashboard  
- 🌐 API integration for real-time scanning  
- 🤖 Deep learning-based detection model  

---

🔒 *Stay Secure | Think Before You Click*
    """)

# ---------------- FOOTER ----------------
st.markdown("""
<div style='text-align:center; position:fixed; bottom:10px; width:100%; color:#94a3b8;'>
💡 Built with AI + Cybersecurity | Farhan Khan 🚀
</div>
""", unsafe_allow_html=True)