# main.py
import string
import random
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import pymongo
import redis
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- 1. DEFINE YOUR DATABASE CONNECTIONS ---
DATABASE_URL = "postgresql://postgres:12345@localhost/postgres" # Replace with your password/db if different
MONGO_URL = "mongodb://localhost:27017/"
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# --- 2. SETUP DATABASE CLIENTS ---
mongo_client = pymongo.MongoClient(MONGO_URL)
mongo_db = mongo_client["url_shortener_analytics"]
clicks_collection = mongo_db["clicks"]

# Redis connection with error handling
redis_client = None
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    # Test the connection
    redis_client.ping()
    print("✅ Redis connected successfully!")
except Exception as e:
    print(f"⚠️ Redis connection failed: {e}")
    print("📝 App will work without Redis caching")
    redis_client = None

# --- 3. IMPROVED DATABASE DEPENDENCY ---
# This new structure is more reliable for handling connections in FastAPI
def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        conn.close()

# --- API Setup ---
app = FastAPI(title="Shorten URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLBase(BaseModel):
    original_url: str

def generate_short_code(size=7, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@app.post("/shorten")
def create_short_url(url: URLBase, request: Request, conn=Depends(get_db_connection)):
    short_code = generate_short_code()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO urls (original_url, short_code) VALUES (%s, %s) RETURNING short_code",
                (url.original_url, short_code)
            )
            new_url_record = cur.fetchone()
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    base_url = str(request.base_url)
    full_short_url = f"{base_url}{new_url_record['short_code']}"
    
    return {"short_url": full_short_url}

# --- 4. CORRECTED THE redirect_to_url FUNCTION ---
@app.get("/{short_code}")
def redirect_to_url(short_code: str, request: Request, conn=Depends(get_db_connection)):
    """Finds the long URL (checking cache first!) and redirects."""
    
    # Check Redis cache if available
    cached_url = None
    if redis_client:
        try:
            cached_url = redis_client.get(short_code)
            if cached_url:
                print("✅ Found in Redis cache!")
                log_entry = { "short_code": short_code, "timestamp": datetime.datetime.utcnow(), "ip_address": request.client.host }
                clicks_collection.insert_one(log_entry)
                return RedirectResponse(url=cached_url)
        except Exception as e:
            print(f"⚠️ Redis cache error: {e}")
    
    print("🔍 Not in cache, checking database...")
    original_url = None
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT original_url FROM urls WHERE short_code = %s", (short_code,))
            record = cur.fetchone()
            if record:
                original_url = record['original_url']
            else:
                raise HTTPException(status_code=404, detail="Short URL not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

    # Cache the result in Redis if available
    if redis_client and original_url:
        try:
            redis_client.set(short_code, original_url, ex=3600)
            print("💾 Cached in Redis for 1 hour")
        except Exception as e:
            print(f"⚠️ Failed to cache in Redis: {e}")
    
    # Log the click
    try:
        log_entry = { "short_code": short_code, "timestamp": datetime.datetime.utcnow(), "ip_address": request.client.host }
        clicks_collection.insert_one(log_entry)
        print("📊 Click logged successfully")
    except Exception as e:
        print(f"⚠️ Failed to log click: {e}")

    return RedirectResponse(url=original_url)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serves the frontend index.html file."""
    with open("index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)
