from pydantic import BaseModel, Field, HttpUrl
from typing import Literal, List, Dict, Any

Difficulty = Literal["easy", "medium", "hard"]

class GenerateRequest(BaseModel):
    url: HttpUrl = Field(..., description="Wikipedia article URL")

class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(..., min_length=4, max_length=4)
    answer: str
    difficulty: Difficulty
    explanation: str

class KeyEntities(BaseModel):
    people: List[str] = []
    organizations: List[str] = []
    locations: List[str] = []

class QuizPayload(BaseModel):
    id: int
    url: str
    title: str
    summary: str | None = None
    key_entities: KeyEntities = Field(default_factory=KeyEntities)
    sections: List[str] = []
    quiz: List[QuizQuestion] = []
    related_topics: List[str] = []
    created_at: Any | None = None
    updated_at: Any | None = None

class QuizListItem(BaseModel):
    id: int
    url: str
    title: str
    created_at: Any | None = None
