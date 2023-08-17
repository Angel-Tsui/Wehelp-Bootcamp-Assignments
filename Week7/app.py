from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
import mysql.connector
from datetime import datetime
con=mysql.connector.connect(
    user="root",
    password="",
    host="localhost",
    database="website"
)
# cursor=con.cursor(dictionary=True)
app=Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)
app.secret_key="info"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signin", methods=["POST"])
def verify():
    username=request.form["username"]
    pw=request.form["pw"]
    if len(username)==0 and len(pw)==0:
        return redirect("/error?message=請輸入賬號及密碼")
    else:
        # 從資料庫取得某個注冊了的 user 資訊，辨認正在登入的人是否曾注冊
        cursor=con.cursor(dictionary=True)
        cursor.execute("SELECT * FROM member WHERE username=%s AND password=%s",(username,pw))
        userinfo=cursor.fetchone()
        con.commit()
        if userinfo:
            session["user"]=userinfo
            return redirect("/member")
        else:
            return redirect("/error?message=賬號或密碼不正確")

@app.route("/member")
def member():
    if "user" in session:
        # 從 session 取出登入了的 user 的 id, name, username
        userinfo=session["user"]
        user_username=userinfo["username"]
        user_id=userinfo["id"]
        user_name=userinfo["name"]
        #製作留言區，把資料庫裏面所有user的content全部取出，放在畫面上
        cursor=con.cursor(dictionary=True)
        cursor.execute("SELECT message.id, member.name, message.content FROM member INNER JOIN message ON member.id=message.member_id ORDER BY message.time DESC")
        all_comment=cursor.fetchall()
        con.commit()
        return render_template("member.html", loggedin_user=user_name, all_comment=all_comment)
    else:
        return redirect("/")

@app.route("/createMessage", methods=["POST"])
def createMessage():
    if "user" in session:
        userinfo=session["user"]
        # print(userinfo)
        # 用 session 取得 user 的 id 做辨認
        user_id=userinfo['id']
        user_username=userinfo['username']
        # 從前端取得新的content
        new_message=request.form["content"]
        # 用 session 裏取得的 user id 辨認新的 content 是哪個 user 的留言，利用 foreign key 連接 member_id 和 user_id
        cursor=con.cursor(dictionary=True)
        cursor.execute("INSERT INTO message(member_id,content)VALUES(%s, %s)",(user_id, new_message))
        con.commit()
        return redirect("/member")
    else:
        return redirect("/")

@app.route("/signout")
def signout():
    del session["user"]
    # session.pop("user",None)
    return redirect("/")

@app.route("/error")
def error():
    e_message=request.args.get("message")
    return render_template("error.html", message=e_message)

@app.route("/signup", methods=["POST"])
def signup():
    cursor=con.cursor(dictionary=True)
    name=request.form["name"]
    username=request.form["username"]
    pw=request.form["pw"]
    cursor.execute("SELECT * FROM member WHERE username=%s",(username,))
    current_user=cursor.fetchone()
    if current_user:
        con.commit()
        return redirect("/error?message=帳號已經被註冊")
    else:
        cursor.execute("INSERT INTO member(name,username,password)VALUES(%s,%s,%s)",(name, username, pw))
        con.commit()
        return redirect("/")

@app.route("/api/member", methods=['GET','PATCH'])
def getName():
    if "user" in session:
        if request.method == "GET":
            # 先在後端把需要的資料處理好 (從前端取到的name 取得 id, name, username)
            cursor=con.cursor(dictionary=True)
            username=request.args.get("username")
            cursor.execute("SELECT id, name, username FROM member WHERE username=%s",(username,))
            name_query=cursor.fetchone()
            if name_query:
                query_id=name_query["id"]
                query_name=name_query["name"]
                query_username=name_query["username"]
                return {"data":{"id":query_id, "name":query_name, "username":query_username}}
            else:
                return {"data":None}
        if request.method == "PATCH":
            current_user=session["user"]
            current_name=current_user["name"]
            cursor=con.cursor(dictionary=True)
            result = request.json       # 接json物件
            new_name=result["name"]     # 把新的名字取出
            cursor.execute("UPDATE member SET name=%s WHERE name=%s",(new_name,current_name))
            con.commit()
            cursor.execute("SELECT*FROM member WHERE name=%s",(new_name,))
            updated=cursor.fetchone()
            if updated:
                session["user"]=updated
                return {"ok":True}
            else:
                return {"error":True}
    else:
        return redirect("/")

app.run(port=3000)
con.close()
print("connection successful")