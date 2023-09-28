#系统基础库
import urllib3
#flask路由库
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
#用于动态规划线程
from concurrent.futures import ThreadPoolExecutor
#自定义文件获取数据库连接和图书馆数据
from SQL_link import connect_database,query_course_by_section
from qlu_lib import get_lib_seat
#用来发送邮件，自己写的
from sendm import  mail_to_send_me
#用于调试输出获取到的东西（图书馆）如果图书馆数据获取有问题的时候再进行调试
from typing import Any, Dict, List, Tuple

#禁用 urllib3 库中的 InsecureRequestWarning 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#flask后端管理
app = Flask(__name__)
CORS(app)
#线程管理
executor = ThreadPoolExecutor()

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/dark.html')
def dark():
    return render_template('dark.html')
@app.route('/mimi.html')
def mimi():
    return render_template('mimi.html')
@app.route('/about.html')
def about():
    return render_template('about.html')

#发送图书馆数据
@app.route('/api/libseat', methods=['GET', 'POST'])
def libseat():
    dt, hm, av_seat_list, un_seat_list, seat_sign = get_lib_seat()
    if len(av_seat_list) == 0:
        av_seat_list = [{'area_name': '---', 'available_num': '---'}]
    if len(un_seat_list) == 0:
        un_seat_list = [{'area_name': '---', 'available_num': '---'}]
    res = jsonify({'status': 'success', 'av_seats': av_seat_list, 'un_seats': un_seat_list, 'dt': dt, 'hm': hm,
                   'visitcount': 'OK', 'hint': '查询成功'})
    return res, 200, {"Content-Type": "application/json"}

#获取课表
@app.route('/api/data', methods=['POST'])
def data_classroom():
    data = request.get_json()  # 获取前端发送的 JSON 数据
    value = data['data']  # 获取 value 值
    result = query_course_by_section(value)
    return jsonify(result)

#获取留言板中的数据
@app.route('/api/message', methods=['POST'])
def me_classroom():
    data = request.get_json()  # 获取前端发送的 JSON 数据
    value = data['data']  # 获取 value 值
    mail_to_send_me(value)
    return ''

if __name__ == '__main__':
    #连接数据库
    connect_database()
    app.run()



