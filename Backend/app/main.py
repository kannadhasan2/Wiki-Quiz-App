from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db import Base, engine, get_db
from app.schemas import GenerateRequest, QuizPayload, QuizListItem
from app.scraper import scrape_wikipedia
from app.llm import generate_quiz_payload
from app import crud
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Wiki Quiz Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # must be False when using "*"
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"ok": True}

@app.post("/generate-quiz", response_model=QuizPayload)
def generate_quiz(req: GenerateRequest, db: Session = Depends(get_db)):
    url = str(req.url)

    # Cache: if already exists, return it immediately
    existing = crud.get_by_url(db, url)
    if existing:
        return QuizPayload(
            id=existing.id,
            url=existing.url,
            title=existing.title,
            summary=existing.summary,
            sections=existing.sections or [],
            key_entities=existing.key_entities or {},
            quiz=existing.quiz or [],
            related_topics=existing.related_topics or [],
            created_at=existing.created_at,
            updated_at=existing.updated_at,
        )

    # 1) scrape
    try:
        scraped = scrape_wikipedia(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Scraping failed: {e}")

    # 2) llm generate
    try:
        llm_out = generate_quiz_payload(
            scraped["title"],
            scraped["summary"],
            scraped["sections"],
            scraped["full_text"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM generation failed: {e}")

    # 3) store
    try:
        saved = crud.create_quiz(
            db,
            url=url,
            title=scraped["title"],
            summary=scraped["summary"],
            sections=scraped["sections"],
            key_entities=llm_out.get("key_entities", {}),
            quiz=llm_out.get("quiz", []),
            related_topics=llm_out.get("related_topics", []),
            raw_html=scraped.get("raw_html"),
        )
    except IntegrityError:
        db.rollback()
        # If a race created it, return the cached one
        existing = crud.get_by_url(db, url)
        if existing:
            return QuizPayload(
                id=existing.id,
                url=existing.url,
                title=existing.title,
                summary=existing.summary,
                sections=existing.sections or [],
                key_entities=existing.key_entities or {},
                quiz=existing.quiz or [],
                related_topics=existing.related_topics or [],
                created_at=existing.created_at,
                updated_at=existing.updated_at,
            )
        raise HTTPException(status_code=500, detail="DB insert failed (IntegrityError).")

    return QuizPayload(
        id=saved.id,
        url=saved.url,
        title=saved.title,
        summary=saved.summary,
        sections=saved.sections or [],
        key_entities=saved.key_entities or {},
        quiz=saved.quiz or [],
        related_topics=saved.related_topics or [],
        created_at=saved.created_at,
        updated_at=saved.updated_at,
    )

@app.get("/quizzes", response_model=list[QuizListItem])
def list_quizzes(limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    rows = crud.list_quizzes(db, limit=limit, offset=offset)
    return [
        QuizListItem(id=r.id, url=r.url, title=r.title, created_at=r.created_at)
        for r in rows
    ]

@app.get("/quizzes/{quiz_id}", response_model=QuizPayload)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    row = crud.get_by_id(db, quiz_id)
    if not row:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return QuizPayload(
        id=row.id,
        url=row.url,
        title=row.title,
        summary=row.summary,
        sections=row.sections or [],
        key_entities=row.key_entities or {},
        quiz=row.quiz or [],
        related_topics=row.related_topics or [],
        created_at=row.created_at,
        updated_at=row.updated_at,
    )
