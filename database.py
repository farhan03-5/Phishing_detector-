import streamlit as st
import psycopg2
import hashlib

# ✅ DATABASE CONNECTION (SAFE + CACHED)
@st.cache_resource
def get_connection():
    try:
        return psycopg2.connect(st.secrets["DB_URL"])
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        return None

conn = get_connection()


def get_cursor():
    if conn:
        return conn.cursor()
    return None


# 🔐 HASH PASSWORD
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ✅ CREATE USER (SIGNUP)
def add_user(username, password):
    cursor = get_cursor()
    if not cursor:
        return False

    try:
        # Check existing user
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            return False

        # Insert user
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hash_password(password))
        )
        conn.commit()
        return True

    except Exception as e:
        st.error(f"❌ Signup error: {e}")
        return False


# ✅ LOGIN USER (FIXED LOGIC)
def login_user(username, password):
    cursor = get_cursor()
    if not cursor:
        return None

    try:
        cursor.execute(
            "SELECT username, password FROM users WHERE username=%s",
            (username,)
        )
        user = cursor.fetchone()

        if not user:
            return None

        # Compare hashed password
        if user[1] == hash_password(password):
            return user
        else:
            return None

    except Exception as e:
        st.error(f"❌ Login error: {e}")
        return None


# 📩 SAVE EMAIL SCAN
def save_scan(username, email, result, confidence):
    cursor = get_cursor()
    if not cursor:
        return

    try:
        cursor.execute(
            "INSERT INTO scans (username, email, result, confidence) VALUES (%s, %s, %s, %s)",
            (username, email, int(result), float(confidence))
        )
        conn.commit()
    except Exception as e:
        st.error(f"❌ Scan save error: {e}")


# 📊 GET USER STATS (REAL-TIME)
def get_user_stats(username):
    cursor = get_cursor()
    if not cursor:
        return 0, 0, 0

    try:
        cursor.execute(
            "SELECT result FROM scans WHERE username=%s",
            (username,)
        )
        data = cursor.fetchall()

        total = len(data)
        phishing = sum(1 for d in data if d[0] == 1)
        safe = sum(1 for d in data if d[0] == 0)

        return total, phishing, safe

    except Exception as e:
        st.error(f"❌ Stats error: {e}")
        return 0, 0, 0