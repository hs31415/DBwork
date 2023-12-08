import pymysql
from fastapi import HTTPException
from pydantic import BaseModel

class borrowBody(BaseModel):
    account: str
    book_id: int


async def borrowInfo(book_id: int,conn: pymysql.connections.Connection):
    print(book_id)
    try:
        sql = "SELECT id, isBorrow, borrower FROM book WHERE book_id = %s"
        with conn.cursor() as cursor:
            cursor.execute(sql, (book_id,))
            results = cursor.fetchall()

            borrows = []
            for result in results:
                borrow = {
                    'id': result[0],
                    'isborrow': result[1],
                    'borrower': result[2]
                }
                print(borrow)
                borrows.append(borrow)


            return borrows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def borrow(body: borrowBody,conn: pymysql.connections.Connection):
    try:
        borrowId = body.book_id
        account = body.account
        sql = "SELECT isBorrow, book_id FROM book WHERE id=%s"
        update_sql = "UPDATE book SET isBorrow=1 WHERE id=%s"
        insert_sql = "INSERT INTO borrow (reader_account, book_id) VALUES (%s, %s)"
        update_books_sql = "UPDATE books SET currentNum=currentNum-1 WHERE id=%s"
        update_borrower_sql = "UPDATE book SET borrower=%s WHERE id=%s"
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
                cursor.execute(update_books_sql, (result[1],))
                cursor.execute(update_borrower_sql, (account, borrowId))
                conn.commit()
                return {"message": "借阅成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def borrowRecord(account: str,conn: pymysql.connections.Connection):
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