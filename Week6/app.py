from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
import mysql.connector

con=mysql.connector.connect(
    user="root",
    password="",
    host="localhost",
    database="website"
    # buffered=True
)
cursor=con.cursor()

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
        cursor.execute("SELECT * FROM member WHERE username=%s AND password=%s",(username,pw))
        userinfo=cursor.fetchone()
        if userinfo:
            session["user"]=userinfo
            return redirect("/member")
        # exist=cursor.fetchall()
        # # 將所有 user 的 name 和 password 做對照，辨認正在等人的人賬號密碼對不對
        # every_user={}
        # for everyone in exist:
        #     every_username=everyone[2]
        #     every_password=everyone[3]
        #     every_user[every_username]=every_password
        # # 如果正在登入的人賬號密碼對，讓他登入
        # if (username in every_user) and (pw==every_user[username]):
        #     # 把所有關於登入了的 user 的 info 放到 session 裏面
        #     cursor.execute("SELECT * FROM member LEFT JOIN message ON member.id=message.member_id WHERE username=%s",(username,))
        #     userinfo=cursor.fetchone()
        #     session["user"]=userinfo
        #     return redirect("/member")
        else:
            return redirect("/error?message=賬號或密碼不正確")

@app.route("/member")
def member():
    if "user" in session:
        # 從 session 取出登入了的 user 的 id, name, username
        userinfo=session["user"]
        user_username=userinfo[2]
        user_id=userinfo[0]
        user_name=userinfo[1]
        # 製作留言區，把資料庫裏面所有user的content全部取出，放在畫面上
        cursor.execute("SELECT member.id, member.name, message.id, message.content FROM member INNER JOIN message ON member.id=message.member_id ORDER BY message.time DESC")
        all_comment=cursor.fetchall()
        # 指定哪些 content 可以被登入了的 user 刪除
        for x in all_comment:
            if x[0]==user_id:
                
                # print(x[0], user_id)
                # print(x[3])
        return render_template("member.html",loggedin_user=user_name, all_comment=all_comment, delete=button)
    else:
        return redirect("/")

@app.route("/createMessage", methods=["POST"])
def createMessage():
    userinfo=session["user"]
    # 用 session 取得 user 的 id 做辨認
    user_id=userinfo[0]
    user_username=userinfo[2]
    # 從前端取得新的content
    new_message=request.form["content"]
    # 用 session 裏取得的 user id 辨認新的 content 是哪個 user 的留言，利用 foreign key 連接 member_id 和 user_id
    cursor.execute("INSERT INTO message(member_id,content)VALUES(%s, %s)",(user_id, new_message))
    con.commit()
    return redirect("/member")

@app.route("/deleteMessage", methods=["POST"])
def deleteMessage():
    # 取得被刪除的留言的 message.id，再從資料庫刪除
    delete_message_id=request.form["id"]
    print(delete_message_id)
    cursor.execute("DELETE FROM message WHERE id=%s",(delete_message_id,))
    con.commit()
    return redirect("/member")

@app.route("/signout")
def signout():
    session.pop("user",None)
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
    cursor.execute("SELECT * FROM member WHERE username=%s",(username,))
    current_user=cursor.fetchone()
    if current_user:
        return redirect("/error?message=帳號已經被註冊")
    else:
        cursor.execute("INSERT INTO member(name,username,password)VALUES(%s,%s,%s)",(name, username, pw))
        con.commit()
        return redirect("/")

app.run(port=3000)
con.close()
print("connection successful")