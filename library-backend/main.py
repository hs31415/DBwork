import pymysql
from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class UserRegistration(BaseModel):
    account: str
    password: str

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

@app.post('/register')
async def register(user_data: UserRegistration):
    try:
        account = user_data.account
        password = user_data.password
        # 创建游标对象
        with conn.cursor() as cursor:
            # 查询账号是否已存在
            sql = "SELECT COUNT(*) FROM readers WHERE account = %s"
            cursor.execute(sql, (account,))
            result = cursor.fetchone()
            if result[0] > 0:
                return {'message': '账号已存在'}
            # 执行插入操作
            sql = "INSERT INTO readers (account, name, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (account, f"用户{account}", password))
            # 提交事务
            conn.commit()
        return {'message': '注册成功'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/login')
async def login(user_data: UserRegistration):
    try:
        account = user_data.account
        password = user_data.password

        # 查询数据库中是否存在该读者
        sql = "SELECT * FROM readers WHERE account=%s AND password=%s"
        with conn.cursor() as cursor:
            cursor.execute(sql, (account, password))
            result = cursor.fetchone()
            if result is None:
                return {"message": "账号或密码错误"}
            else:
                # 登录成功，返回读者ID
                reader_id = result[0]
                return {"message": "登录成功", "readerId": reader_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/books/")
async def get_books():
    try:
        sql = "SELECT id, title, author, publisher, currentNum FROM books"
        with conn.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()

            books = []
            for result in results:
                book = {
                    "id": result[0],
                    "title": result[1],
                    "author": result[2],
                    "publisher": result[3],
                    "currentNum": result[4]
                }
                books.append(book)

            return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/book/{book_id}")
async def get_book_by_id(book_id: int):
    print(book_id)
    try:
        sql = "SELECT id, title, author, publisher, currentNum, description FROM books WHERE id = %s"
        with conn.cursor() as cursor:
            cursor.execute(sql, (book_id,))
            result = cursor.fetchone()

            if not result:
                raise HTTPException(status_code=404, detail="Book not found")

            book = {
                "id": result[0],
                "title": result[1],
                "author": result[2],
                "publisher": result[3],
                "currentNum": result[4],
                "description": result[5]
            }

            return book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
def shutdown_event():
    # 关闭数据库连接
    conn.close()

if __name__ == '__main__':
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, proxy_headers=True)
    finally:
        conn.close()
