import os
import time
import json
from hashlib import md5
from functools import wraps
from enum import Enum
from http import HTTPStatus
from flask import request,session
from info.dbs.models import User
from info import db
from info.dbs.user_play import create_one,query_role,query_roles,update_role

#ACCOUNTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "accounts.json")

SESSION_IDS = {}

#LOGIN_TIMEOUT = 60 * 60 * 24

LOGIN_TIMEOUT = 60
class Role(Enum):
    ADMIN = "admin"
    CMDB = "cmdb"
    GUEST = "guest"

def permission(roles=None):
    def login_required(func):
        @wraps(func)
        def inner():
            session_id = request.headers.get("session_id", "")
            global SESSION_IDS
            if session_id not in SESSION_IDS:  # 是否存在会话信心
                return {"data": None, "status_code": HTTPStatus.UNAUTHORIZED, "message": "username not login"}
            if time.time() - SESSION_IDS[session_id]["timestamp"] > LOGIN_TIMEOUT:  # 是否会话仍有效
                SESSION_IDS.pop(session_id)  # 如果失效则移除会话信息
                return {"data": None, "status_code": HTTPStatus.UNAUTHORIZED, "message": "username login timeout"}
            SESSION_IDS[session_id]["timestamp"] = time.time()  # 更新会话时间
            current_user = SESSION_IDS[session_id]
#            print(current_user)
            role_values = [role.value for role in roles]
#            print(role_values)
            user_role = current_user["user_info"].get("role").split(',')
            user_roles = set(user_role) & set(role_values)
#            print(user_roles)
            if roles is not None and user_roles == set():
                return {"data": None, "status_code": HTTPStatus.FORBIDDEN, "message": "user has no permission"}
            return func()
        return inner
    return login_required



def register():
    """注册用户信息"""
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:  # 判断用户输入的参数
        return {"data": None, "status_code": HTTPStatus.BAD_REQUEST, "message": "must have username and password"}
#    if not os.path.exists(ACCOUNTS_FILE):  # 判断是否存在指定文件
#        return {"data": None, "status_code": HTTPStatus.NOT_FOUND, "message": "not found accounts file"}
#    with open(ACCOUNTS_FILE, "r+") as f:
#        accounts = json.load(f)
#    for account in accounts:
#        if account["username"] == username:  # 判断是否用户已存在
#            return {"data": None, "status_code": HTTPStatus.CONFLICT, "message": "username is already exists"}
     #accounts.append({"username": username, "password": md5(password.encode()).hexdigest()})
#    accounts.append({"username": username, "password": password})
#    with open(ACCOUNTS_FILE, "w") as f:
#        json.dump(accounts, f, indent=2)
    if create_one(username,password) == True:
        return {"data": username, "status_code": HTTPStatus.OK, "message": "register username successfully"}
    else:
        return {"data": username, "status_code": HTTPStatus.OK, "message": "username is already exists"}


def Login():
    """用户登录"""
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return {"data": None, "status_code": HTTPStatus.BAD_REQUEST, "message": "invalid parameters"}
#    if not os.path.exists(ACCOUNTS_FILE):  # 是否存在用户信息文件
#        return {"data": None, "status_code": HTTPStatus.NOT_FOUND, "message": "not found accounts file"}
#    with open(ACCOUNTS_FILE, "r+") as f:
#        accounts = json.load(f)
#    current_user = None
#    for account in accounts:
#        if account["username"] == username:
#            current_user = account
#            break
#    if current_user is None: # 是否用户已注册
#        return {"data": None, "status_code": HTTPStatus.NOT_FOUND, "message": "username is not exists"}
#    if password != current_user["password"]:  #
    #if md5(password.encode()).hexdigest() != md5(current_user["password"].encode()).hexdigest():
#        return {"data": None, "status_code": HTTPStatus.UNAUTHORIZED, "message": "password is not correct"}
    if query_role(username,password) == "user":
        return {"data": None, "status_code": HTTPStatus.NOT_FOUND, "message": "username is not exists"}
    elif query_role(username,password) == "pass":
        return {"data": None, "status_code": HTTPStatus.UNAUTHORIZED, "message": "password is not correct"}
    global SESSION_IDS
    for session_id, session_info in SESSION_IDS.items():  # 判断用户是否已经登陆
        if session_info["user_info"].get("username") == username: # 如果已经登录则更新时间戳并返回已登陆的sessionID
            session_info["timestamp"] = time.time()
            return {"data": {"session_id": session_id}, "status_code": HTTPStatus.OK, "message": "login successfully"}
    session_id = md5((password + str(time.time())).encode()).hexdigest()  # 生成会话ID
    SESSION_IDS[session_id] = {"user_info": {'username': '{0}'.format(username),'password': '{0}'.format(password),'role': '{0}'.format(query_role(username,password))}, "timestamp": time.time()}  # 记录会话信息
    print(SESSION_IDS)
    return {"data": {"session_id": session_id}, "status_code": HTTPStatus.OK, "message": "login successfully"}


def permission_manage():
    username = request.form.get("username")
    role = request.form.get("role")
    if not username or not role:
        return {"data": None, "status_code": HTTPStatus.BAD_REQUEST}
    roles = [role.value for role in Role]
    rolesr = role.split(',')
    for i in rolesr:
        if i not in roles:  # 判断输入的角色名称是否合法
            return {"data": None, "status_code": HTTPStatus.BAD_REQUEST}
#    if not os.path.exists(ACCOUNTS_FILE):  # 是否存在用户信息文件
#        return {"data": None, "status_code": HTTPStatus.NOT_FOUND, "message": "not found accounts file"}
#    with open(ACCOUNTS_FILE, "r+") as f:
#        accounts = json.load(f)
#    permit_user = None
#    for account in accounts: # 查找被授权用户
#        if account.get("username", "") == username:
#            permit_user = account
#            break
#    if permit_user is None:  # 是否用户已注册
    if query_roles(username) == False:
        return {"data": None, "status_code": HTTPStatus.NOT_FOUND, "message": "username is not exists"}
    if update_role(username,role):
#    with open(ACCOUNTS_FILE, "w+") as f:
#        json.dump(accounts, f, indent=2)
        global SESSION_IDS
        for _, session_info in SESSION_IDS.items(): # 如果授权用户已登陆则修改session中该用户的角色信息
            if session_info["user_info"].get("username") == username:
                session_info["user_info"]["role"] = role
        return {"data": "", "status_code": HTTPStatus.OK, "message": "successfully"}