# Wikipedia Quiz Generator – Backend (FastAPI + Gemini + Supabase)

This project is a backend service that accepts a **Wikipedia article URL**, scrapes its HTML content, generates a **quiz using a Large Language Model (Gemini)**, and stores all results in a **PostgreSQL database (Supabase)**.  
It also provides a **history API** to retrieve previously generated quizzes.

---
##Deployment
**Backend**: https://wiki-quiz-app-sauw.onrender.com
**Frontend**: 
---

## ✨ Features

- Accepts Wikipedia article URLs (HTML scraping only)
- Scrapes article title, summary, sections, and full text
- Generates:
  - 5–10 multiple-choice quiz questions
  - 4 options per question
  - Correct answer
  - Difficulty level (easy / medium / hard)
  - Short explanation grounded in article content
- Extracts key entities (people, organizations, locations)
- Suggests related Wikipedia topics
- Stores all data in Supabase (PostgreSQL)
- Caching to prevent duplicate LLM calls
- Graceful handling of Gemini free-tier quota limits

---

## 🏗️ Tech Stack

- **Backend:** FastAPI (Python)
- **LLM:** Google Gemini (via LangChain)
- **Database:** PostgreSQL (Supabase)
- **Scraping:** BeautifulSoup (HTML only)
- **ORM:** SQLAlchemy
- **Environment:** Python 3.10+

```
Backend/
│
├── app/
│   ├── main.py        # FastAPI routes
│   ├── config.py      # Environment variables loader
│   ├── db.py          # Database connection (Supabase Postgres)
│   ├── models.py      # SQLAlchemy models
│   ├── schemas.py     # Pydantic schemas
│   ├── scraper.py     # Wikipedia HTML scraping
│   ├── llm.py         # Gemini + LangChain logic
│   ├── crud.py        # Database operations
│   └── __init__.py
│
├── requirements.txt   # Python dependencies
├── .env               # Environment variables
└── supabase.sql       # Supabase SQL schema (tables, triggers)

```


---

## 🗄️ Supabase Database Setup (Step-by-Step)

### 1️⃣ Create Supabase Project
- Go to https://supabase.com
- Create a new project
- Save the **database password**

### 2️⃣ Get Connection String
Supabase → **Project Settings → Database → Connection string (URI)**

Example: postgresql://postgres:<PASSWORD>@db.<PROJECT_REF>.supabase.co:5432/postgres?sslmode=require


### 3️⃣ Create Tables
Supabase → **SQL Editor** → Run:

```sql
create table if not exists wiki_quizzes (
  id bigserial primary key,
  url text not null unique,
  title text not null,
  summary text,
  sections jsonb not null default '[]'::jsonb,
  key_entities jsonb not null default '{}'::jsonb,
  quiz jsonb not null default '[]'::jsonb,
  related_topics jsonb not null default '[]'::jsonb,
  raw_html text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

## 🔐 Environment Variables (.env)

DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@db.YOUR_PROJECT_REF.supabase.co:5432/postgres?sslmode=require  
GEMINI_API_KEY=YOUR_GEMINI_API_KEY  
APP_ENV=development  

## 📦 Installation & Run

### 1️⃣ Install dependencies

pip install -r requirements.txt  

### 2️⃣ Start server

uvicorn app.main:app --reload --port 8000  

### 3️⃣ Health check

GET http://127.0.0.1:8000/health  

## 🔌 API Endpoints

### ▶ Generate Quiz

POST /generate-quiz  

#### Request

{
  "url": "https://en.wikipedia.org/wiki/Alan_Turing"
}

#### Response (sample)

{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "title": "Alan Turing",
  "summary": "Alan Turing was a British mathematician...",
  "key_entities": {
    "people": ["Alan Turing", "Alonzo Church"],
    "organizations": ["Bletchley Park"],
    "locations": ["United Kingdom"]
  },
  "sections": ["Early life", "World War II", "Legacy"],
  "quiz": [
    {
      "question": "What was Alan Turing’s contribution during WWII?",
      "options": [
        "Breaking the Enigma code",
        "Inventing radar",
        "Developing jet engines",
        "Atomic research"
      ],
      "answer": "Breaking the Enigma code",
      "difficulty": "medium",
      "explanation": "Mentioned in the World War II section."
    }
  ],
  "related_topics": ["Cryptography", "Enigma machine"]
}

### ▶ Get Quiz History

GET /quizzes  

Returns a list of previously processed Wikipedia URLs.

### ▶ Get Quiz Details

GET /quizzes/{id}  

Returns full quiz data for a specific record.

## 🧠 Prompt Design (LangChain)

Key design principles:

Uses only article content  
Explicit JSON schema  
Prevents hallucination  
Enforces difficulty levels  
Short grounded explanations  

The prompt strictly instructs the LLM to return valid JSON only.

## ⚠️ Gemini Free Tier Limitation

Gemini free tier allows ~20 requests per day per model  

To handle this:

URL-based caching prevents duplicate LLM calls  
Graceful 429 handling  
Cached quizzes are returned instantly  

This mirrors real-world production strategies for LLM cost and rate-limit control.

## 📁 Project Structure

