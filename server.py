from flask import Flask, render_template, request
from smweb.sm import steammatch
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html.j2")

@app.route("/list", methods=["POST"])
def listpage():
    if request.form["input"] == "":
        return "error: no input"
    if request.form["op"] == "":
        return "error: no op"
    raw_users = request.form["input"].split(",")
    users = list()
    for user in raw_users:
        users.append(user.strip(" ").replace("https://steamcommunity.com/id/", ""))
    if len(users) < 2:
        return "error: not enough users"
    if request.form["op"] == "and":
        return render_template("list.html.j2", l=steammatch.and_games(users))
    elif request.form["op"] == "or":
        return render_template("list.html.j2", l=steammatch.or_games(users))
    elif request.form["op"] == "xor":
        if len(users) > 2:
            return "error: too many users"
        return render_template("list.html.j2", l=steammatch.xor_games(users[0], users[1]))
    elif request.form["op"] == "diff":
        if len(users) > 2:
            return "error: too many users"
        return render_template("list.html.j2", l=steammatch.diff_games(users[0], users[1]))
