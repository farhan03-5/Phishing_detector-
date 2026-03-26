from pymongo import MongoClient
import hashlib

# 🔥 CONNECT TO MONGODB ATLAS
client = MongoClient("mongodb+srv://farhaan891999_db_user:zmpxAI4SQuHRP4CA@cluster0.uqp4ec9.mongodb.net/?retryWrites=true&w=majority")

# Database + Collection
db = client["phishing_app"]
users_collection = db["users"]   # 🔥 change to "users" (best practice)

# 🔐 HASH PASSWORD
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ✅ REGISTER USER
def add_user(username, password):
    print("👉 Creating user:", username)

    try:
        if users_collection.find_one({"username": username}):
            print("❌ User already exists")
            return False

        users_collection.insert_one({
            "username": username,
            "password": hash_password(password)
        })

        print("✅ User created")
        return True

    except Exception as e:
        print("❌ DB Error:", e)
        return False


# ✅ LOGIN USER
def login_user(username, password):
    print("🔍 Login attempt:", username)

    try:
        user = users_collection.find_one({"username": username})

        if not user:
            print("❌ User NOT found")
            return None

        if user["password"] == hash_password(password):
            print("✅ Login success")
            return user
        else:
            print("❌ Wrong password")
            return None

    except Exception as e:
        print("❌ DB Error:", e)
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