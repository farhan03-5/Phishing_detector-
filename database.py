from pymongo import MongoClient
import hashlib

# 🔥 CONNECT TO LOCAL MONGODB
client = MongoClient("mongodb://localhost:27017/")

# Database + Collection
db = client["phishing_app"]
users_collection = db["user"]

# 🔐 HASH PASSWORD
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ REGISTER USER
def add_user(username, password):
    try:
        # Check if user exists
        if users_collection.find_one({"username": username}):
            return False

        # Insert new user
        users_collection.insert_one({
            "username": username,
            "password": hash_password(password)
        })
        return True

    except Exception as e:
        print("Error:", e)
        return False

# ✅ LOGIN USER
def login_user(username, password):
    try:
        user = users_collection.find_one({
            "username": username,
            "password": hash_password(password)
        })
        return user

    except Exception as e:
        print("Error:", e)
        return None
    
    # 📩 SAVE EMAIL SCAN
def save_scan(username, email, result, confidence):
    db["scans"].insert_one({
        "username": username,
        "email": email,
        "result": int(result),
        "confidence": float(confidence)
    })

# 📊 GET USER SCANS
def get_user_scans(username):
    return list(db["scans"].find({"username": username}))

# 📊 GET USER STATS
def get_user_stats(username):
    scans = list(db["scans"].find({"username": username}))

    total = len(scans)
    phishing = sum(1 for s in scans if s["result"] == 1)
    safe = sum(1 for s in scans if s["result"] == 0)

    return total, phishing, safe