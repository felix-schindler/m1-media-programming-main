from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    created_date = db.Column(db.DateTime(), default=datetime.now(timezone.utc))


@app.route("/<name>", methods=["GET", "POST"])
def hello(name):
    if request.method == "POST":
        new_message = Message(user=name, content=request.form["msg"])
        db.session.add(new_message)
        db.session.commit()
    messages = Message.query.order_by(Message.created_date).all()
    return render_template("index.html", name=name, messages=messages)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tables created")

    app.run(port=8000, debug=True)
