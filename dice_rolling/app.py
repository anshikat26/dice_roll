from flask import Flask, render_template, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "dice_game_secret"

@app.route("/")
def index():
    if "p1_score" not in session:
        session["p1_score"] = 0
        session["p2_score"] = 0
        session["turn"] = 1
        session["last_roll"] = None
        session["winner"] = None

    return render_template(
        "index.html",
        p1=session["p1_score"],
        p2=session["p2_score"],
        turn=session["turn"],
        roll=session["last_roll"],
        winner=session["winner"]
    )

@app.route("/roll")
def roll():
    if session.get("winner"):
        return redirect(url_for("index"))

    dice = random.randint(1, 6)
    session["last_roll"] = dice

    if session["turn"] == 1:
        session["p1_score"] += dice
        session["turn"] = 2
    else:
        session["p2_score"] += dice
        session["turn"] = 1

    if session["p1_score"] >= 30:
        session["winner"] = "Player 1"
    elif session["p2_score"] >= 30:
        session["winner"] = "Player 2"

    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
