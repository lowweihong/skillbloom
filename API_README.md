# 🚀 Learning Plan Generator - Backend API

A **FastAPI-based REST API** that provides backend services for the Learning Plan Generator, allowing frontend applications to create personalized learning plans through HTTP requests.

## ✨ Features

- **🔌 RESTful API** - Standard HTTP endpoints for all operations
- **🌐 CORS Enabled** - Cross-origin requests supported for web frontends
- **📚 Auto-generated Docs** - Interactive API documentation with Swagger UI
- **⚡ Fast Performance** - Built with FastAPI and Uvicorn
- **🔒 Error Handling** - Comprehensive error handling and validation
- **📊 Request Tracking** - Unique request IDs for plan retrieval
- **🔄 Batch Processing** - Generate multiple plans in a single request

## 🏗️ Architecture

```
Frontend Application → HTTP Requests → FastAPI Backend → LangChain AI Agents → Learning Plan
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
# Create .env file
echo "GOOGLE_API_KEY=your_gemini_api_key_here" > .env
```

### 3. Start the Backend Server
```bash
python start_backend.py
```

### 4. Access API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔌 API Endpoints

### Base URL
```
http://localhost:8000
```

### Core Endpoints

#### 1. Generate Learning Plan
```http
POST /api/v1/generate-plan
```

**Request Body:**
```json
{
  "topic": "Python Programming",
  "background": "Complete beginner with no programming experience",
  "preferred_format": "video",
  "user_id": "user123",
  "session_id": "session456"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Learning plan generated successfully",
  "data": {
    "user_input": {...},
    "knowledge_gap": {...},
    "topic_plan": {...},
    "topic_details": [...],
    "learning_path": "...",
    "recommended_resources": [...],
    "timeline": "...",
    "success_metrics": [...]
  },
  "timestamp": "2025-01-27T10:30:00",
  "request_id": "uuid-here"
}
```

#### 2. Retrieve Learning Plan
```http
GET /api/v1/plan/{request_id}
```

#### 3. List Recent Plans
```http
GET /api/v1/plans?limit=10&offset=0
```

#### 4. Delete Learning Plan
```http
DELETE /api/v1/plan/{request_id}
```

#### 5. Batch Generate Plans
```http
POST /api/v1/batch-generate
```

**Request Body:**
```json
[
  {
    "topic": "Python Programming",
    "background": "Beginner",
    "preferred_format": "video"
  },
  {
    "topic": "Machine Learning",
    "background": "Intermediate Python",
    "preferred_format": "text"
  }
]
```

### Utility Endpoints

#### Health Check
```http
GET /health
```

#### API Information
```http
GET /
```

## 🌐 Frontend Integration

### JavaScript/HTML Frontend

```html
<!DOCTYPE html>
<html>
<head>
    <title>Learning Plan Generator</title>
</head>
<body>
    <form id="planForm">
        <input type="text" id="topic" placeholder="Topic to learn" required>
        <textarea id="background" placeholder="Your background" required></textarea>
        <select id="format" required>
            <option value="video">Video</option>
            <option value="text">Text</option>
            <option value="audio">Audio</option>
        </select>
        <button type="submit">Generate Plan</button>
    </form>

    <div id="result"></div>

    <script>
        document.getElementById('planForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = {
                topic: document.getElementById('topic').value,
                background: document.getElementById('background').value,
                preferred_format: document.getElementById('format').value
            };

            try {
                const response = await fetch('http://localhost:8000/api/v1/generate-plan', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('result').innerHTML = 
                        `<h3>✅ Plan Generated!</h3>
                         <p>Request ID: ${result.data.request_id}</p>
                         <p>Topics: ${result.data.topic_plan.main_topics.join(', ')}</p>`;
                } else {
                    document.getElementById('result').innerHTML = 
                        `<h3>❌ Error: ${result.message}</h3>`;
                }
            } catch (error) {
                document.getElementById('result').innerHTML = 
                    `<h3>❌ Network Error: ${error.message}</h3>`;
            }
        });
    </script>
</body>
</html>
```

### Python Frontend Client

```python
from frontend_client import LearningPlanAPIClient

# Initialize client
client = LearningPlanAPIClient("http://localhost:8000")

# Generate learning plan
result = client.generate_plan(
    topic="Machine Learning",
    background="I have intermediate Python skills",
    preferred_format="video"
)

if result.get("success"):
    print(f"✅ Plan generated! ID: {result['data']['request_id']}")
    print(f"📚 Topics: {result['data']['topic_plan']['main_topics']}")
else:
    print(f"❌ Failed: {result.get('message', 'Unknown error')}")
```

### React Frontend Example

```jsx
import React, { useState } from 'react';

function LearningPlanForm() {
    const [formData, setFormData] = useState({
        topic: '',
        background: '',
        preferred_format: 'video'
    });
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await fetch('http://localhost:8000/api/v1/generate-plan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            setResult(data);
        } catch (error) {
            setResult({ success: false, message: error.message });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    placeholder="Topic to learn"
                    value={formData.topic}
                    onChange={(e) => setFormData({...formData, topic: e.target.value})}
                    required
                />
                <textarea
                    placeholder="Your background"
                    value={formData.background}
                    onChange={(e) => setFormData({...formData, background: e.target.value})}
                    required
                />
                <select
                    value={formData.preferred_format}
                    onChange={(e) => setFormData({...formData, preferred_format: e.target.value})}
                >
                    <option value="video">Video</option>
                    <option value="text">Text</option>
                    <option value="audio">Audio</option>
                </select>
                <button type="submit" disabled={loading}>
                    {loading ? 'Generating...' : 'Generate Plan'}
                </button>
            </form>

            {result && (
                <div>
                    {result.success ? (
                        <div>
                            <h3>✅ Plan Generated!</h3>
                            <p>Request ID: {result.data.request_id}</p>
                            <p>Topics: {result.data.topic_plan.main_topics.join(', ')}</p>
                        </div>
                    ) : (
                        <div>
                            <h3>❌ Error: {result.message}</h3>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}

export default LearningPlanForm;
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Gemini API key | Yes |

### Server Configuration

- **Host**: 0.0.0.0 (accessible from any IP)
- **Port**: 8000
- **CORS**: Enabled for all origins (configure for production)
- **Logging**: Info level with request/response logging

## 📊 Response Format

All API responses follow a consistent format:

```json
{
  "success": boolean,
  "message": "Human-readable message",
  "data": object | null,
  "error": "Error details" | null,
  "timestamp": "ISO 8601 timestamp",
  "request_id": "UUID string"
}
```

## 🚨 Error Handling

### HTTP Status Codes

- **200**: Success
- **400**: Bad Request (validation error)
- **404**: Not Found
- **500**: Internal Server Error

### Error Response Format

```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error information",
  "timestamp": "2025-01-27T10:30:00",
  "request_id": ""
}
```

## 🔒 Security Considerations

### Production Deployment

1. **CORS Configuration**: Restrict allowed origins
2. **Rate Limiting**: Implement API rate limiting
3. **Authentication**: Add JWT or API key authentication
4. **HTTPS**: Use SSL/TLS encryption
5. **Input Validation**: Validate all user inputs
6. **Logging**: Monitor API usage and errors

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["*"],
)
```

## 📈 Performance & Scaling

### Current Implementation

- **In-memory Storage**: Plans stored in memory (not persistent)
- **Single Process**: Single worker process
- **Synchronous Processing**: Blocking API calls

### Production Improvements

1. **Database Storage**: Use PostgreSQL/MongoDB for persistence
2. **Redis Caching**: Cache frequently accessed plans
3. **Async Processing**: Implement background job queues
4. **Load Balancing**: Multiple worker processes
5. **CDN**: Static file delivery optimization

## 🧪 Testing

### Test the API

```bash
# Start the server
python start_backend.py

# Test with curl
curl -X POST "http://localhost:8000/api/v1/generate-plan" \
     -H "Content-Type: application/json" \
     -d '{
       "topic": "Python Programming",
       "background": "Complete beginner",
       "preferred_format": "video"
     }'

# Test health check
curl "http://localhost:8000/health"
```

### Run Frontend Examples

```bash
# Python client demo
python frontend_client.py

# Open HTML frontend in browser
open frontend_example.html
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

```bash
# Production environment
export GOOGLE_API_KEY=your_production_key
export ENVIRONMENT=production
export LOG_LEVEL=warning
```

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Uvicorn Documentation**: https://www.uvicorn.org/
- **LangChain Documentation**: https://python.langchain.com/
- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph/

## 🤝 Support

For questions or issues:

1. Check the API documentation at `/docs`
2. Review error logs in the console
3. Test with the provided frontend examples
4. Ensure the Gemini API key is properly configured

---

**Happy Learning Plan Generation! 🎓✨** 