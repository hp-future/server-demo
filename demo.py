from flask import Flask, request
import json
import pymysql
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

server = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
CORS(server, resources=r'/*')


class Config(object):
    """配置参数"""
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:hp123456@127.0.0.1:3306/user"
    SQLALCHEMY_TRACK_MODIFICATIONS = True


server.config.from_object(Config)

db = SQLAlchemy(server)

# 连接数据库
conn = pymysql.connect(
    # 连接名称，默认127.0.0.1
    host='localhost',
    # 用户名
    user='root',
    # 密码
    passwd='hp123456',
    # 端口,默认为3306
    port=3306,
    # 数据库名称
    db='user',
    # 字符编码
    charset='utf8')

cur = conn.cursor()  # 生成游标对象
sql = "select account, nickname, password, sex from `new_table` "  # SQL语句
cur.execute(sql)  # 执行SQL语句
data = cur.fetchall()  # 通过fetchall方法获得数据

a = []
for i in data:
    item = {'account': i[0], 'nickname': i[1], 'password': i[2], 'sex': i[3]}
    a.append(item)

cur.close()  # 关闭游标
conn.close()  # 关闭连接


@server.route('/getData', methods=['get'])
def getData():
    # res = {'msg': 'hello word!', 'msg_code': 0}
    res = []
    for j in a:
        j['code'] = 0
        res.append(j)

    return json.dumps(res, ensure_ascii=False)


class User(db.Model):
    """用户表"""
    __tablename__ = "new_table"  # 指明数据库的表名

    account = db.Column(db.Integer, primary_key=True)  # 整型的主键，会默认设置为自增主键
    nickname = db.Column(db.String(64))
    password = db.Column(db.Integer)
    sex = db.Column(db.String)  # 从底层中


@server.route('/registered', methods=['POST'])
def registered():
    form = request.json
    # print(form)
    user1 = User(account=form['account'], nickname=form['nickname'], password=form['password'], sex=form['sex'])
    db.session.add(user1)
    db.session.commit()

    return json.dumps(form, ensure_ascii=False)


server.run()
