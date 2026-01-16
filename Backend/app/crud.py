from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models import WikiQuiz

def get_by_url(db: Session, url: str) -> WikiQuiz | None:
    return db.execute(select(WikiQuiz).where(WikiQuiz.url == url)).scalar_one_or_none()

def get_by_id(db: Session, quiz_id: int) -> WikiQuiz | None:
    return db.get(WikiQuiz, quiz_id)

def list_quizzes(db: Session, limit: int = 50, offset: int = 0) -> list[WikiQuiz]:
    stmt = select(WikiQuiz).order_by(WikiQuiz.created_at.desc()).limit(limit).offset(offset)
    return list(db.execute(stmt).scalars().all())

def create_quiz(
    db: Session,
    *,
    url: str,
    title: str,
    summary: str | None,
    sections: list[str],
    key_entities: dict,
    quiz: list,
    related_topics: list[str],
    raw_html: str | None = None
) -> WikiQuiz:
    row = WikiQuiz(
        url=url,
        title=title,
        summary=summary,
        sections=sections,
        key_entities=key_entities,
        quiz=quiz,
        related_topics=related_topics,
        raw_html=raw_html,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
