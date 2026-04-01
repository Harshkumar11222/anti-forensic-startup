from fastapi import FastAPI, HTTPException
from detector.detect import scan_system
from jose import jwt
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # sab allow (dev ke liye)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "mysecretkey"

users = {
    "harshu": "9999"
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
    return {"message": "Backend is LIVE 🚀"}

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