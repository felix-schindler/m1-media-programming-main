from datetime import datetime, timezone
from os import path
from uuid import uuid4

from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

base_path = path.dirname(path.dirname(__file__))

app = Flask(__name__, template_folder=path.join(base_path, "data", "templates"))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{path.join(base_path, 'data', 'sqlite.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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

    app.secret_key = uuid4()

    app.run(port=8000, debug=True)
