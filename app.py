from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

GUARDS_FILE = "guards.json"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

def load_guards():
    if os.path.exists(GUARDS_FILE):
        with open(GUARDS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_guards(guards):
    with open(GUARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(guards, f, ensure_ascii=False, indent=4)

guards = load_guards()

@app.template_filter('format_date')
def format_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%d/%m/%Y")
    except:
        return value

@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    return render_template("index.html", guards=guards, datetime=datetime, timedelta=timedelta, username=session.get("username"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="שם משתמש או סיסמה שגויים")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/guard/<name>")
def guard_details(name):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    for g in guards:
        if g["name"] == name:
            return render_template("details.html", guard=g, datetime=datetime, timedelta=timedelta)
    return "מאבטח לא נמצא", 404

@app.route("/add", methods=["GET", "POST"])
def add_guard():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    if request.method == "POST":
        new_guard = {
            "name": request.form["name"],
            "level": request.form["level"],
            "last_refresh": request.form["last_refresh"],
            "health_declaration": request.form["health_declaration"]
        }
        guards.append(new_guard)
        save_guards(guards)
        return redirect(url_for("home"))
    return render_template("add_guard.html")

@app.route("/edit_guard/<name>", methods=["GET", "POST"])
def edit_guard(name):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    guard = next((g for g in guards if g["name"] == name), None)
    if not guard:
        return "מאבטח לא נמצא", 404

    if request.method == "POST":
        # שמירה על שם קבוע
        guard["level"] = request.form["level"]
        guard["last_refresh"] = request.form["last_refresh"]
        guard["health_declaration"] = request.form["health_declaration"]
        save_guards(guards)
        return redirect(url_for("home"))

    return render_template("edit_guard.html", guard=guard)

@app.route("/delete/<name>")
def delete_guard(name):
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    global guards
    guards = [g for g in guards if g["name"] != name]
    save_guards(guards)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
