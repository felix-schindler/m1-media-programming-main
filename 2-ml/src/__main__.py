from os import path

from flask import Flask, render_template

from cost import base_path

app = Flask(__name__, template_folder=path.join(base_path, "data", "templates"))


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/predictions", methods=["POST"])
def predictions():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=8000, debug=True)
