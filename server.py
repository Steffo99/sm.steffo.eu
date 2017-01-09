from flask import Flask, render_template, request, flash, redirect, url_for
from sm import steammatch
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html.j2")

@app.route("/list", methods=["POST"])
def listpage():
    try:
        if request.form["op"] == "":
            return render_template("error.html.j2", errortitle="Error", errordesc="No operation specified.")
    except KeyError:
        return render_template("error.html.j2", errortitle="Error", errordesc="No operation specified.")
    try:
        raw_users = request.form["input"].split(",")
    except KeyError:
        raw_users = []
    users = list()
    for user in raw_users:
        user = user.replace("https://steamcommunity.com/id/", "").replace("https://steamcommunity.com/profile/", "").replace("http://steamcommunity.com/id/", "").replace("http://steamcommunity.com/profile/", "").strip(" /")
        if user not in users:
            users.append(user)
    if len(users) < 2:
        return render_template("error.html.j2", errortitle="Error", errordesc="Not enough profiles specified.")
    if request.form["op"] == "and":
        return render_template("list.html.j2", l=steammatch.and_games(users))
    elif request.form["op"] == "or":
        return render_template("list.html.j2", l=steammatch.or_games(users))
    elif request.form["op"] == "xor":
        return render_template("list.html.j2", l=steammatch.xor_games(users[0], users[1]))
    elif request.form["op"] == "diff":
        return render_template("list.html.j2", l=steammatch.diff_games(users[0], users[1]))
