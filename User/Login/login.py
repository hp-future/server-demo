import json
from flask import Flask, request
import pymysql
from flask_cors import CORS

# 开启一个服务
server = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
CORS(server, resources=r'/*')


# 登录
@server.route('/login', methods=['POST'])
def login():
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', passwd='hp123456', port=3306, db='user', charset='utf8')
    cur = conn.cursor()  # 生成游标对象

    form = request.json

    data_1 = ''
    data_2 = ''
    for i in range(2):
        if i == 0:
            sql = "select account from `user` where account = %s"  # SQL语句
            cur.execute(sql, form['account'])  # 执行SQL语句
            data_1 = cur.fetchall()  # 通过fetchall方法获得数据
            if not data_1:
                res = {'msg': '用户不存在', 'status': 0}
        if i == 1 and data_1:
            sql = "select account, password, nickname from `user` where account = %s and password = %s"  # SQL语句
            cur.execute(sql, (form['account'], form['password']))  # 执行SQL语句
            data_2 = cur.fetchall()  # 通过fetchall方法获得数据
            if not data_2:
                res = {'msg': '密码错误', 'status': 0}
    if data_1 and data_2:
        res = {'msg': '登录成功', 'status': 1, 'user': {'nickname': data_2[0][2]}}
    cur.close()
    conn.close()
    return json.dumps(res, ensure_ascii=False)


server.run()
