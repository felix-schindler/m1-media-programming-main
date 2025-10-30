from flask import Flask, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "6514b0a4-72eb-4011-82c2-cc2d05ad4ef2"

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.now(timezone.utc))


@app.route("/", methods=["GET", "POST"])
def hello():
    username = session.get("user")

    if not username:
        return redirect(url_for("login"))

    if request.method == "POST":
        new_message = Message(user=username, content=request.form["msg"])
        db.session.add(new_message)
        db.session.commit()
    messages = Message.query.order_by(Message.created_date).all()
    return render_template("index.html", user=username, messages=messages)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        session["user"] = username
        return redirect("/")
    return render_template("login.html")


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("user", default=None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tables created")

    app.run(port=8000, debug=True)
