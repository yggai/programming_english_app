"""
兼容旧版本的单词API路由
"""

from fastapi import APIRouter
from sqlmodel import Session
from typing import List, Dict, Any
import random

from ...db.database import get_session

router = APIRouter()


# 示例单词数据（兼容旧版本）
SAMPLE_WORDS = [
    {"id": 1, "word": "variable", "translation": "变量", "example": "let x = 10;"},
    {"id": 2, "word": "function", "translation": "函数", "example": "function hello() { return 'Hello'; }"},
    {"id": 3, "word": "array", "translation": "数组", "example": "const arr = [1, 2, 3];"},
    {"id": 4, "word": "object", "translation": "对象", "example": "const obj = { name: 'John' };"},
    {"id": 5, "word": "class", "translation": "类", "example": "class Person { constructor() {} }"},
    {"id": 6, "word": "method", "translation": "方法", "example": "obj.toString()"},
    {"id": 7, "word": "property", "translation": "属性", "example": "obj.name"},
    {"id": 8, "word": "loop", "translation": "循环", "example": "for(let i = 0; i < 10; i++) {}"},
    {"id": 9, "word": "condition", "translation": "条件", "example": "if (x > 0) {}"},
    {"id": 10, "word": "exception", "translation": "异常", "example": "try {} catch(e) {}"}
]


@router.get("/words", tags=["legacy"])
async def get_words():
    """
    兼容旧版本的单词列表端点
    
    Returns:
        Dict: 包含成功状态和单词列表的字典
    """
    return {"success": True, "data": SAMPLE_WORDS}


@router.get("/random-word", tags=["legacy"])
async def get_random_word():
    """
    兼容旧版本的随机单词端点
    
    Returns:
        Dict: 包含成功状态和随机单词的字典
    """
    random_word = random.choice(SAMPLE_WORDS)
    return {"success": True, "data": random_word}