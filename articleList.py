import json
import pymysql
from flask import Flask, request
from flask_cors import CORS

server = Flask(__name__)

# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
CORS(server, resources=r'/*')


@server.route('/articleList', methods=['GET'])
def articleList():
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', passwd='hp123456', port=3306, db='user',
                           charset='utf8', cursorclass=pymysql.cursors.DictCursor)
    cur = conn.cursor()  # 生成游标对象

    # 获取请求参数
    params = request.args

    sql = "select article_id, title, content, time, read_num, img from `article_list` where channel_name = %s"
    cur.execute(sql, params['channel_name'])  # 执行SQL语句
    res = cur.fetchall()  # 通过fetchall方法获得数据

    cur.close()
    conn.close()
    return json.dumps(res, ensure_ascii=False)


server.run()
