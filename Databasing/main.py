from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import os

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

conn = pymysql.connect(
    host='*',
    user='*',
    password='*',
    database='*'
)

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("data"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()
    if user:
        session["username"] = username
        return redirect(url_for("data"))
    else:
        return render_template("login.html", error="Invalid username or password")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/data")
def data():
    if "username" not in session:
        return redirect(url_for("index"))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM data")
    data = cursor.fetchall()
    return render_template("data.html", data=data)

if __name__ == "__main__":
    app.run(host="*", port=80)
