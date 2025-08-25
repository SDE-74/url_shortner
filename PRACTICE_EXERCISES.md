# 🎯 Practice Exercises for Interview Preparation

## 🚀 Hands-on Coding Problems

### Exercise 1: MongoDB Operations

**Problem**: Create a MongoDB collection for URL shortener and implement CRUD operations.

```python
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['url_shortener']
collection = db['urls']

# TODO: Implement these functions

def create_url(original_url, short_code):
    """
    Create a new URL entry in MongoDB
    """
    pass

def get_url_by_code(short_code):
    """
    Retrieve URL by short code
    """
    pass

def update_click_count(short_code):
    """
    Increment click count for a URL
    """
    pass

def delete_url(short_code):
    """
    Delete a URL entry
    """
    pass

def get_popular_urls(limit=10):
    """
    Get URLs ordered by click count
    """
    pass
```

**Solution**:
```python
def create_url(original_url, short_code):
    url_doc = {
        "original_url": original_url,
        "short_code": short_code,
        "created_at": datetime.utcnow(),
        "clicks": 0
    }
    result = collection.insert_one(url_doc)
    return result.inserted_id

def get_url_by_code(short_code):
    return collection.find_one({"short_code": short_code})

def update_click_count(short_code):
    return collection.update_one(
        {"short_code": short_code},
        {"$inc": {"clicks": 1}}
    )

def delete_url(short_code):
    return collection.delete_one({"short_code": short_code})

def get_popular_urls(limit=10):
    return collection.find().sort("clicks", -1).limit(limit)
```

---

### Exercise 2: SQL Queries

**Problem**: Write SQL queries for the URL shortener database.

```sql
-- TODO: Create the tables
CREATE TABLE urls (
    -- Your table structure here
);

CREATE TABLE analytics (
    -- Your analytics table structure here
);

-- TODO: Write these queries

-- 1. Find URLs created in the last 7 days
-- 2. Get total clicks for each URL
-- 3. Find the most popular URL
-- 4. Get URLs with custom codes
-- 5. Calculate average clicks per URL
```

**Solution**:
```sql
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    custom_code BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    clicks INTEGER DEFAULT 0
);

CREATE TABLE analytics (
    id SERIAL PRIMARY KEY,
    url_id INTEGER REFERENCES urls(id),
    ip_address INET,
    user_agent TEXT,
    visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 1. Find URLs created in the last 7 days
SELECT * FROM urls 
WHERE created_at >= CURRENT_DATE - INTERVAL '7 days';

-- 2. Get total clicks for each URL
SELECT u.short_code, u.original_url, u.clicks
FROM urls u
ORDER BY u.clicks DESC;

-- 3. Find the most popular URL
SELECT * FROM urls 
ORDER BY clicks DESC 
LIMIT 1;

-- 4. Get URLs with custom codes
SELECT * FROM urls 
WHERE custom_code = TRUE;

-- 5. Calculate average clicks per URL
SELECT AVG(clicks) as avg_clicks FROM urls;
```

---

### Exercise 3: Redis Implementation

**Problem**: Implement caching and rate limiting with Redis.

```python
import redis
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# TODO: Implement these functions

def cache_url(short_code, original_url, expire_time=3600):
    """
    Cache a URL in Redis with expiration
    """
    pass

def get_cached_url(short_code):
    """
    Get cached URL from Redis
    """
    pass

def rate_limit_user(user_id, max_requests=100, window=3600):
    """
    Implement rate limiting for a user
    """
    pass

def track_user_activity(user_id, action):
    """
    Track user actions in Redis
    """
    pass
```

**Solution**:
```python
def cache_url(short_code, original_url, expire_time=3600):
    key = f"url:{short_code}"
    r.setex(key, expire_time, original_url)
    return True

def get_cached_url(short_code):
    key = f"url:{short_code}"
    return r.get(key)

def rate_limit_user(user_id, max_requests=100, window=3600):
    key = f"rate_limit:{user_id}"
    current = r.incr(key)
    
    if current == 1:
        r.expire(key, window)
    
    return current <= max_requests

def track_user_activity(user_id, action):
    key = f"user_activity:{user_id}"
    r.lpush(key, f"{action}:{time.time()}")
    r.ltrim(key, 0, 99)  # Keep last 100 activities
```

---

### Exercise 4: API Design

**Problem**: Design a RESTful API for the URL shortener.

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# TODO: Define your data models
class URLRequest(BaseModel):
    # Your model here
    pass

class URLResponse(BaseModel):
    # Your response model here
    pass

# TODO: Implement these endpoints

@app.post("/api/urls", response_model=URLResponse)
async def create_short_url(request: URLRequest):
    """
    Create a new short URL
    """
    pass

@app.get("/api/urls/{short_code}")
async def redirect_to_url(short_code: str):
    """
    Redirect to original URL
    """
    pass

@app.get("/api/urls/{short_code}/stats")
async def get_url_stats(short_code: str):
    """
    Get URL statistics
    """
    pass

@app.delete("/api/urls/{short_code}")
async def delete_url(short_code: str):
    """
    Delete a URL
    """
    pass
```

**Solution**:
```python
class URLRequest(BaseModel):
    original_url: str
    custom_code: Optional[str] = None

class URLResponse(BaseModel):
    short_code: str
    original_url: str
    short_url: str
    created_at: str
    clicks: int

@app.post("/api/urls", response_model=URLResponse)
async def create_short_url(request: URLRequest):
    # Validate URL
    if not request.original_url.startswith(('http://', 'https://')):
        raise HTTPException(status_code=400, detail="Invalid URL format")
    
    # Generate short code
    short_code = request.custom_code or generate_short_code(request.original_url)
    
    # Save to database
    url_id = create_url(request.original_url, short_code)
    
    return URLResponse(
        short_code=short_code,
        original_url=request.original_url,
        short_url=f"https://yoursite.com/{short_code}",
        created_at=datetime.utcnow().isoformat(),
        clicks=0
    )
```

---

### Exercise 5: Python Advanced Concepts

**Problem**: Implement advanced Python features for the URL shortener.

```python
import asyncio
import aiohttp
from functools import wraps
import time

# TODO: Implement these functions

def retry_on_failure(max_retries=3, delay=1):
    """
    Decorator to retry function on failure
    """
    pass

class URLShortener:
    """
    URL Shortener class with async methods
    """
    
    async def validate_url(self, url):
        """
        Asynchronously validate if URL is accessible
        """
        pass
    
    async def batch_create_urls(self, urls):
        """
        Create multiple URLs concurrently
        """
        pass

def generate_unique_codes(count=100):
    """
    Generate unique short codes using generator
    """
    pass
```

**Solution**:
```python
def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class URLShortener:
    async def validate_url(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(url, timeout=10) as response:
                    return response.status < 400
        except:
            return False
    
    async def batch_create_urls(self, urls):
        tasks = [self.validate_url(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

def generate_unique_codes(count=100):
    import string
    import random
    
    used_codes = set()
    while len(used_codes) < count:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if code not in used_codes:
            used_codes.add(code)
            yield code
```

---

## 🧪 Testing Your Solutions

### 1. **Set Up Your Environment**
```bash
# Install dependencies
pip install pymongo redis fastapi uvicorn aiohttp

# Start MongoDB (if using Docker)
docker run -d -p 27017:27017 mongo

# Start Redis (if using Docker)
docker run -d -p 6379:6379 redis
```

### 2. **Run Your Code**
```python
# Test MongoDB functions
if __name__ == "__main__":
    # Test your functions here
    url_id = create_url("https://example.com", "test123")
    print(f"Created URL with ID: {url_id}")
    
    url = get_url_by_code("test123")
    print(f"Retrieved URL: {url}")
```

### 3. **Common Issues to Watch For**
- Connection errors to databases
- Missing error handling
- Incorrect data types
- Memory leaks in async code
- Race conditions in concurrent operations

---

## 📚 Additional Practice Problems

### **Easy Level:**
1. Create a simple counter API using FastAPI
2. Implement basic CRUD operations with SQLite
3. Build a simple caching system with Python dictionaries

### **Medium Level:**
1. Implement user authentication with JWT tokens
2. Create a rate limiting middleware
3. Build a simple analytics dashboard

### **Hard Level:**
1. Implement URL expiration and cleanup
2. Build a distributed caching system
3. Create a URL validation service with multiple checks

---

## 🎯 Interview Tips

### **During the Interview:**
1. **Think Aloud**: Explain your thought process
2. **Ask Questions**: Clarify requirements before coding
3. **Start Simple**: Begin with a basic solution, then optimize
4. **Handle Errors**: Show you think about edge cases
5. **Test Your Code**: Run through examples verbally

### **Code Quality:**
1. **Clean Code**: Use meaningful variable names
2. **Error Handling**: Include try-catch blocks
3. **Documentation**: Add comments for complex logic
4. **Efficiency**: Consider time and space complexity
5. **Security**: Think about input validation and sanitization

---

**Practice these exercises regularly and you'll be well-prepared for your interview!** 🚀
