import streamlit as st
from pymongo import MongoClient
import hashlib

# 🔥 CONNECT USING STREAMLIT SECRETS (IMPORTANT FOR DEPLOYMENT)
client = MongoClient(st.secrets["MONGO_URI"])

# Database + Collections
db = client["phishing_app"]
users_collection = db["users"]
scans_collection = db["scans"]


# 🔐 HASH PASSWORD
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ✅ REGISTER USER
def add_user(username, password):
    try:
        print("👉 Creating user:", username)

        if users_collection.find_one({"username": username}):
            print("❌ User already exists")
            return False

        users_collection.insert_one({
            "username": username,
            "password": hash_password(password)
        })

        print("✅ User created successfully")
        return True

    except Exception as e:
        print("❌ DB Error (add_user):", e)
        return False


# ✅ LOGIN USER
def login_user(username, password):
    try:
        print("🔍 Login attempt:", username)

        user = users_collection.find_one({"username": username})

        if not user:
            print("❌ User not found")
            return None

        if user["password"] == hash_password(password):
            print("✅ Login successful")
            return user

        print("❌ Wrong password")
        return None

    except Exception as e:
        print("❌ DB Error (login_user):", e)
        return None


# 📩 SAVE EMAIL SCAN
def save_scan(username, email, result, confidence):
    try:
        scans_collection.insert_one({
            "username": username,
            "email": email,
            "result": int(result),
            "confidence": float(confidence)
        })
        print("✅ Scan saved")

    except Exception as e:
        print("❌ DB Error (save_scan):", e)


# 📊 GET USER SCANS
def get_user_scans(username):
    try:
        return list(scans_collection.find({"username": username}))
    except Exception as e:
        print("❌ DB Error (get_user_scans):", e)
        return []


# 📊 GET USER STATS (REAL-TIME DASHBOARD)
def get_user_stats(username):
    try:
        scans = list(scans_collection.find({"username": username}))

        total = len(scans)
        phishing = sum(1 for s in scans if s["result"] == 1)
        safe = sum(1 for s in scans if s["result"] == 0)

        return total, phishing, safe

    except Exception as e:
        print("❌ DB Error (get_user_stats):", e)
        return 0, 0, 0