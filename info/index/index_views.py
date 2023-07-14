from info.index import index_blue
from info.index.index import times,check_login
from flask import render_template,request,make_response,jsonify,redirect
from flask_cors import CORS
import json
from info.dbs.db_play import query_lock_path

@index_blue.after_request
def after(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'  # 允许跨域地址
    resp.headers['Access-Control-Allow-Methods'] = '*'  # 请求 ‘*’ 就是全部
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  # 头部
    resp.headers['Access-Control-Allow-Credentials'] = 'True'
    return resp

CORS(index_blue, resources=r'/*', supports_credentials=True)

@index_blue.route('',methods=['GET','POST'])
def index():
    return times()

@index_blue.route('/path',methods=['GET','POST'])
def get_path():
    data = json.loads(request.data)
    paths = data.get('path')
    if query_lock_path(paths) != "Fail":
        print(paths)
        print(query_lock_path(paths))
        return "OK"
    else:
        return "False"



@index_blue.route('/test',methods=['GET','POST'])
def user():
    data = json.loads(request.data)
    print(data)
    if data:
        if data.get('email') == 'guwenjun' and data.get('password') == 'wifi@123':
            return "OK"
        else:
            return "FAIL"
    else:
        return "AUTH"







