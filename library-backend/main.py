import pymysql
import bcrypt
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from Login import login


class UserRegistration(BaseModel):
    account: str
    password: str


class borrowBody(BaseModel):
    account: str
    book_id: int


class changeName(BaseModel):
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

            # 使用bcrypt进行密码加密
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            print(hashed_password)
            # 执行插入操作
            sql = "INSERT INTO readers (account, name, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (account, f"用户{account}", hashed_password))
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
        sql = "SELECT * FROM readers WHERE account=%s"
        with conn.cursor() as cursor:
            cursor.execute(sql, (account,))
            result = cursor.fetchone()
            if result is None:
                return {"message": "账号或密码错误"}
            else:
                # 验证密码是否正确
                stored_password = result[2]
                print(stored_password)
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    # 登录成功，返回读者ID
                    reader_id = result[0]
                    return {"message": "登录成功", "readerId": reader_id}
                else:
                    return {"message": "账号或密码错误"}
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


@app.get("/borrowInfo/{book_id}")
async def borrowInfo(book_id: int):
    print(book_id)
    try:
        sql = "SELECT id, isBorrow FROM book WHERE book_id = %s"
        with conn.cursor() as cursor:
            cursor.execute(sql, (book_id,))
            results = cursor.fetchall()

            borrows = []
            for result in results:
                borrow = {
                    'id': result[0],
                    'isborrow': result[1]
                }
                borrows.append(borrow)


            return borrows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/borrow')
async def borrow(body: borrowBody):
    try:
        borrowId = body.book_id
        account = body.account
        # 查询数据库中是否存在该读者
        sql = "SELECT isBorrow FROM book WHERE id=%s"
        update_sql = "UPDATE book SET isBorrow=1 WHERE id=%s"
        insert_sql = "INSERT INTO borrow (reader_account, book_id) VALUES (%s, %s)"
        with conn.cursor() as cursor:
            cursor.execute(sql, (borrowId,))
            result = cursor.fetchone()

            print(result[0])

            if result[0]:
                print("书已经借出")
                return {"message": "借阅失败"}
            else:
                print("借出图书")
                cursor.execute(update_sql, (borrowId,))
                cursor.execute(insert_sql, (account, borrowId))
                conn.commit()
                return {"message": "借阅成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/borrowRecord/{account}")
async def borrowRecord(account: str):
    print(account)
    try:
        sql = """
        SELECT borrow.book_id, books.title
        FROM borrow
        INNER JOIN book ON borrow.book_id = book.id
        INNER JOIN books ON book.book_id = books.id
        WHERE reader_account = %s
        """
        with conn.cursor() as cursor:
            cursor.execute(sql, (account,))
            results = cursor.fetchall()

            borrowRecords = []
            for result in results:
                borrowRecord = {
                    'id': result[0],
                    'title': result[1]
                }
                borrowRecords.append(borrowRecord)
            return borrowRecords
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/returnBook')
async def returnBook(body: borrowBody):
    try:
        returnId = body.book_id
        account = body.account
        # 查询数据库中是否存在匹配的借阅记录
        select_sql = "SELECT * FROM borrow WHERE reader_account=%s AND book_id=%s"
        delete_sql = "DELETE FROM borrow WHERE reader_account=%s AND book_id=%s"
        update_sql = "UPDATE book SET isBorrow=0 WHERE id=%s"

        with conn.cursor() as cursor:
            cursor.execute(select_sql, (account, returnId))
            result = cursor.fetchone()

            if result is None:
                print("未找到对应的借阅记录")
                return {"message": "归还失败"}
            else:
                # 删除借阅记录并更新图书状态
                cursor.execute(delete_sql, (account, returnId))
                cursor.execute(update_sql, (returnId,))
                conn.commit()
                return {"message": "归还成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/userInfo/{account}")
async def userInfo(account: str):
    print(account)
    try:
        sql = "SELECT name FROM readers WHERE account = %s"
        with conn.cursor() as cursor:
            cursor.execute(sql, (account,))
            result = cursor.fetchone()

            return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post('/changeName')
async def changeName(body: changeName):
    try:
        account = body.account
        name = body.name
        print(account)
        print(name)
        sql = "UPDATE readers SET name = %s WHERE account = %s"
        with conn.cursor() as cursor:
            cursor.execute(sql, (name, account))

        conn.commit()

        return {"message": "修改成功"}

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
