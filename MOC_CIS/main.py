from crypt import methods
import json
from distutils.sysconfig import project_base
from xml.sax.handler import version

from flask import Flask, render_template, request, redirect, session
import pickle
import SQL

whowuw = None
app = Flask(__name__)
# 设置秘钥
app.config['SECRET_KEY'] = '**##$$..tuiio23'
main = json.loads(open("./static/json/main.json","r").read())
Projects = {}

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


# {
# 设置登录入口路由，响应HTML页面
@app.route("/login")
def login_enter():
    return render_template('login.html')


# 设置用户登录路由，响应登录是否成功
@app.route("/loginpost", methods=["POST"])
def login():
    user = request.values.get("user")
    pwd = request.values.get("pwd")
    result = SQL.login(user,pwd)
    if result == True:
        session["name"] =  user
        return redirect("/")
    else:
        return "用户名和密码错误"

@app.route('/sign')
def sign():
    return render_template("signup.html")

@app.route("/signpost", methods=["POST"])
def signpost():
    user = request.values.get("user")
    pwd = request.values.get("pwd")
    key = request.values.get("key")
    result = SQL.sign(user,pwd,key)
    if result == True:
        session["name"] = user
        return redirect("/")
    else:
        return '用户名已存在或邀请码已被使用或邀请码错误'

# 默认网址对应的路由
@app.route('/')
def index():
    username = session.get("name")
    if username != None:
        return render_template("index.html")
    else:
        return redirect("/login")

@app.route('/project', methods=['GET'])
def project():
    project = request.values.get("project")
    # project = "冰船"
    projectList = []
    for i in main['个人'][project]:
        projectList.append(i)

    return render_template('project.html', Projects = projectList, project =project)

@app.route('/FindPlayer', methods=['GET'])
def FindPlayer():
    project = request.values.get("project")
    Projects = request.values.get("Projects")
    PlayerList = []
    for i in main['个人'][project][Projects]:
        PlayerList.append(i)
    return render_template('player.html', PlayerList = PlayerList)

@app.route('/Athlete', methods=['GET'])
def Athlete():
    name = request.values.get("id")
    url = "./static/json/Athlete/"+name+".json"
    info = json.loads(open(url, "r").read())
    achieve = info['历史成绩']
    useVersion = info['常用游戏版本']
    points = str(info['积分'])
    mostAchieve = {}
    name = info['游戏名']

    a = []
    for i in achieve:
        type = achieve[i]['type']
        unit = achieve[i]['单位']
        del achieve[i]['type']
        del achieve[i]['单位']
        if type == 1:
            # print(i)
            for m in achieve[i]:
                a.append(achieve[i][m])
            a.sort(reverse=False)
            mostAchieve[i] = str(a[0])+unit
            a = []
        elif type == 2:
            a = []
            # print(i)
            for m in achieve[i]:
                a.append(achieve[i][m])
            a.sort(reverse = True)
            mostAchieve[i] = str(a[0])+unit
            a = []
        else:
            mostAchieve[i] = '详见下表'



    return render_template('Athlete.html',
        name = str(name),
        achieve = achieve,
        mostAchieve = mostAchieve,
        points = str(points),
        useVersion = str(useVersion),
        unit = str(unit)
    )
    # return  achieve

app.run(host='0.0.0.0',port=5000,debug=True)