from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ...db.database import get_session
from ...models.word import Word, WordCreate, WordUpdate, WordRead
from ...services.word_service import WordService
from ...utils.deps import get_current_active_user
from ...models.user import User

router = APIRouter(prefix="/words", tags=["words"])


@router.get("/", response_model=List[WordRead])
async def get_words(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """获取单词列表"""
    word_service = WordService(session)
    words = word_service.get_words(skip=skip, limit=limit)
    return words


@router.get("/{word_id}", response_model=WordRead)
async def get_word(
    word_id: int,
    session: Session = Depends(get_session)
):
    """获取单个单词"""
    word_service = WordService(session)
    word = word_service.get_word_by_id(word_id)
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found"
        )
    return word


@router.post("/", response_model=WordRead)
async def create_word(
    word_create: WordCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """创建新单词"""
    word_service = WordService(session)
    # 检查单词是否已存在
    existing_word = word_service.get_word_by_word(word_create.word)
    if existing_word:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Word already exists"
        )
    
    word = word_service.create_word(word_create)
    return word


@router.put("/{word_id}", response_model=WordRead)
async def update_word(
    word_id: int,
    word_update: WordUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """更新单词"""
    word_service = WordService(session)
    word = word_service.update_word(word_id, word_update)
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found"
        )
    return word


@router.delete("/{word_id}")
async def delete_word(
    word_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """删除单词"""
    word_service = WordService(session)
    success = word_service.delete_word(word_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Word not found"
        )
    return {"message": "Word deleted successfully"}


@router.get("/random/", response_model=WordRead)
async def get_random_word(
    session: Session = Depends(get_session)
):
    """获取随机单词"""
    word_service = WordService(session)
    word = word_service.get_random_word()
    if not word:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No words available"
        )
    return word


@router.get("/category/{category}", response_model=List[WordRead])
async def get_words_by_category(
    category: str,
    session: Session = Depends(get_session)
):
    """根据分类获取单词"""
    word_service = WordService(session)
    words = word_service.get_words_by_category(category)
    return words


@router.get("/difficulty/{difficulty}", response_model=List[WordRead])
async def get_words_by_difficulty(
    difficulty: str,
    session: Session = Depends(get_session)
):
    """根据难度获取单词"""
    word_service = WordService(session)
    words = word_service.get_words_by_difficulty(difficulty)
    return words