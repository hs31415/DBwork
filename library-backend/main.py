import pymysql
import bcrypt
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from login import login
from register import register
from books import get_book_by_id, get_books
from borrow import borrowRecord, borrow, borrowInfo
from returnbook import returnBook
from userinfo import userInfo, changeName

class UserRegistration(BaseModel):
    account: str
    password: str


class borrowBody(BaseModel):
    account: str
    book_id: int


class userName(BaseModel):
    account: str
    name: str


app = FastAPI()
# 添加跨域请求中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的跨域请求，也可以设置为特定的来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# 连接 MySQL 数据库
conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='741852',
    database='mylibrary',
)

# 将连接对象传递给视图函数
@app.post("/register")
async def register_router(user_data: UserRegistration):
    return await register(user_data, conn)

@app.post("/login")
async def login_router(user_data: UserRegistration):
    return await login(user_data, conn)

@app.get("/get_books")
async def get_books_router():
    return await get_books(conn)

@app.get("/get_book_by_id/{book_id}")
async def get_books_router_router(book_id: int):
    return await get_book_by_id(book_id, conn)

@app.get("/borrowInfo/{book_id}")
async def borrowInfo_router(book_id: int):
    return await borrowInfo(book_id, conn)
@app.post('/borrow')
async def borrow_router(body: borrowBody):
    return await borrow(body, conn)

@app.get("/borrowRecord/{account}")
async def borrowRecord_router(account: str):
    return await borrowRecord(account, conn)

@app.post('/returnBook')
async def returnBook_router(body: borrowBody):
    return await returnBook(body, conn)


@app.get("/userInfo/{account}")
async def userInfo_router(account: str):
    return await userInfo(account, conn)

@app.post('/changeName')
async def changeName_router(body: userName):
    return await changeName(body, conn)


@app.on_event("shutdown")
def shutdown_event():
    # 关闭数据库连接
    conn.close()

if __name__ == '__main__':
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, proxy_headers=True)
    finally:
        conn.close()
