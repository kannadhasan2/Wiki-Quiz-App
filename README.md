# 🧠 Wikipedia Quiz Generator – Full Stack (FastAPI + Gemini + Supabase + React + Tailwind)

This project is a **full-stack application** that accepts a **Wikipedia article URL**, scrapes its HTML content, generates a **quiz using a Large Language Model (Google Gemini via LangChain)**, and stores all results in a **PostgreSQL database (Supabase)**.

It includes:
- ✅ FastAPI backend (scraping + LLM + DB storage)
- ✅ React + Tailwind frontend (2 tabs + modal)
- ✅ History view backed by Supabase PostgreSQL
- ✅ Caching to avoid duplicate LLM calls

---

## 🌍 Deployment

- **Backend (FastAPI Render)**: https://wiki-quiz-app-sauw.onrender.com  
- **Frontend**: https://wiki-quiz-app-two.vercel.app/

> Local frontend runs at: `http://localhost:5173`

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

  ### Frontend
- Clean minimal UI with Tailwind
- Two tabs:
  - **Generate Quiz**
  - **Past Quizzes (History)**
- Card-based quiz layout
- History table + Details modal
- Optional “Take Quiz” mode (if enabled in UI)


---

## 🏗️ Tech Stack

- **Backend:** FastAPI (Python)
- **LLM:** Google Gemini (via LangChain)
- **Database:** PostgreSQL (Supabase)
- **Scraping:** BeautifulSoup (HTML only)
- **ORM:** SQLAlchemy
- **Environment:** Python 3.10+

### Frontend
- **React + Vite**
- **Tailwind CSS**
- Fetch API
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


Frontend/
│
├── src/
│   ├── components/
│   │   ├── QuizCard.jsx    # Quiz card UI
│   │   └── Modal.jsx       # Reusable modal
│   ├── api.js              # Backend API calls
│   ├── App.jsx             # Main app (Tabs: Generate + History)
│   ├── main.jsx            # React entry point
│   └── index.css           # Tailwind CSS styles
│
├── index.html
├── tailwind.config.js
├── postcss.config.js
├── vite.config.js
└── package.json


```


---
## 📦 Installation

### Prerequisites
- Python **3.10+**
- Node.js **18+**
- PostgreSQL (Supabase)
- Git

---

## 🔧 Backend Installation (FastAPI)

### 1️⃣ Clone the repository
```bash
git clone <YOUR_REPOSITORY_URL>
cd Backend
```

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
```

## 🎨 Frontend Installation (React + Tailwind CSS)

### Prerequisites
- Node.js **18+**
- npm (comes with Node.js)

---

### 1️⃣ Navigate to frontend directory
```bash
cd Frontend
npm install
npm run dev
```
### 2️⃣ Configure backend API URL
### Edit Frontend/src/api.js:
```
const BASE_URL = "http://localhost:8000";
// or deployed backend:
// const BASE_URL = "https://wiki-quiz-app-sauw.onrender.com";
```
