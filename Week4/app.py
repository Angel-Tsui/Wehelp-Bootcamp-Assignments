from flask import Flask
from flask import request
from flask import redirect
from flask import render_template
from flask import session


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
    acc=request.form["acc"]
    pw=request.form["pw"]
    if len(acc)==0 and len(pw)==0:
        return redirect("/error?message=請輸入賬號及密碼")
    else:
        if acc=="test" and pw=="test":
            session["user"]=acc
            print(acc)
            return redirect("/member")
        else:
            return redirect("/error?message=賬號或密碼不正確")

@app.route("/member")
def member():
    if "user" in session:
        acc=session["user"]
        return render_template("member.html",message=acc)
    else:
        return redirect("/")

@app.route("/signout")
def signout():
    session.pop("user",None)
    return redirect("/")

@app.route("/error")
def error():
    e_message=request.args.get("message")
    return render_template("error.html", message=e_message)

app.run(port=3000)