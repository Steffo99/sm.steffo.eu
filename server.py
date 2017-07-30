import os, sys
to_add = os.path.realpath(os.path.dirname(__file__))
if to_add not in sys.path:
    sys.path.append(to_add)

from flask import Flask, render_template, request
from raven.contrib.flask import Sentry
from sm import steammatch

with open(os.path.join(os.path.dirname(__file__), "sentrytoken.txt")) as file:
    sentrytoken = file.read()

app = Flask(__name__)
sentry = Sentry(app, dsn='https://{}@sentry.io/164282'.format(sentrytoken))

@app.route("/")
def home():
    return render_template("home.html.j2")

@app.route("/list", methods=["POST"])
def listpage():
    if "op" not in request.form or request.form["op"] == "":
        return render_template("error.html.j2", errortitle="Error", errordesc="No operation specified.")
    if "input" in request.form:
        raw_users = request.form["input"].split(",")
    else:
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
        else:
            return render_template("error.html.j2", errortitle="Error", errordesc="Invalid operation: {}".format(request.form["op"]))
    except steammatch.InvalidVanityURLError as e:
        return render_template("error.html.j2", errortitle="Error", errordesc="Invalid Vanity URL: {}".format(e.vanity))
    except steammatch.PrivateProfileError as e:
        return render_template("error.html.j2", errortitle="Error", errordesc="Profile is private: {}".format(e.steamid))
    except steammatch.SteamRequestError as e:
        return render_template("error.html.j2", errortitle="Error", errordesc="Steam API request failed: {}".format(e))
    except:
        sentry.captureException()
        return render_template("error.html.j2", errortitle="Unknown error", errordesc="The error has been reported to the site admin. Try again later!")
