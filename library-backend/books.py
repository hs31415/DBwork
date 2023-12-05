import pymysql
from fastapi import HTTPException

async def get_books(conn: pymysql.connections.Connection):
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



async def get_book_by_id(book_id: int,conn: pymysql.connections.Connection):
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

