from flask import Flask, render_template, request, flash, redirect, url_for
from smweb.sm import steammatch
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html.j2")

@app.route("/list", methods=["POST"])
def listpage():
    if request.form["op"] == "":
        flash('ERROR: No operation selected.')
        return redirect(url_for('/'))
    raw_users = request.form["input"].split(",")
    users = list()
    for user in raw_users:
        user = user.strip(" ").replace("https://steamcommunity.com/id/", "").replace("https://steamcommunity.com/profile/", "").replace("http://steamcommunity.com/id/", "").replace("http://steamcommunity.com/profile/", "")
        if user not in users:
            users.append(user)
    if len(users) < 2:
        flash('ERROR: Not enough profiles specified.')
        return redirect(url_for('/'))
    if request.form["op"] == "and":
        return render_template("list.html.j2", l=steammatch.and_games(users))
    elif request.form["op"] == "or":
        return render_template("list.html.j2", l=steammatch.or_games(users))
    elif request.form["op"] == "xor":
        return render_template("list.html.j2", l=steammatch.xor_games(users[0], users[1]))
    elif request.form["op"] == "diff":
        return render_template("list.html.j2", l=steammatch.diff_games(users[0], users[1]))
