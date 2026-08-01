# Decipher – AI-Powered Fact Verification System

An AI-powered fact verification platform that validates textual claims using **live web evidence** and **Large Language Models (LLMs)** to deliver transparent, explainable, and evidence-backed verification results.

---

## Overview

The rapid spread of misinformation across digital platforms has made verifying information more challenging than ever. Search engines often return numerous results without a definitive conclusion, while standalone LLMs may generate responses that are inaccurate or unsupported.

**Decipher** addresses this challenge by combining **live web evidence retrieval** with **AI-powered reasoning**. The system analyzes user-provided claims, retrieves relevant evidence from trusted online sources, and generates a structured verification report containing a verdict, confidence score, explanation, and supporting references.

---

## Key Features

- 🔍 AI-powered fact verification
- 📄 Automatic claim extraction
- 🔄 Intelligent query rewriting
- 🌐 Live evidence retrieval
- 🤖 LLM-based reasoning using Groq
- 📊 Confidence score generation
- 📝 Explainable verdicts
- 🔗 Supporting source references
- 💻 Modern and responsive user interface

---

## Technology Stack

### Frontend
- React.js
- Vite
- Axios
- HTML5
- CSS3

### Backend
- FastAPI
- Python

### AI Services
- Groq API
- Llama 3.1 8B Instant

### Evidence Retrieval
- Tavily Search API

---

## System Workflow

```text
User Claim
      │
      ▼
Claim Extraction
      │
      ▼
Query Rewriting
      │
      ▼
Evidence Retrieval
      │
      ▼
LLM Verification
      │
      ▼
Summary Generation
      │
      ▼
Result Presentation
```

---

## Project Architecture

```
ai_powered_fact_verification
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── services
│   │   ├── models
│   │   └── config
│   ├── requirements.txt
│   └── main.py
│
├── frontend
│   ├── src
│   │   ├── components
│   │   ├── services
│   │   └── styles
│   └── public
│
├── README.md
├── TEAM_DETAILS.md
├── DATABASE.md
├── SRS.pdf
└── Project_Report.pdf
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/pranithaa-p/ai_powered_fact_verification.git
cd ai_powered_fact_verification
```

---

### Backend Setup

```bash
cd backend

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## Environment Variables

Create a `.env` file inside the **backend** directory.

```env
GROQ_API_KEY=YOUR_GROQ_API_KEY
TAVILY_API_KEY=YOUR_TAVILY_API_KEY
```

For the frontend, create a `.env` file inside the **frontend** directory.

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

---

## Deployment

### Frontend

**Vercel**

https://ai-powered-fact-verification.vercel.app/

### Backend

**Render**

https://ai-powered-fact-verification.onrender.com

---

## API Endpoints

| Method | Endpoint | Description |
|----------|----------------|--------------------------------|
| GET | `/` | API Status |
| GET | `/api/health` | Health Check |
| POST | `/api/verify` | Verify textual claims |

---

## Why Decipher?

Unlike conventional search engines or standalone AI chatbots, Decipher follows a structured verification pipeline:

- Retrieves **live evidence** instead of relying solely on pre-trained knowledge.
- Evaluates claims using **LLM reasoning** over retrieved evidence.
- Generates **transparent verdicts** with explanations and confidence scores.
- Provides **supporting references** for every verification result.
- Handles multiple factual claims within a single input.

This approach makes the verification process more reliable, explainable, and user-friendly.

---

## Future Enhancements

- Multilingual fact verification
- Image and video verification
- PDF and document verification
- Browser extension
- Verification history
- User authentication
- Batch claim verification
- Advanced source credibility analysis

---

## Team

| Name | Responsibility |
|------|----------------|
| **Pranitha P** | Backend Development, AI Integration, API Development, System Architecture |
| **Nethra B** | Frontend Development, UI/UX Design, Testing & Deployment |

---

## Live Demo

🌐 **Frontend:** https://ai-powered-fact-verification.vercel.app/

⚙️ **Backend API:** https://ai-powered-fact-verification.onrender.com

---

## License

This project was developed as part of a hackathon and academic initiative for educational and research purposes.
