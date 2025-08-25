# 🚀 Quick Reference Cheat Sheet

## 🍃 MongoDB Commands

### Basic Operations
```javascript
// Connect
mongo
use url_shortener

// Insert
db.urls.insertOne({
    original_url: "https://example.com",
    short_code: "abc123",
    created_at: new Date(),
    clicks: 0
})

// Find
db.urls.findOne({short_code: "abc123"})
db.urls.find({clicks: {$gt: 100}})

// Update
db.urls.updateOne(
    {short_code: "abc123"},
    {$inc: {clicks: 1}}
)

// Delete
db.urls.deleteOne({short_code: "abc123"})

// Indexes
db.urls.createIndex({short_code: 1}, {unique: true})
db.urls.createIndex({clicks: -1})
```

---

## 🗄️ SQL Commands

### Basic Queries
```sql
-- Create table
CREATE TABLE urls (
    id SERIAL PRIMARY KEY,
    original_url TEXT NOT NULL,
    short_code VARCHAR(10) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    clicks INTEGER DEFAULT 0
);

-- Insert
INSERT INTO urls (original_url, short_code) 
VALUES ('https://example.com', 'abc123');

-- Select
SELECT * FROM urls WHERE clicks > 100;
SELECT short_code, COUNT(*) FROM urls GROUP BY short_code;

-- Update
UPDATE urls SET clicks = clicks + 1 WHERE short_code = 'abc123';

-- Delete
DELETE FROM urls WHERE short_code = 'abc123';
```

---

## 🔴 Redis Commands

### Basic Operations
```bash
# Connect
redis-cli

# String operations
SET url:abc123 "https://example.com"
GET url:abc123
SETEX url:abc123 3600 "https://example.com"  # Expire in 1 hour

# Hash operations
HSET user:123 clicks 0
HGET user:123 clicks
HINCRBY user:123 clicks 1

# List operations
LPUSH user:123:activity "clicked_url"
LRANGE user:123:activity 0 -1

# Set operations
SADD popular_urls "abc123"
SMEMBERS popular_urls

# Expiration
EXPIRE key 3600
TTL key
```

---

## 🐍 Python FastAPI

### Basic Setup
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Models
class URLRequest(BaseModel):
    original_url: str
    custom_code: str = None

# Endpoints
@app.post("/api/urls")
async def create_url(request: URLRequest):
    return {"message": "URL created"}

@app.get("/{short_code}")
async def redirect_url(short_code: str):
    return {"redirect": f"https://example.com/{short_code}"}

# Run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 🔑 Key Concepts

### Database Types
```
SQL Databases (PostgreSQL, MySQL):
- ACID compliance
- Structured data
- Relationships
- Complex queries

NoSQL (MongoDB):
- Flexible schema
- Horizontal scaling
- JSON-like documents
- High performance

In-Memory (Redis):
- Fastest access
- Temporary storage
- Caching
- Session management
```

### API Types
```
REST API:
- HTTP methods (GET, POST, PUT, DELETE)
- Stateless
- JSON/XML responses
- Standard status codes

GraphQL:
- Single endpoint
- Client specifies data needed
- Strong typing
- Efficient data fetching

gRPC:
- Protocol buffers
- High performance
- Bidirectional streaming
- Strong typing
```

### Python Features
```
Async/Await:
- Non-blocking I/O
- Concurrent operations
- Event loop
- Coroutines

Decorators:
- Function modification
- Cross-cutting concerns
- Clean code
- Reusable logic

Generators:
- Memory efficient
- Lazy evaluation
- Iterator pattern
- Infinite sequences
```

---

## 🚨 Common Interview Questions

### Quick Answers

**Q: What is the difference between MongoDB and PostgreSQL?**
**A**: MongoDB is NoSQL (document-based, flexible schema), PostgreSQL is SQL (relational, ACID compliant)

**Q: Why use Redis?**
**A**: Fastest access (in-memory), caching, session storage, real-time data

**Q: What are HTTP status codes?**
**A**: 2xx (success), 4xx (client error), 5xx (server error)

**Q: Explain async/await**
**A**: Non-blocking operations, allows concurrent execution, better performance for I/O operations

**Q: What is connection pooling?**
**A**: Reusing database connections instead of creating new ones for each request

---

## 📊 System Design Basics

### Scaling Strategies
```
Vertical Scaling:
- Increase server resources
- CPU, RAM, storage
- Limited by hardware

Horizontal Scaling:
- Add more servers
- Load balancing
- Distributed systems
- Better for high traffic
```

### Caching Strategies
```
Cache-Aside:
- Check cache first
- Update cache after database
- Simple but can have stale data

Write-Through:
- Update cache and database simultaneously
- Consistent but slower writes

Write-Behind:
- Update cache immediately
- Update database asynchronously
- Fast but can lose data
```

---

## 🛠️ Development Tools

### Database Tools
```
MongoDB: MongoDB Compass, Studio 3T
PostgreSQL: pgAdmin, DBeaver
Redis: RedisInsight, Redis Commander
```

### API Testing
```
Postman: REST API testing
Insomnia: API development
curl: Command line testing
```

### Python Tools
```
pip: Package management
venv: Virtual environments
pytest: Testing framework
black: Code formatting
flake8: Linting
```

---

## 📝 Interview Checklist

### Before Interview:
- [ ] Review your project code
- [ ] Practice coding problems
- [ ] Understand key concepts
- [ ] Prepare project explanations
- [ ] Set up development environment

### During Interview:
- [ ] Think aloud
- [ ] Ask clarifying questions
- [ ] Start with simple solutions
- [ ] Consider edge cases
- [ ] Test your code verbally

### After Interview:
- [ ] Reflect on questions
- [ ] Note areas for improvement
- [ ] Practice weak topics
- [ ] Update your knowledge

---

**Remember: Stay calm, think step by step, and don't be afraid to ask questions!** 🍀
