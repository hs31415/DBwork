import pymysql
from fastapi import HTTPException
from pydantic import BaseModel

class borrowBody(BaseModel):
    account: str
    book_id: int

async def returnBook(body: borrowBody, conn: pymysql.connections.Connection):
    try:
        returnId = body.book_id
        account = body.account
        # 查询数据库中是否存在匹配的借阅记录
        select_sql = "SELECT * FROM borrow WHERE reader_account=%s AND book_id=%s"
        delete_sql = "DELETE FROM borrow WHERE reader_account=%s AND book_id=%s"
        update_sql = "UPDATE book SET isBorrow=0 WHERE id=%s"
        # 恢复书本数量
        sql = "SELECT book_id FROM book WHERE id=%s"
        update_books_sql = "UPDATE books SET currentNum=currentNum+1 WHERE id=%s"

        with conn.cursor() as cursor:
            cursor.execute(select_sql, (account, returnId))
            result = cursor.fetchone()

            if result is None:
                print("未找到对应的借阅记录")
                return {"message": "归还失败"}
            else:
                # 删除借阅记录并更新图书状态
                cursor.execute(sql, (returnId,))
                result = cursor.fetchone()
                cursor.execute(update_books_sql, (result[0],))
                cursor.execute(delete_sql, (account, returnId))
                cursor.execute(update_sql, (returnId,))
                conn.commit()
                return {"message": "归还成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))