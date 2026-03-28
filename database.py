import streamlit as st
import psycopg2
import hashlib

# 🔥 CONNECT TO SUPABASE POSTGRES
conn = psycopg2.connect(
    st.secrets["DB_URL"],
    sslmode="require"   # 🔥 VERY IMPORTANT for Supabase
)
cursor = conn.cursor()


# 🔐 HASH PASSWORD
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ✅ REGISTER USER
def add_user(username, password):
    try:
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            return False

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hash_password(password))
        )
        conn.commit()
        return True

    except Exception as e:
        print("DB Error:", e)
        return False


# ✅ LOGIN USER
def login_user(username, password):
    try:
        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, hash_password(password))
        )
        return cursor.fetchone()

    except Exception as e:
        print("DB Error:", e)
        return None


# 📩 SAVE EMAIL SCAN
def save_scan(username, email, result, confidence):
    try:
        cursor.execute(
            "INSERT INTO scans (username, email, result, confidence) VALUES (%s, %s, %s, %s)",
            (username, email, int(result), float(confidence))
        )
        conn.commit()
    except Exception as e:
        print("DB Error:", e)


# 📊 GET USER STATS (REAL-TIME)
def get_user_stats(username):
    try:
        cursor.execute("SELECT result FROM scans WHERE username=%s", (username,))
        data = cursor.fetchall()

        total = len(data)
        phishing = sum(1 for d in data if d[0] == 1)
        safe = sum(1 for d in data if d[0] == 0)

        return total, phishing, safe

    except:
        return 0, 0, 0