from info.cloud.cloud_deliver import Cloud_deliver,Cloud_deliver_unlock,hw_deliver,Vue_Post_Deliver_Unlock,Vue_Post_Del
from info.cloud import cloud_blue
from flask_cors import CORS
from flask import make_response,jsonify,request
import json
from info.dbs.db_play import Cloud_infos

@cloud_blue.after_request
def after(resp):
    resp = make_response(resp)
    resp.headers['Access-Control-Allow-Origin'] = '*'  # 允许跨域地址
    resp.headers['Access-Control-Allow-Methods'] = '*'  # 请求 ‘*’ 就是全部
    resp.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'  # 头部
    resp.headers['Access-Control-Allow-Credentials'] = 'True'
    return resp

CORS(cloud_blue, resources=r'/*', supports_credentials=True)

@cloud_blue.route('/postinfo',methods=['GET'])
def Post_Lock_info():
    response_object = {'status': 'success'}
    autu_info = Cloud_infos()
    response_object['books'] = autu_info
    return jsonify(response_object)

@cloud_blue.route('/getinfo',methods=['POST'])
def Get_Vue_info():
    return Vue_Post_Deliver_Unlock()

@cloud_blue.route('/postdel',methods=['POST'])
def Post_Del():
    return Vue_Post_Del()

@cloud_blue.route('/unlock',methods=['POST'])
def deliver_del():
    return Cloud_deliver_unlock()

@cloud_blue.route('/deliver',methods=['POST'])
def deliver():
    return Cloud_deliver()

@cloud_blue.route('/hw/runserver',methods=['POST'])
def hw_delivers():
    return hw_deliver()