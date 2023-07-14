from flask import request,session
from info.dbs.models import Ns_contract,Auth_user,Auth_lock,Cloud_deliver,Cloud_deliver_hw
from info import db
import redis
from http import HTTPStatus
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def Get_email_info(value):
    r =redis.Redis(host='127.0.0.1',port=6379,db=0)
    values = r.get(value)
    if values != None:
        print(values)
        return values
    else:
        return "Fail"


def Send_email(recipient, content):
    try:
        username = "guwj"
        password = "xnkslc"
        sender = "guwj@test.com"
        subject = "自动化投递任务锁入队列"
        # 创建SMTP连接
        server = smtplib.SMTP('smtp.exmail.qq.com', 587)
        server.starttls()
        # 登录账号
        server.login(username, password)
        # 构造邮件内容
        msg = MIMEText(content)
        msg['From'] = formataddr(('Sender', sender))
        msg['To'] = formataddr(('Recipient', recipient))
        msg['Subject'] = subject
        # 发送邮件
        server.sendmail(sender, [recipient], msg.as_string())
        # 关闭SMTP连接
        server.quit()
        print("邮件发送成功")
    except Exception as e:
        print("邮件发送失败: " + str(e))

def create_one(paths,users,mem,time,namespace,region):
    #data = json.loads(request.data)
    #usernames = request.form.get("username")
    #passwords = request.form.get("password")
    auth_lock = Auth_lock(path=paths, user=users, memory=mem, create_time=time, namespace=namespace, region=region)
    db.session.add(auth_lock)
    db.session.commit()
    return "deliver Fail, data is lock\n"
    #use = User(username=data.get("username"),password=data.get("password"))
#    if db.session.query(Auth_lock.path, Auth_lock.user, Auth_lock.id).filter_by(user=users).all():
#        return False
#        return {"data": None, "status_code": HTTPStatus.UNAUTHORIZED, "message": "user already exists. Change the name"}
#    else:

#        return {"status_code": 200, "message": "Write completed"}

def del_one(ids):
    auth_id = db.session.query(Auth_lock).filter(Auth_lock.id == ids).first()
    if auth_id:
        db.session.delete(auth_id)
        db.session.commit()
        db.session.close()
        return {"status_code": 200, "message": "Del completed"}
    else:
        return {"data": None, "status_code": HTTPStatus.UNAUTHORIZED, "message": "id does not exist"}

def Auth_cloud(name,passwd):
    use = db.session.query(Auth_user.auth_user, Auth_user.auth_pass).filter_by(auth_user=name).first()
    if use:
        if use[0] == str(name) and use[1] == str(passwd):
            return 'True'
    else:
        return 'Fail'

def create_cloud(name,namespace,projectId,taskId,image,callback,root_dir,cmd,slot,memory,user_id,group_id,priority,workdir,contract,create_time):
    win_deliver = Cloud_deliver(name=name,namespace=namespace,projectId=projectId,taskId=taskId,image=image,callback=callback,root_dir=root_dir,cmd=cmd,slot=slot,memory=memory,user_id=user_id,group_id=group_id,priority=priority,workdir=workdir,contract=contract,create_time=create_time)
    db.session.add(win_deliver)
    db.session.commit()
    return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Task created successfully"}

def create_cloud_hw(name,namespace,projectId,taskId,image,callback,root_dir,cmd,slot,memory,user_id,group_id,priority,workdir,contract,create_time):
    win_deliver = Cloud_deliver_hw(name=name,namespace=namespace,projectId=projectId,taskId=taskId,image=image,callback=callback,root_dir=root_dir,cmd=cmd,slot=slot,memory=memory,user_id=user_id,group_id=group_id,priority=priority,workdir=workdir,contract=contract,create_time=create_time)
    db.session.add(win_deliver)
    db.session.commit()
    return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Task created successfully"}

def Lock_cloud(user,ns,projectId,taskId,image,callback,root_dir,cmd,slot,memory,user_id,group_id,priority,workdir,contract,create_time):
    lock_deliver = Ns_contract(user=user,ns=ns,projectId=projectId,taskId=taskId,image=image,callback=callback,root_dir=root_dir,cmd=cmd,slot=slot,memory=memory,user_id=user_id,group_id=group_id,priority=priority,workdir=workdir,contract=contract,create_time=create_time)
    db.session.add(lock_deliver)
    db.session.commit()
    return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "Data Lock"}

def del_cloud(ids):
    lock_id = db.session.query(Ns_contract).filter(Ns_contract.id == ids).first()
    if lock_id:
        db.session.delete(lock_id)
        db.session.commit()
        db.session.close()
        return {"status_code": 200, "message": "Del completed"}
    else:
        return {"status_code": HTTPStatus.UNAUTHORIZED, "message": "id does not exist"}

def query_region(projectId):
    region = db.session.query(Cloud_deliver.projectId,Cloud_deliver.id).filter_by(projectId=projectId).all()
    if region:
        return "True"
    else:
        return "Fail"

def query_region_hw(projectId):
    region = db.session.query(Cloud_deliver_hw.projectId,Cloud_deliver_hw.id).filter_by(projectId=projectId).all()
    if region:
        return "True"
    else:
        return "Fail"

def query_lock_auto(Ids):
    data = db.session.query(Auth_lock.user,Auth_lock.path,Auth_lock.region).filter_by(id=Ids).all()
    if data:
        for i in data:
            pass
        return i
    else:
        return "Fail"

def query_lock_path(Path):
    data = db.session.query(Auth_lock.path).filter_by(path=Path).all()
    if data:
        for i in data:
            pass
        string_path = ''.join(i)
        return string_path
    else:
        return "Fail"

def Cloud_infos():
    info_list = []
    infos = db.session.query(Ns_contract.id,Ns_contract.user, Ns_contract.projectId, Ns_contract.memory, Ns_contract.create_time ,Ns_contract.ns).all()
    for s in infos:
        dic = {}
        dic['id'] = s.id
        dic['user'] = s.user
        dic['projectId'] = s.projectId
        dic['memory'] = s.memory
        dic['namespace'] = s.ns
        dic['create_time'] = s.create_time
        print(f'Id: {s.id} | User: {s.user} | ProjectId: {s.projectId} | Memory: {s.memory} | Create_time: {s.create_time} | Namespace: {s.namespace}')
        print('----')
        info_list.append(dic)
    return info_list

def Auto_infos():
    info_list = []
    infos = db.session.query(Auth_lock.id, Auth_lock.user, Auth_lock.path, Auth_lock.memory,Auth_lock.create_time,Auth_lock.namespace).all()
    # 类似于 select * from Books
    for s in infos:
        dic = {}
        dic['id'] = s.id
        dic['user'] = s.user
        dic['path'] = s.path
        dic['memory'] = s.memory
        dic['namespace'] = s.namespace
        dic['create_time'] = s.create_time
        print(f'Id: {s.id} | User: {s.user} | Path: {s.path} | Memory: {s.memory} | Create_time: {s.create_time} | Namespace: {s.namespace}')
        print('----')
        info_list.append(dic)
    return info_list

def query_lock_cloud(Ids):
    data = db.session.query(Ns_contract.user,Ns_contract.ns,Ns_contract.projectId,Ns_contract.taskId,Ns_contract.image,Ns_contract.callback,Ns_contract.root_dir,Ns_contract.cmd,Ns_contract.slot,Ns_contract.memory,Ns_contract.user_id,Ns_contract.group_id,Ns_contract.priority,Ns_contract.workdir).filter_by(id=Ids).all()
    if data:
        for i in data:
            pass
        return i
    else:
        return "Fail"
