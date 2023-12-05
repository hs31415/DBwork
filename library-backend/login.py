import pymysql
import bcrypt
from fastapi import HTTPException
from pydantic import BaseModel

class UserRegistration(BaseModel):
    account: str
    password: str

async def login(user_data: UserRegistration, conn: pymysql.connections.Connection):
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

async def ADlogin(user_data: UserRegistration, conn: pymysql.connections.Connection):
    try:
        account = user_data.account
        password = user_data.password

        # 查询数据库中是否存在该读者
        sql = "SELECT password,account FROM admin WHERE account=%s"
        with conn.cursor() as cursor:
            cursor.execute(sql, (account,))
            result = cursor.fetchone()
            if result is None:
                return {"message": "账号或密码错误"}
            else:
                # 验证密码是否正确
                stored_password = result[0]
                print(stored_password)
                if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                    # 登录成功，返回管理员ID
                    admin_id = result[1]
                    return {"message": "登录成功", "adminId": admin_id}
                else:
                    return {"message": "账号或密码错误"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
