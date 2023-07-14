from info.index import index_blue,other_blue
from info.roles import role_blue
from info.dbs import user_blue
from flask import render_template
from info.index.other import times
from info.index.index import check_login
from info.roles.role import permission,permission_manage,register,Login,Role
from info.dbs.user_play import create_one,query_one,update_one,del_one
from  info import csrf

@csrf.exempt
@role_blue.route("/register", methods=["POST"])
def registry():
    return register()

@csrf.exempt
@role_blue.route("/login", methods=["POST"])
def Logins():
    return Login()

@csrf.exempt
@role_blue.route("/permission_manage", methods=["POST"])
@permission(roles=[Role.ADMIN])
def permission_manage():
    return permission_manage()