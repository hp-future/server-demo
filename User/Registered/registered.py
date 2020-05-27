import json
from flask import Flask, request
import pymysql
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# 开启一个服务
server = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
CORS(server, resources=r'/*')


class Config(object):
    """配置参数"""
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:hp123456@127.0.0.1:3306/user"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


server.config.from_object(Config)

db = SQLAlchemy(server)


class User(db.Model):
    """用户表"""
    __tablename__ = "user"  # 指明数据库的表名

    account = db.Column(db.Integer, primary_key=True)  # 整型的主键，会默认设置为自增主键
    nickname = db.Column(db.String(64))
    password = db.Column(db.Integer)
    sex = db.Column(db.String)  # 从底层中


# 注册
@server.route('/registered', methods=['POST'])
def registered():
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', passwd='hp123456', port=3306, db='user', charset='utf8')
    cur = conn.cursor()  # 生成游标对象

    # 获取参数
    form = request.json
    data_1 = ''
    data_2 = ''

    # 查询数据库中已经存在的信息
    for i in range(2):
        if i == 0:
            sql = "select * from `user` where account = %s"  # SQL语句
            cur.execute(sql, int(form['account']))  # 执行SQL语句
            data_1 = cur.fetchall()  # 通过fetchall方法获得数据
            if data_1:
                res = {'msg': '用户已经注册', 'status': 0}
        if i == 1:
            sql = "select * from `user` where nickname = %s"  # SQL语句
            cur.execute(sql, form['nickname'])  # 执行SQL语句
            data_2 = cur.fetchall()  # 通过fetchall方法获得数据
            if data_1 and data_2:
                res = {'msg': '用户已经注册, 该昵称已经存在', 'status': 0}
            if not data_1 and data_2:
                res = {'msg': '该昵称已经存在', 'status': 0}
    if not data_1 and not data_2:
        user1 = User(account=form['account'], nickname=form['nickname'], password=form['password'], sex=form['sex'])
        db.session.add(user1)
        db.session.commit()
        res = {'msg': '注册成功', 'status': 1}

        cur.close()
        conn.close()

        return json.dumps(res, ensure_ascii=False)
    else:
        cur.close()
        conn.close()

        return json.dumps(res, ensure_ascii=False)


server.run()
