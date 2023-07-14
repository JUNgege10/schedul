import time
from http import HTTPStatus
from flask import request,redirect,render_template,url_for
from info import db
from info.dbs.models import User,Auth_user
from info.Auth import ldap_auth

def auth_login():
    user = request.form.get("userId")
    password = request.form.get("password")
    if ldap_auth(user,password) == "True":
        return redirect("http://127.0.0.1:5000/index", 302)
    else:
        return render_template('news/user.html')


def check_login():
    user = request.form.get("userId")
    password = request.form.get("password")
    use = db.session.query(User.username, User.password).filter_by(username=user).first()
    if use:
        if use[0] == str(user) and use[1] == str(password):
            return redirect("http://127.0.0.1:8080", 302)
            #return render_template("news/index.html")
        return render_template("news/user.html")
    else:
        return render_template("news/user.html")
    return render_template('news/user.html')

def times():
    pass
    times = time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())
    return times
