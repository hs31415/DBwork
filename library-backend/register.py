import pymysql
import bcrypt
from fastapi import HTTPException
from pydantic import BaseModel

class UserRegistration(BaseModel):
    account: str
    password: str

async def register(user_data: UserRegistration, conn: pymysql.connections.Connection):
    try:
        account = user_data.account
        password = user_data.password
        print(account)
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