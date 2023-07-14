import subprocess
from flask import request
import requests
import yaml
import json
import os
from http import HTTPStatus
import time
import requests
from info.dbs.db_play import Auth_cloud,create_cloud,Lock_cloud,del_cloud,query_region,create_cloud_hw,query_region_hw,query_lock_cloud
from info.Auth.ldap_auth import Auth_ldap
from info.dbs.db_play import query_lock_auto,Get_email_info

times = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

def Pay_load(name,namespace,projectId,taskId,image,callback,root_dir,cmd,slot,memory,user_id,group_id,priority,workdir):
    url = 'http://192.168.230.10:5000/api/cloud/hw/runserver'
    payload = {
        "name": name,
        "namespace": namespace,
        "projectId": projectId,
        "taskId": taskId,
        "image": image,
        "callback": callback,
        "root_dir": root_dir,
        "cmd": cmd,
        "slot": slot,
        "memory": memory,
        "user_id": user_id,
        "group_id": group_id,
        "priority": priority,
        "workdir": workdir
    }
    headers = {'Content-Type': 'application/json'}  ##需在header头中带入用户&密码做验证
    response = requests.post(url, headers=headers, json=payload)
    return (response.text)


def Get_resource(value):
    url = 'http://192.168.100.52:8888/v3/resource'
    payload = {'type': '{0}'.format(value)}
    response = requests.post(url, data=payload)
    return int(response.text)

def Chage_yaml(name,namespace,projectId,taskId,image,callback,root_dir,cmd,slot,memory,user_id,group_id,priority,workdir):
    with open("cloud.yaml", 'r') as file:
        data = yaml.safe_load(file)
    data['metadata']['name'] = name
    data['metadata']['namespace'] = namespace
    data['metadata']['annotations']['description'] = projectId + '-' + taskId
    data['spec']['template']['metadata']['name'] = name
    data['spec']['template']['spec']['containers'][0]['image'] = image
    data['spec']['template']['spec']['containers'][0]['env'][0]['value'] = callback
    data['spec']['template']['spec']['containers'][0]['env'][1]['value'] = root_dir
    data['spec']['template']['spec']['containers'][0]['command'][2] = cmd
    data['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = slot
    data['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'] = memory + 'Gi'
    data['spec']['template']['spec']['containers'][0]['resources']['limits']['cpu'] = slot
    data['spec']['template']['spec']['containers'][0]['resources']['limits']['memory'] = memory + 'Gi'
    data['spec']['template']['spec']['securityContext']['runAsUser'] = user_id
    data['spec']['template']['spec']['securityContext']['runAsGroup'] = group_id
    data['spec']['template']['spec']['priority'] = priority
    data['spec']['template']['spec']['containers'][0]['workingDir'] = workdir
    with open("cloud.yaml", 'w') as file:
        yaml.dump(data, file)

def hw_deliver():
    data = json.loads(request.data)
    Chage_yaml(data.get('name'), data.get('namespace'), data.get('projectId'), data.get('taskId'), data.get('image'),data.get('callback'), data.get('root_dir'), data.get('cmd'), data.get('slot'), data.get('memory'),data.get('user_id'), data.get('group_id'), data.get('priority'), data.get('workdir'))
    os.system("/usr/bin/kubectl create -f cluster.yaml")
    return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Cloud deliver executed"}



def Cloud_deliver():
    data = json.loads(request.data)
    name = request.headers.get('user')
    password = request.headers.get('pass')
    #if Auth_cloud(name,password) == 'True':
    if name == "xuebiao.wu" and Auth_cloud(name,password) == "True":
        if data.get('name') != None and data.get('namespace') != None and data.get('projectId') != None and data.get('taskId') != None and data.get('image') != None and data.get('callback') != None and data.get('root_dir') != None and data.get('cmd') != None and data.get('slot') != None and data.get('memory') != None and data.get('user_id') != None and data.get('group_id') != None and data.get('priority') != None and data.get('workdir') != None :
            if int(data.get('memory')) < 256:
                if query_region(data.get('projectId')) == 'Fail' and query_region_hw(data.get('projectId')) == 'Fail' and int(data.get('memory')) < Get_resource('memory') and int(data.get('slot')) < Get_resource('cpu'):
                    Chage_yaml(data.get('name'),data.get('namespace'),data.get('projectId'),data.get('taskId'),data.get('image'),data.get('callback'),data.get('root_dir'),data.get('cmd'),data.get('slot'),data.get('memory'),data.get('user_id'),data.get('group_id'),data.get('priority'),data.get('workdir'))
                    #os.system("/usr/bin/kubectl create -f cloud.yaml")
                    create_cloud(data.get('name'),data.get('namespace'),data.get('projectId'),data.get('taskId'),data.get('image'),data.get('callback'),data.get('root_dir'),data.get('cmd'),data.get('slot'),data.get('memory'),data.get('user_id'),data.get('group_id'),data.get('priority'),data.get('workdir'),'idc',times)
                    return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Idc deliver executed one"}
                elif query_region(data.get('projectId')) == 'True' and query_region_hw(data.get('projectId')) == 'Fail' and int(data.get('memory')) < Get_resource('memory') and int(data.get('slot')) < Get_resource('cpu'):
                    Chage_yaml(data.get('name'),data.get('namespace'),data.get('projectId'),data.get('taskId'),data.get('image'),data.get('callback'),data.get('root_dir'),data.get('cmd'),data.get('slot'),data.get('memory'),data.get('user_id'),data.get('group_id'),data.get('priority'),data.get('workdir'))
                    #os.system("/usr/bin/kubectl create -f cloud.yaml")
                    create_cloud(data.get('name'),data.get('namespace'),data.get('projectId'),data.get('taskId'),data.get('image'),data.get('callback'),data.get('root_dir'),data.get('cmd'),data.get('slot'),data.get('memory'),data.get('user_id'),data.get('group_id'),data.get('priority'),data.get('workdir'),'idc',times)
                    return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Idc deliver executed"}
                else:
                    #Pay_load(data.get('name'), data.get('namespace'), data.get('projectId'), data.get('taskId'),data.get('image'), data.get('callback'), data.get('root_dir'), data.get('cmd'),data.get('slot'), data.get('memory'), data.get('user_id'), data.get('group_id'),data.get('priority'),data.get('workdir'))
                    create_cloud_hw(data.get('name'), data.get('namespace'), data.get('projectId'), data.get('taskId'),data.get('image'), data.get('callback'), data.get('root_dir'), data.get('cmd'),data.get('slot'), data.get('memory'), data.get('user_id'), data.get('group_id'),data.get('priority'),data.get('workdir'),'cloud', times)
                    return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Cloud deliver executed"}
            else:
                Lock_cloud(data.get('name'),data.get('namespace'),data.get('projectId'),data.get('taskId'),data.get('image'),data.get('callback'),data.get('root_dir'),data.get('cmd'),data.get('slot'),data.get('memory'),data.get('user_id'),data.get('group_id'),data.get('priority'),data.get('workdir'),'idc',times)
                return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Data Lock"}
        else:
            return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Data missing"}
    else:
        return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "The account or password is incorrect"}

def Cloud_deliver_unlock(ids):
    #data = json.loads(request.data)
    if query_lock_cloud(ids) != "Fail":
        if query_region(query_lock_cloud(ids)[2]) == 'Fail' and query_region_hw(query_lock_cloud(ids)[2]) == 'Fail' and int(query_lock_cloud(ids)[9]) < Get_resource('memory') and int(query_lock_cloud(ids)[8]) < Get_resource('cpu'):
            Chage_yaml(query_lock_cloud(ids)[0], query_lock_cloud(ids)[1], query_lock_cloud(ids)[2], query_lock_cloud(ids)[3],query_lock_cloud(ids)[4], query_lock_cloud(ids)[5], query_lock_cloud(ids)[6],query_lock_cloud(ids)[7], query_lock_cloud(ids)[8],query_lock_cloud(ids)[9], int(query_lock_cloud(ids)[10]), int(query_lock_cloud(ids)[11]), int(query_lock_cloud(ids)[12]),query_lock_cloud(ids)[13])
            #os.system("/usr/bin/kubectl create -f cloud.yaml")
            create_cloud(query_lock_cloud(ids)[0], query_lock_cloud(ids)[1], query_lock_cloud(ids)[2], query_lock_cloud(ids)[3],query_lock_cloud(ids)[4], query_lock_cloud(ids)[5], query_lock_cloud(ids)[6], query_lock_cloud(ids)[7],query_lock_cloud(ids)[8], query_lock_cloud(ids)[9], int(query_lock_cloud(ids)[10]), int(query_lock_cloud(ids)[11]),int(query_lock_cloud(ids)[12]),query_lock_cloud(ids)[13],'idc',times)
            del_cloud(int(ids))
            return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Del completed and Idc deliver executed one"}
        elif query_region(query_lock_cloud(ids)[2]) == 'True' and query_region_hw(query_lock_cloud(ids)[2]) == 'Fail' and int(query_lock_cloud(ids)[9]) < Get_resource('memory') and int(query_lock_cloud(ids)[8]) < Get_resource('cpu'):
            Chage_yaml(query_lock_cloud(ids)[0], query_lock_cloud(ids)[1], query_lock_cloud(ids)[2], query_lock_cloud(ids)[3],query_lock_cloud(ids)[4], query_lock_cloud(ids)[5], query_lock_cloud(ids)[6],query_lock_cloud(ids)[7], query_lock_cloud(ids)[8],query_lock_cloud(ids)[9], int(query_lock_cloud(ids)[10]), int(query_lock_cloud(ids)[11]), int(query_lock_cloud(ids)[12]),query_lock_cloud(ids)[13])
            #os.system("/usr/bin/kubectl create -f cloud.yaml")
            create_cloud(query_lock_cloud(ids)[0], query_lock_cloud(ids)[1], query_lock_cloud(ids)[2], query_lock_cloud(ids)[3],query_lock_cloud(ids)[4], query_lock_cloud(ids)[5], query_lock_cloud(ids)[6], query_lock_cloud(ids)[7],query_lock_cloud(ids)[8], query_lock_cloud(ids)[9], int(query_lock_cloud(ids)[10]), int(query_lock_cloud(ids)[11]),int(query_lock_cloud(ids)[12]),query_lock_cloud(ids)[13],'idc',times)
            del_cloud(int(ids))
            return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Del completed and Idc deliver executed"}
        else:
            Pay_load(int(ids),query_lock_cloud(ids)[0], query_lock_cloud(ids)[1], query_lock_cloud(ids)[2], query_lock_cloud(ids)[3],query_lock_cloud(ids)[4], query_lock_cloud(ids)[5], query_lock_cloud(ids)[6], query_lock_cloud(ids)[7],query_lock_cloud(ids)[8], query_lock_cloud(ids)[9], int(query_lock_cloud(ids)[10]), int(query_lock_cloud(ids)[11]),int(query_lock_cloud(ids)[12]),query_lock_cloud(ids)[13])
            create_cloud_hw(query_lock_cloud(ids)[0], query_lock_cloud(ids)[1], query_lock_cloud(ids)[2], query_lock_cloud(ids)[3],query_lock_cloud(ids)[4], query_lock_cloud(ids)[5], query_lock_cloud(ids)[6], query_lock_cloud(ids)[7],query_lock_cloud(ids)[8], query_lock_cloud(ids)[9], int(query_lock_cloud(ids)[10]), int(query_lock_cloud(ids)[11]),int(query_lock_cloud(ids)[12]),query_lock_cloud(ids)[13],'cloud',times)
            return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Del completed and Cloud deliver executed"}
    else:
        return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Id data missing"}


def Vue_Post_Deliver_Unlock():
    data = json.loads(request.data)
    recipient = Get_email_info(data["namespace"]).decode('utf-8')
    if query_lock_cloud(data["id"]) != "Fail":
        if Auth_ldap(data["ldapUser"],data["password"]) != "True":
            return "AUTH"
        elif data["ldapUser"] == "kaiqing.di" or data["ldapUser"] == "chen.shi":
            Cloud_deliver_unlock(str(data["id"]))
            return "OK"
        elif recipient.split('@')[0] != data["ldapUser"]:
            return "NS"
        else:
            Cloud_deliver_unlock(str(data["id"]))
            return "OK"
    else:
        return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Cloud unlock and Del completed"}

def Vue_Post_Del():
    data = json.loads(request.data)
    recipient = Get_email_info(data["namespace"]).decode('utf-8')
    if query_lock_cloud(data["id"]) != "Fail":
        if data["username"] == "kaiqing.di" or data["username"] == "chen.shi":
            del_cloud((int(data["id"])))
            return "OK"
        elif recipient.split('@')[0] != data["username"]:
            return "NS"
        else:
            del_cloud((int(data["id"])))
            return "OK"
    else:
        return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "IDC unlock and Del completed"}