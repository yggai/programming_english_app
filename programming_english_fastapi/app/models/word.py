from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Category(str, Enum):
    BASIC = "basic"
    CONTROL_FLOW = "control_flow"
    DATA_STRUCTURE = "data_structure"
    OBJECT_ORIENTED = "object_oriented"
    FUNCTION = "function"
    ERROR_HANDLING = "error_handling"


class WordBase(SQLModel):
    word: str = Field(index=True)
    translation: str
    definition: str
    example: str
    category: Category = Field(default=Category.BASIC)
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.BEGINNER)
    pronunciation: Optional[str] = None


class Word(WordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class WordCreate(WordBase):
    pass


class WordUpdate(SQLModel):
    word: Optional[str] = None
    translation: Optional[str] = None
    definition: Optional[str] = None
    example: Optional[str] = None
    category: Optional[Category] = None
    difficulty: Optional[DifficultyLevel] = None
    pronunciation: Optional[str] = None


class WordRead(WordBase):
    id: int
    created_at: datetime
    updated_at: datetime


class LearningRecordBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")
    word_id: int = Field(foreign_key="word.id")
    correct_count: int = Field(default=0)
    incorrect_count: int = Field(default=0)
    mastery_level: int = Field(default=0, ge=0, le=5)


class LearningRecord(LearningRecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    last_reviewed: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class LearningRecordCreate(LearningRecordBase):
    pass


class LearningRecordRead(LearningRecordBase):
    id: int
    last_reviewed: datetime
    created_at: datetime