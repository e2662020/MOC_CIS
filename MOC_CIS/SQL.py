# -*- coding: UTF-8 -*-
# 导入pymysql模块
import pymysql
import json
from pymysql.converters import escape_string

# 建立数据库连接
conn = pymysql.connect(
    host='localhost',  # 主机名（或IP地址）
    port=3306,  # 端口号，默认为3306
    user='root',  # 用户名
    password='837322bc635b0e2b',  # 密码
    charset='utf8mb4'  # 设置字符编码
)

# 获取mysql服务信息（测试连接，会输出MySQL版本号）
print(conn.get_server_info())


def find_key(key):
    conn.ping(reconnect=True)
    cursor = conn.cursor()

    # 选择数据库
    conn.select_db("key")

    # 查表
    cursor.execute('SELECT * FROM `MAIN`;')

    # 获取查询结果，返回result
    result: tuple = cursor.fetchall()
    cursor.close()
    conn.close()

    for i in result:
        if i[0] == key:
            return True
            # break

    return False


def login(username, pwd):
    conn.ping(reconnect=True)
    cursor = conn.cursor()

    # 选择数据库
    conn.select_db("user")

    # 查表
    cursor.execute('SELECT * FROM `MAIN`;')

    # 获取查询结果，返回result
    result: tuple = cursor.fetchall()
    cursor.close()
    conn.close()
    for i in result:
        if i[0] == username:
            if i[1] == pwd:
                return True
            else:
                return False
    return False


def sign(username, pwd, key):
    new = str((username, pwd))

    a = find_key(key)

    if a == True:
        cursor = conn.cursor()
        conn.ping(reconnect=True)
        conn.select_db("key")
        sql = 'DELETE FROM `MAIN` WHERE `KEY` = %s'
        cursor.execute(sql, (key))

        cursor = conn.cursor()
        conn.ping(reconnect=True)
        # 选择数据库
        conn.select_db("user")

        print(new)
        sql = "INSERT INTO MAIN (USERNAME,PASSWORD) VALUES " + new

        print(sql)
        cursor.execute(sql)
        conn.commit()

        cursor.close()
        conn.close()

        return True
    else:
        return False
    # return False

# a = open("KEY.json", "r").read()
# text = json.loads(a)
# print(text)
# cursor = conn.cursor()
# # 选择数据库
# conn.select_db("key")
# for i in text:
#     text = str((i))
#     print(i)
#     sql = 'INSERT INTO MAIN VALUES ("'+text+'")'

#     print(sql)
#     cursor.execute(sql)
#     conn.commit()

# cursor.close()
# conn.close()

