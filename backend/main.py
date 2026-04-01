from fastapi import FastAPI, HTTPException
from detector.detect import scan_system
from jose import jwt

app = FastAPI()

SECRET_KEY = "mysecretkey"

users = {
    "admin": "1234"
}

def create_token(username):
    return jwt.encode({"user": username}, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except:
        return False

@app.get("/")
def home():
    return {"message": "Anti-Forensic Detection System Running 🚀"}

@app.get("/login")
def login(username: str, password: str):
    if username in users and users[username] == password:
        token = create_token(username)
        return {"token": token}
    return {"error": "Invalid credentials"}

@app.get("/scan")
def scan(token: str):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized")

    return scan_system("C:\\Users")