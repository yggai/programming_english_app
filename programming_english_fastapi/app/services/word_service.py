from typing import List, Optional
from sqlmodel import Session, select
from ..models.word import Word, WordCreate, WordUpdate


class WordService:
    """单词服务类"""

    def __init__(self, session: Session):
        self.session = session

    def create_word(self, word_create: WordCreate) -> Word:
        """创建新单词"""
        word = Word.model_validate(word_create)
        self.session.add(word)
        self.session.commit()
        self.session.refresh(word)
        return word

    def get_word_by_id(self, word_id: int) -> Optional[Word]:
        """根据ID获取单词"""
        statement = select(Word).where(Word.id == word_id)
        result = self.session.exec(statement)
        return result.first()

    def get_word_by_word(self, word_text: str) -> Optional[Word]:
        """根据单词文本获取单词"""
        statement = select(Word).where(Word.word == word_text)
        result = self.session.exec(statement)
        return result.first()

    def get_words(self, skip: int = 0, limit: int = 100) -> List[Word]:
        """获取单词列表"""
        statement = select(Word).offset(skip).limit(limit)
        result = self.session.exec(statement)
        return result.all()

    def get_words_by_category(self, category: str) -> List[Word]:
        """根据分类获取单词"""
        statement = select(Word).where(Word.category == category)
        result = self.session.exec(statement)
        return result.all()

    def get_words_by_difficulty(self, difficulty: str) -> List[Word]:
        """根据难度获取单词"""
        statement = select(Word).where(Word.difficulty == difficulty)
        result = self.session.exec(statement)
        return result.all()

    def update_word(self, word_id: int, word_update: WordUpdate) -> Optional[Word]:
        """更新单词"""
        word = self.get_word_by_id(word_id)
        if not word:
            return None
        
        word_data = word_update.model_dump(exclude_unset=True)
        for key, value in word_data.items():
            setattr(word, key, value)
        
        self.session.add(word)
        self.session.commit()
        self.session.refresh(word)
        return word

    def delete_word(self, word_id: int) -> bool:
        """删除单词"""
        word = self.get_word_by_id(word_id)
        if not word:
            return False
        
        self.session.delete(word)
        self.session.commit()
        return True

    def get_random_word(self) -> Optional[Word]:
        """获取随机单词"""
        import random
        words = self.get_words()
        if not words:
            return None
        return random.choice(words)