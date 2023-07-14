import subprocess
from flask import request
import sys,os,yaml
import json
from info.dbs.db_play import create_one,del_one,query_lock_auto,Get_email_info,Send_email
import time
from http import HTTPStatus
from info.cloud.cloud_deliver import Get_resource
import requests
from info.Auth.ldap_auth import Auth_ldap
import psutil

times = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())


def check_process(pid):
    process_exists = False
    for proc in psutil.process_iter(['pid']):
        if proc.info['pid'] == pid:
            process_exists = True
            break
    return process_exists

def exec_run(cmd):
    stdoutls = []
    def receive():
        (stdout) = \
            proc.communicate()
    try:
        for rcmd in cmd:
            proc = subprocess.Popen(rcmd,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
            while proc.returncode is None:
                stdout = proc.communicate()
            stdoutls.append(stdout)
    except Exception as e:
        print
        e
        sys.exit(0)
    finally:
        return stdoutls

def get_users(id):
    result = os.popen("id %s -un" % id)
    res = result.read()
    for line in res.splitlines():
        return line

def get_mem(path):
    with open(path + '/cluster.yaml', 'r') as f:
        data = yaml.safe_load(f)
    keyword = "mem"
    values = []
    for key in data:
        if isinstance(data[key], dict):
            for sub_key in data[key]:
                if keyword in sub_key:
                    values.append(data[key][sub_key])
        else:
            if keyword in key:
                values.append(data[key])
    flag = False
    for item in values:
        if item.isdigit() and int(item) > 256:
            flag = True
            break
    if flag:
        return 'true'
    else:
        return 'false'

def get_mem_value(path):
    with open(path + '/cluster.yaml', 'r') as f:
        data = yaml.safe_load(f)
    keyword = "mem"
    values = []
    for key in data:
        if isinstance(data[key], dict):
            for sub_key in data[key]:
                if keyword in sub_key:
                    values.append(data[key][sub_key])
        else:
            if keyword in key:
                values.append(data[key])
    total = 0
    for item in values:
        try:
            total += int(item)
        except ValueError:
            pass
    return total

def Get_Ns(path):
    with open(path + '/cluster.yaml', 'r') as f:
        data = yaml.safe_load(f)
    keyword = "namespace"
    values = []
    for key in data:
        if isinstance(data[key], dict):
            for sub_key in data[key]:
                if keyword in sub_key:
                    values.append(data[key][sub_key])
        else:
            if keyword in key:
                values.append(data[key])
    return values[0]

def Send_Email_project(ns,user,path,memory):
    if Get_email_info(ns) != "Fail":
        recipient = Get_email_info(ns).decode('utf-8')
        print(type(Get_email_info(ns)))
        print(recipient)
        content = "当前用户{0}投递任务路径为{1}，由于该任务单任务内存分配大于256G，总消耗内存为{2}。已锁入自动化任务队列，请及时处理。".format(user, path, memory)
        Send_email(recipient, content)
    else:
        return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "该Namespace{0}未设置管理员".format(ns)}

def HW_Deliver(user,path):
    url = 'http://192.168.230.10:5000/api/auto/hw/uncordon'
    payload = {
        "user": user,
        "path": path
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=payload)
    return (response.text)

def Post_deliver():
    data = json.loads(request.data)
    if data.get('user') != None and data.get('path') != None:
        #os.chdir(data.get('path'))
        Users = get_users(data.get('user'))
        #if  get_mem(data.get('user')) != 'true':
        if data.get('user') == 'guwj02':
            if data.get('task') == None:
                #job_value = 200
                #os.system("su {0} -c 'export TMP=./ && /data/software/miniconda/bin/snakemake  --cluster ""ksub"" --cluster-config cluster.yaml -j {1} --latency-wait 300 &'".format(Users,job_value))
                return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "deliver executed"}
            else:
                #job_value = data.get('task')
                #os.system("su {0} -c 'export TMP=./ && /data/software/miniconda/bin/snakemake  --cluster ""ksub"" --cluster-config cluster.yaml -j {1} --latency-wait 300 &'".format(Users, job_value))
                return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "deliver executed"}
        else:
            #create_one(data.get('path'), Users, get_mem_value(data.get('path')), times, Get_Ns(data.get('path')))
            create_one(data.get('path'), data.get('user'), "400", times,  Get_Ns(data.get('path')), "idc")
            #Send_Email_project(Get_Ns(data.get('path')),Users,data.get('path'),get_mem_value(data.get('path')))
            return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Deliver Lock"}
    else:
        return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Data missing"}

def deliver_unlock(ids):
    #data = json.loads(request.data)
    if query_lock_auto(ids) != "Fail":
        if query_lock_auto(ids)[2] == "idc":
        #if ids:
            #os.chdir(query_lock_auto(ids)[1])
            #Users = get_users(query_lock_auto(ids)[0])
            #os.system("su {0} -c 'export TMP=./ && /data/software/miniconda/bin/snakemake  --cluster ""ksub"" --cluster-config cluster.yaml -j 200 --latency-wait 300 &'".format(Users))
            del_one(int(ids))
            return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "IDC unlock and Del completed"}
        else:
            #HW_Deliver(query_lock_auto(ids)[0],query_lock_auto(ids)[1])
            del_one(int(ids))
            return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "CLOUD unlock andDel completed"}
    else:
        return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Id data missing"}

def Post_unlock():
       data = json.loads(request.data)
       if  data.get('path') != None:
           os.chdir(data.get('path'))
           exec_run(["/data/software/miniconda/bin/snakemake  --unlock"])
           return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "unlock executed"}
       else:
           return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Data missing"}

def Post_check():
       data = json.loads(request.data)
       if data.get('path') != None:
           os.chdir(data.get('path'))
           exec_run(["/data/software/miniconda/bin/snakemake -npr -s Snakefile"])
           return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "check executed"}
       else:
           return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Data missing"}

def Vue_Post_deliver_unlock():
    data = json.loads(request.data)
    print(data["id"])
    print(data["namespace"])
    print(data["ldapUser"])
    print(data["password"])
    recipient = Get_email_info(data["namespace"]).decode('utf-8')
    if query_lock_auto(data["id"]) != "Fail":
        if Auth_ldap(data["ldapUser"],data["password"]) != "True":
            return "AUTH"
        elif data["ldapUser"] == "kaiqing.di" or data["ldapUser"] == "chen.shi":
            deliver_unlock(str(data["id"]))
            return "OK"
        elif recipient.split('@')[0] != data["ldapUser"]:
            return "NS"
        else:
            deliver_unlock(str(data["id"]))
            return "OK"
    else:
        return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "IDC unlock and Del completed"}


def Vue_Post_Del():
    data = json.loads(request.data)
    print(data["id"])
    print(data["namespace"])
    print(data["username"])
    recipient = Get_email_info(data["namespace"]).decode('utf-8')
    if query_lock_auto(data["id"]) != "Fail":
        if data["username"] == "kaiqing.di" or data["username"] == "chen.shi":
            del_one(int(data["id"]))
            return "OK"
        elif recipient.split('@')[0] != data["username"]:
            return "NS"
        else:
            del_one(int(data["id"]))
            return "OK"
    else:
        return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "IDC unlock and Del completed"}
