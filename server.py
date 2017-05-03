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
        user = user.replace("https://steamcommunity.com/id/", "").replace("https://steamcommunity.com/profiles/", "").replace("http://steamcommunity.com/id/", "").replace("http://steamcommunity.com/profiles/", "").strip(" /")
        if user not in users:
            users.append(user)
    if len(users) < 2:
        return render_template("error.html.j2", errortitle="Error", errordesc="Not enough profiles specified.")
    try:
        if request.form["op"] == "and":
            return render_template("list.html.j2", l=sorted(steammatch.and_games(users), key=lambda game: game.name))
        elif request.form["op"] == "or":
            return render_template("list.html.j2", l=sorted(steammatch.or_games(users), key=lambda game: game.name))
        elif request.form["op"] == "xor":
            return render_template("list.html.j2", l=sorted(steammatch.xor_games(users[0], users[1]), key=lambda game: game.name))
        elif request.form["op"] == "diff":
            return render_template("list.html.j2", l=sorted(steammatch.diff_games(users[0], users[1]), key=lambda game: game.name))
    except steammatch.InvalidVanityURLError as e:
        return render_template("error.html.j2", errortitle="Error", errordesc="Invalid Vanity URL: {}".format(e.vanity))
    except steammatch.PrivateProfileError as e:
        return render_template("error.html.j2", errortitle="Error", errordesc="Profile is private: {}".format(e.steamid))
    except steammatch.SteamRequestError as e:
        return render_template("error.html.j2", errortitle="Error", errordesc="Steam API request failed: {} {}".format(e.requeststatus, e.requestcontent))
    except Exception as e:
        if __debug__:
            raise
        else:
            return render_template("error.html.j2", errortitle="Unknown error", errordesc=repr(e))