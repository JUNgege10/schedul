from info.automation.deliver import Post_check
from info.automation.deliver import Post_deliver
from info.automation.deliver import Post_unlock,Vue_Post_deliver_unlock,Vue_Post_Del
from info.automation import automation_blue
from flask_cors import CORS
from flask import make_response,jsonify,request
import json
from info.dbs.db_play import Auto_infos

@automation_blue.after_request
def after(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'  # 允许跨域地址
    resp.headers['Access-Control-Allow-Methods'] = '*'  # 请求 ‘*’ 就是全部
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  # 头部
    resp.headers['Access-Control-Allow-Credentials'] = 'True'
    return resp

CORS(automation_blue, resources=r'/*', supports_credentials=True)

@automation_blue.route('/postinfo',methods=['GET'])
def Post_Lock_info():
    response_object = {'status': 'success'}
    autu_info = Auto_infos()
    response_object['books'] = autu_info
    return jsonify(response_object)

@automation_blue.route('/getinfo',methods=['POST'])
def Get_Vue_info():
    return Vue_Post_deliver_unlock()

@automation_blue.route('/postdel',methods=['POST'])
def Post_Del():
    return Vue_Post_Del()

@automation_blue.route('/deliver',methods=['POST'])
def delivers():
    return Post_deliver()

@automation_blue.route('/unlock',methods=['POST'])
def unlocks():
    return Post_unlock()

@automation_blue.route('/check',methods=['POST'])
def checks():
    return Post_check()