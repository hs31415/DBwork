import pymysql
from fastapi import HTTPException
from pydantic import BaseModel

class bookInfo(BaseModel):
    title: str
    author: str
    publisher: str
    description: str

class bookNum(BaseModel):
    id: int
    number: int

async def get_books(conn: pymysql.connections.Connection):
    try:
        sql = "SELECT id, title, author, publisher, count, currentNum FROM books"
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
                    "count":result[4],
                    "currentNum": result[5]
                }
                books.append(book)

            return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def get_book_by_id(book_id: int,conn: pymysql.connections.Connection):
    print(book_id)
    try:
        sql = "SELECT id, title, author, publisher, count, currentNum, description FROM books WHERE id = %s"
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
                "count": result[4],
                "currentNum": result[5],
                "description": result[6]
            }

            return book
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def addBook(book_info: bookInfo,conn: pymysql.connections.Connection):
    print(book_info)
    title = book_info.title
    author = book_info.author
    publisher = book_info.publisher
    description = book_info.description
    try:
        # 先查询数据库中是否有相同的书籍信息
        with conn.cursor() as cursor:
            sql = "SELECT * FROM books WHERE title=%s AND author=%s AND publisher=%s"
            cursor.execute(sql, (title, author, publisher))
            result = cursor.fetchone()
            if result is not None:
                return {"message": "已有相同书籍"}

        # 若数据库中不存在相同的书籍信息，则插入一条数据
        with conn.cursor() as cursor:
            sql = "INSERT INTO books(title, author, publisher, description) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (title, author, publisher, description))
            conn.commit()
            return {"message": "添加成功"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def addNum(book_num: bookNum,conn: pymysql.connections.Connection):
    print(book_num)
    book_id = book_num.id
    num = book_num.number
    try:
        with conn.cursor() as cursor:
            # 调用存储过程
            cursor.callproc("insert_books", (book_id, num))
            conn.commit()
            return {"message": "添加图书成功"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

