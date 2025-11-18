from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Programming English API", version="1.0.0")

# 配置CORS以允许Flutter应用访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to Programming English API"}

@app.get("/api/words")
async def get_words():
    """返回编程英语单词列表"""
    words = [
        {"id": 1, "word": "variable", "translation": "变量", "example": "let x = 10;"},
        {"id": 2, "word": "function", "translation": "函数", "example": "function hello() { return 'Hello'; }"},
        {"id": 3, "word": "array", "translation": "数组", "example": "const arr = [1, 2, 3];"},
        {"id": 4, "word": "object", "translation": "对象", "example": "const obj = { name: 'John' };"},
        {"id": 5, "word": "class", "translation": "类", "example": "class Person { constructor() {} }"}
    ]
    return {"success": True, "data": words}

@app.get("/api/random-word")
async def get_random_word():
    """返回随机编程英语单词"""
    import random
    words = [
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
    random_word = random.choice(words)
    return {"success": True, "data": random_word}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)