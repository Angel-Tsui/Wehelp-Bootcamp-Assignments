from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
import mysql.connector
con=mysql.connector.connect(
    user="root",
    password="",
    host="localhost",
    database="website"
)
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
        cursor.execute("SELECT message.id, member.name, message.content, message.member_id FROM member INNER JOIN message ON member.id=message.member_id ORDER BY message.time DESC")
        all_comment=cursor.fetchall()
        con.commit()
        return render_template("member.html", loggedin_user=user_name, all_comment=all_comment, user_id=user_id)
    else:
        return redirect("/")

@app.route("/createMessage", methods=["POST"])
def createMessage():
    userinfo=session["user"]
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

@app.route("/deleteMessage", methods=["POST"])
def deleteMessage():
    userinfo=session["user"]
    user_id=userinfo["id"]
    # 根據 id 查詢要刪除的記錄並刪除他
    message_id=request.form["delete"]
    # 整理 response，刪除 "()"，然後轉成 tuple
    message_id_tidy=message_id.replace("(","")
    message_info=message_id_tidy.replace(")","")
    message_info_tuple=tuple(int(item) for item in message_info.split(','))
    # 在tuple裏面取得 member_id 作核對身份用
    message_id=message_info_tuple[0]
    member_id=message_info_tuple[1]
    if member_id == user_id:
        cursor=con.cursor(dictionary=True)
        cursor.execute("DELETE FROM message WHERE id=%s",(message_id,))
        con.commit()
        print("Delete Completed:", "user id:", user_id, ", message id:", message_id)
    else:
        print("ALERT, HACKER")
    return redirect("/member")


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
    name=request.form["name"]
    username=request.form["username"]
    pw=request.form["pw"]
    cursor=con.cursor(dictionary=True)
    cursor.execute("SELECT * FROM member WHERE username=%s",(username,))
    current_user=cursor.fetchone()
    if current_user:
        con.commit()
        return redirect("/error?message=帳號已經被註冊")
    else:
        cursor.execute("INSERT INTO member(name,username,password)VALUES(%s,%s,%s)",(name, username, pw))
        con.commit()
        return redirect("/")
    
app.run(port=3000)
# cursor.close()
con.close()
print("connection successful")
