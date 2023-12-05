import pymysql
from fastapi import HTTPException
from pydantic import BaseModel

class userName(BaseModel):
    account: str
    name: str

async def userInfo(account: str, conn: pymysql.connections.Connection):
    print(account)
    try:
        sql = "SELECT name FROM readers WHERE account = %s"
        with conn.cursor() as cursor:
            cursor.execute(sql, (account,))
            result = cursor.fetchone()

            return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



async def changeName(body: userName, conn: pymysql.connections.Connection):
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
