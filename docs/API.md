# API Design

## Base URL

http://localhost:8000

---

## GET /

Description:
Returns a welcome message.

Response

```json
{
  "message": "Welcome to Decipher Fact Verification API"
}
```

---

## GET /api/health

Description:
Checks whether the backend service is running.

Response

```json
{
  "status": "healthy"
}
```

---

## POST /api/verify

Description:
Verifies a textual claim using Tavily Search and Groq Llama 3.x.

Request

```json
{
  "claim": "The Eiffel Tower is in Berlin."
}
```

Response

```json
{
  "verdict": "False",
  "confidence": 98,
  "explanation": "The Eiffel Tower is located in Paris, France.",
  "sources": []
}
```