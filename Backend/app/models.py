from sqlalchemy import Text, DateTime, func, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base

class WikiQuiz(Base):
    __tablename__ = "wiki_quizzes"
    __table_args__ = (UniqueConstraint("url", name="uq_wiki_quizzes_url"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)

    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    sections: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)
    key_entities: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    quiz: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)
    related_topics: Mapped[dict] = mapped_column(JSONB, nullable=False, default=list)

    raw_html: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
